import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

REF_TEXT_DEFAULT = (
    "Two Sum, Minecraft edition. LeetCode problem number one, and an interview classic. "
    "Here's the trick. If the target is twenty three and I'm holding a fifteen, "
    "I know exactly what I need. An eight."
)

MODEL_ID = "Qwen/Qwen3-TTS-12Hz-0.6B-Base"


def parse_subtitles(narration_path: str) -> list[str]:
    text = Path(narration_path).read_text(encoding="utf-8")
    stripped = re.sub(r"```[^\n]*\n", "", text).replace("```", "")
    match = re.search(r"^subtitles:\s*\n(.*?)(?=\n[^\s\-\n]|\Z)", stripped, re.MULTILINE | re.DOTALL)
    if not match:
        sys.exit(f"Error: No 'subtitles:' block found in {narration_path}")
    items = [
        re.sub(r"^[ \t]*-\s*", "", line).strip()
        for line in match.group(1).splitlines()
        if re.match(r"^[ \t]*-", line)
    ]
    if not items:
        sys.exit("Error: Empty subtitles list in narration.txt")
    return items


def cache_path(text: str, ref_name: str, cache_dir: Path) -> Path:
    obj = {"model_id": MODEL_ID, "text": text, "voice": ref_name, "v": 2}
    key = hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return cache_dir / f"{key}.mp3"


def ffprobe_duration(mp3_path: str) -> float:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", mp3_path,
        ],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def concat_mp3s(parts: list[str], out_path: str) -> None:
    inputs = [arg for part in parts for arg in ("-i", part)]
    filters = [
        f"[{i}:a]apad,atrim=duration={ffprobe_duration(part):.9f},"
        f"asetpts=PTS-STARTPTS[a{i}]"
        for i, part in enumerate(parts)
    ]
    filters.append(
        "".join(f"[a{i}]" for i in range(len(parts)))
        + f"concat=n={len(parts)}:v=0:a=1[audio]"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filters),
            "-map", "[audio]", "-codec:a", "libmp3lame", "-q:a", "2", out_path,
        ],
        check=True, capture_output=True,
    )


def write_mp3_clean(audio_np, sr: int, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav_path = f.name
    try:
        sf.write(wav_path, audio_np, sr)
        # Strip leading silence and cap any internal/trailing silence > 0.22s, then add 0.08s natural tail
        af = (
            "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-40dB:"
            "stop_periods=-1:stop_duration=0.22:stop_threshold=-40dB,"
            "apad=pad_dur=0.08"
        )
        subprocess.run(
            ["ffmpeg", "-y", "-i", wav_path, "-af", af, "-codec:a", "libmp3lame", "-q:a", "2", str(out_path)],
            check=True, capture_output=True,
        )
    finally:
        if os.path.exists(wav_path):
            os.unlink(wav_path)


def run_folder(folder: Path, ref_audio: Path, model: Qwen3TTSModel, ref_text: str):
    narration_file = folder / "narration.txt"
    cache_dir = folder / ".tts-cache"
    out_audio = folder / "voiceover.mp3"
    out_ts = folder / "timestamps.json"

    subtitles = parse_subtitles(str(narration_file))
    print(f"\n=== Folder: {folder.name} ({len(subtitles)} lines) | Voice: {ref_audio.name} ===")

    # Compact silences in the reference audio so the LLM doesn't imitate long dead pauses
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as rf:
        ref_wav = rf.name
    ref_af = (
        "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-38dB:"
        "stop_periods=-1:stop_duration=0.20:stop_threshold=-38dB"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(ref_audio), "-af", ref_af, "-ar", "24000", "-ac", "1", ref_wav],
        check=True, capture_output=True,
    )

    try:
        prompt = model.create_voice_clone_prompt(ref_audio=ref_wav, ref_text=ref_text)
    finally:
        if os.path.exists(ref_wav):
            os.unlink(ref_wav)

    parts = [""] * len(subtitles)
    started = time.perf_counter()
    for i, text in enumerate(subtitles):
        cp = cache_path(text, ref_audio.stem, cache_dir)
        if cp.exists():
            parts[i] = str(cp)
            print(f"  [{i}] cached ({ffprobe_duration(str(cp)):.2f}s)")
            continue
        t0 = time.perf_counter()
        words = max(1, len(text.split()))
        for attempt in range(3):
            torch.manual_seed(100 + i * 10 + attempt)
            wavs, sr = model.generate_voice_clone(
                text=text,
                language="English",
                voice_clone_prompt=prompt,
            )
            raw_dur = len(wavs[0]) / sr
            if raw_dur <= words * 0.65 + 1.5:
                break
            print(f"    retry [{i}] attempt {attempt+1} (raw_dur={raw_dur:.2f}s too long for {words} words)")
        write_mp3_clean(wavs[0], sr, cp)
        parts[i] = str(cp)
        dur = ffprobe_duration(str(cp))
        print(f"  [{i}] done in {time.perf_counter() - t0:.1f}s -> {dur:.2f}s: {text[:45]}...")

    print(f"Generated in {time.perf_counter() - started:.1f}s. Measuring & concatenating...")
    durations = [ffprobe_duration(p) for p in parts]
    concat_mp3s(parts, str(out_audio))

    start = 0.0
    entries = []
    for i, (text, dur) in enumerate(zip(subtitles, durations)):
        entries.append({
            "index": i,
            "text": text,
            "start_s": round(start, 3),
            "end_s": round(start + dur, 3),
            "duration_s": round(dur, 3),
        })
        start += dur

    out_ts.write_text(
        json.dumps({"total_duration_s": round(start, 3), "subtitles": entries}, indent=2),
        encoding="utf-8",
    )
    print(f"Done {folder.name}: total_duration_s = {start:.2f}s")


def pick_device():
    # CUDA on the Windows laptop, MPS on Apple Silicon, CPU otherwise
    if torch.cuda.is_available():
        return "cuda:0", torch.bfloat16
    if torch.backends.mps.is_available():
        return "mps", torch.bfloat16
    return "cpu", torch.float32


def main():
    device, dtype = pick_device()
    print(f"Loading {MODEL_ID} on {device}...")
    model = Qwen3TTSModel.from_pretrained(MODEL_ID, device_map=device, dtype=dtype)
    demos = Path(__file__).resolve().parent
    # Usage: python tts_qwen_clone.py [video folder] [reference mp3]   (default: the #4 test with the chosen voice)
    folder = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else demos.parent / "0004-madura-sensual"
    ref = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else demos / "04_madura_sensual.mp3"

    run_folder(folder, ref, model, REF_TEXT_DEFAULT)


if __name__ == "__main__":
    main()
