# Transcribes each narration line of a video folder with Whisper and compares it with the script, so TTS glitches
# (missing, repeated or invented words) show up before the render. Run with the .venv-tts Python:
#   python check_voice.py <video folder>
import json
import re
import subprocess
import sys
import tempfile
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
from transformers import pipeline

folder = Path(sys.argv[1])
subs = json.load(open(folder / 'timestamps.json', encoding='utf-8'))['subtitles']
asr = pipeline('automatic-speech-recognition', model='openai/whisper-base.en', device='cpu')
norm = lambda s: re.sub(r'[^a-z0-9 ]', ' ', s.lower().replace('-', ' ')).split()
bad = 0
for s in subs:
    # 16 kHz mono slice of the line from voiceover.mp3
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(s['start_s']), '-t', str(s['duration_s']), '-i',
                          str(folder / 'voiceover.mp3'), '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, dtype=np.float32)
    heard = asr({'raw': audio, 'sampling_rate': 16000})['text'].strip()
    ratio = SequenceMatcher(None, norm(s['text']), norm(heard)).ratio()
    flag = '' if ratio >= 0.75 else '  <-- CHECK'
    bad += bool(flag)
    print(f"{s['index']:2d} {ratio:.2f}{flag}\n   script: {s['text']}\n   heard:  {heard}")
print(f'{bad} lines to check')
