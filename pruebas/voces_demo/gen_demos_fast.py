import json
import time
import urllib.request
from pathlib import Path

BASE = "https://katyado-qwen3-tts.hf.space"
OUT_DIR = Path(__file__).parent

TEXT = (
    "Two Sum, Minecraft edition. LeetCode problem number one, and an interview classic. "
    "Here's the trick. If the target is twenty three and I'm holding a fifteen, "
    "I know exactly what I need. An eight."
)

VOICES = [
    (
        "01_joven_youtuber.wav",
        "A young, energetic female voice in her early twenties, natural American accent, "
        "bright and engaging YouTube creator tone, lively pacing with clear emphasis."
    ),
    (
        "02_calida_storyteller.wav",
        "A warm, soothing female voice, gentle and natural conversational tone, "
        "clear articulation, calm and inviting storyteller style."
    ),
    (
        "03_clara_directa.wav",
        "A crisp, confident young woman's voice, brisk and sharp tech explainer delivery, "
        "natural human inflection, articulate and modern."
    ),
    (
        "04_madura_sensual.wav",
        "A mature woman in her late thirties with a deep, rich, velvety contralto voice, "
        "alluring and intimate late-night tone, soft breathy warmth, slow confident delivery."
    ),
]

def call_voice_design(text: str, desc: str, out_path: Path):
    payload = json.dumps({"data": [text, "English", desc]}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}/gradio_api/call/generate_voice_design",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        event_id = json.loads(resp.read().decode("utf-8"))["event_id"]

    sse_req = urllib.request.Request(
        f"{BASE}/gradio_api/call/generate_voice_design/{event_id}",
    )
    with urllib.request.urlopen(sse_req, timeout=180) as sse:
        event_type = None
        for raw_line in sse:
            line = raw_line.decode("utf-8", errors="replace").strip()
            if line.startswith("event:"):
                event_type = line.split(":", 1)[1].strip()
            elif line.startswith("data:"):
                data_str = line.split(":", 1)[1].strip()
                if event_type == "complete":
                    res = json.loads(data_str)
                    audio_info = res[0]
                    audio_url = audio_info.get("url") or f"{BASE}/gradio_api/file={audio_info['path']}"
                    urllib.request.urlretrieve(audio_url, str(out_path))
                    print(f"OK -> {out_path.name} ({res[1]})")
                    return
                elif event_type == "error":
                    raise RuntimeError(f"Gradio error: {data_str}")

def main():
    for filename, desc in VOICES:
        out_path = OUT_DIR / filename
        if out_path.exists() and out_path.stat().st_size > 1000:
            print(f"Skipping {filename} (already exists)")
            continue
        print(f"Generating {filename}...")
        call_voice_design(TEXT, desc, out_path)

if __name__ == "__main__":
    main()
