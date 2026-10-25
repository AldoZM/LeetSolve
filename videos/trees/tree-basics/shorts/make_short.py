# Cuts one vertical short out of the long guide: its voice is a slice of largo/voiceover.mp3, no new TTS.
# Usage (from a short's folder): python ../make_short.py FIRST LAST [END_CARD_S]
# Writes timestamps.json with every line of the long video shifted so FIRST starts at 0 (same indices, so walk.json
# and at() keep working), plus one silent line at the end for the "full video" card; voiceover.mp3 and narration.txt.
import json, os, shutil, subprocess, sys

LARGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'largo')
first, last = int(sys.argv[1]), int(sys.argv[2])
card = float(sys.argv[3]) if len(sys.argv) > 3 else 3.5

subs = json.load(open(os.path.join(LARGO, 'timestamps.json'), encoding='utf-8'))['subtitles']
t0, t1 = subs[first]['start_s'], subs[last]['end_s']
out = []
for s in subs:
    out.append({**s, 'start_s': round(s['start_s'] - t0, 3), 'end_s': round(s['end_s'] - t0, 3)})
end = {'index': len(subs), 'text': '', 'start_s': round(t1 - t0, 3), 'end_s': round(t1 - t0 + card, 3), 'duration_s': card}
out.append(end)
json.dump({'total_duration_s': end['end_s'], 'subtitles': out}, open('timestamps.json', 'w', encoding='utf-8'), indent=2)

# Voice: the exact slice of the long voiceover, then silence for the card
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(LARGO, 'voiceover.mp3'), '-af',
                f'atrim=start={t0}:end={t1},asetpts=PTS-STARTPTS,apad=pad_dur={card}', '-ac', '1',
                '-c:a', 'libmp3lame', '-q:a', '2', 'voiceover.mp3'], check=True)
with open('narration.txt', 'w', encoding='utf-8') as f:
    f.write('subtitles:\n' + ''.join(f"- {subs[i]['text']}\n" for i in range(first, last + 1)))
shutil.copy(os.path.join(LARGO, 'walk.json'), 'walk.json')
print(f'lines {first}-{last}: {t1 - t0:.3f} s of voice + {card} s card, end card is line {end["index"]}')
