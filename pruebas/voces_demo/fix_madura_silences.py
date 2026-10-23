import hashlib
import json
import subprocess
from pathlib import Path

MODEL_ID = "Qwen/Qwen3-TTS-12Hz-0.6B-Base"


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


def main():
    folder = Path(__file__).resolve().parent.parent / "0004-madura-sensual"
    ts = json.loads((folder / "timestamps.json").read_text(encoding="utf-8"))["subtitles"]
    af = (
        "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-38dB:"
        "stop_periods=-1:stop_duration=0.22:stop_threshold=-38dB,"
        "apad=pad_dur=0.08"
    )
    parts = []
    for i, s in enumerate(ts):
        obj = {"model_id": MODEL_ID, "text": s["text"], "voice": "04_madura_sensual"}
        key = hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        raw_mp3 = folder / ".tts-cache" / f"{key}.mp3"
        clean_mp3 = folder / ".tts-cache" / f"{key}_clean.mp3"
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(raw_mp3), "-af", af, "-codec:a", "libmp3lame", "-q:a", "2", str(clean_mp3)],
            check=True, capture_output=True,
        )
        dur = ffprobe_duration(str(clean_mp3))
        print(f"[{i:02d}] old={s['duration_s']:5.2f}s -> new={dur:5.2f}s | {s['text'][:50]}")
        parts.append(str(clean_mp3))

    out_audio = folder / "voiceover.mp3"
    concat_mp3s(parts, str(out_audio))
    durations = [ffprobe_duration(p) for p in parts]
    start = 0.0
    entries = []
    for i, (s, dur) in enumerate(zip(ts, durations)):
        entries.append({
            "index": i,
            "text": s["text"],
            "start_s": round(start, 3),
            "end_s": round(start + dur, 3),
            "duration_s": round(dur, 3),
        })
        start += dur

    (folder / "timestamps.json").write_text(
        json.dumps({"total_duration_s": round(start, 3), "subtitles": entries}, indent=2),
        encoding="utf-8",
    )
    print(f"Total new duration: {start:.2f}s")


if __name__ == "__main__":
    main()
