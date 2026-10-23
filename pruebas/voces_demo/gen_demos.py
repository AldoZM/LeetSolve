import os
from pathlib import Path
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(parents=True, exist_ok=True)

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
        "A mature woman in her late thirties with a deep, rich, velvety and sensual voice, "
        "alluring and intimate tone, soft breathy warmth, slow confident delivery."
    ),
]

def main():
    print("CUDA available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))

    print("Loading Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign...")
    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
        device_map="cuda:0" if torch.cuda.is_available() else "cpu",
        dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
    )

    for filename, instruct in VOICES:
        out_path = OUT_DIR / filename
        print(f"\nGenerating {filename}...")
        torch.manual_seed(42)
        wavs, sr = model.generate_voice_design(
            text=TEXT,
            language="English",
            instruct=instruct,
        )
        sf.write(str(out_path), wavs[0], sr)
        print(f"Saved: {out_path} ({len(wavs[0])/sr:.1f}s)")

if __name__ == "__main__":
    main()
