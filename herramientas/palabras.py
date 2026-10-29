# When each word of the narration is said, for the subtitles. Run with the .venv-tts Python (Whisper), after the voice:
#   python palabras.py <video folder>        -> <video folder>/words.json
# Whisper hears "google.com" where the script says "google dot com": the script words are kept and the ones Whisper
# heard differently get the times of what it heard there, split by length.
import json
import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
from transformers import pipeline

LEAD = 0.15  # audio before the line, so Whisper does not drop a soft first word

folder = Path(sys.argv[1])
lines = json.load(open(folder / 'timestamps.json', encoding='utf-8'))['subtitles']
asr = pipeline('automatic-speech-recognition', model='openai/whisper-base.en', device='cpu')
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())


def heard_words(line):
    a = max(0.0, line['start_s'] - LEAD)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-t', str(line['end_s'] - a), '-i',
                          str(folder / 'voiceover.mp3'), '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    out = asr({'raw': np.frombuffer(raw, dtype=np.float32), 'sampling_rate': 16000}, return_timestamps='word')
    words = []
    for c in out['chunks']:
        t0, t1 = c['timestamp']
        t1 = t1 if t1 is not None else line['end_s'] - a
        words.append({'w': c['text'].strip(), 'start': a + t0, 'end': a + t1})
    return words


def spread(script, t0, t1):
    # Times for script words with no exact match, split by length between t0 and t1
    sizes = [max(1, len(norm(w))) for w in script]
    total, k, out = sum(sizes), 0, []
    for w, s in zip(script, sizes):
        a = t0 + (t1 - t0) * k / total
        k += s
        out.append({'w': w, 'start': a, 'end': t0 + (t1 - t0) * k / total})
    return out


result = []
for line in lines:
    script = line['text'].split()
    heard = heard_words(line)
    timed = []
    sm = SequenceMatcher(None, [norm(w) for w in script], [norm(h['w']) for h in heard], autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            timed += [{'w': script[i1 + k], 'start': heard[j1 + k]['start'], 'end': heard[j1 + k]['end']}
                      for k in range(i2 - i1)]
        elif i2 > i1:
            if j2 > j1:
                t0, t1 = heard[j1]['start'], heard[j2 - 1]['end']
            else:
                # Nothing heard for these words: the gap between the neighbours
                t0 = timed[-1]['end'] if timed else line['start_s']
                t1 = heard[j1]['start'] if j1 < len(heard) else max(t0, line['end_s'] - 0.35)
            timed += spread(script[i1:i2], t0, t1)
    # Whisper's times run a little early and are not always increasing: nothing before the line, nothing before the last word
    timed[0]['start'] = max(timed[0]['start'], line['start_s'])
    for a, b in zip(timed, timed[1:]):
        b['start'] = max(b['start'], a['start'])
    for w in timed:
        w['start'], w['end'] = round(w['start'], 3), round(max(w['end'], w['start']), 3)
    result.append({'index': line['index'], 'start_s': line['start_s'], 'end_s': line['end_s'], 'words': timed})
    print(line['index'], ' '.join(f"{w['w']}@{w['start']:.2f}" for w in timed[:6]), '...')

json.dump({'lines': result}, open(folder / 'words.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('words.json:', sum(len(r['words']) for r in result), 'words')
