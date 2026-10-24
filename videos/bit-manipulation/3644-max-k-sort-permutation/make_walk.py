# Writes walk.json: the one-pass AND over the misplaced blocks and its event times (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

NUMS = [0, 3, 2, 5, 4, 1, 6]
BITS = 3
# One ore per value (value -> ore), so a block keeps its look wherever it goes
ORE = ["coal", "iron", "redstone", "lapis", "gold", "diamond", "emerald"]
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where `phrase` starts being spoken in line i (nth occurrence)
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
        assert k >= 0, (i, phrase)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


# Per block: visit (the voice names it), verdict (home / out of place), and for the misplaced ones
# "and" (its lamps fly to the panel) and "dark" (the panel shows the new value)
PLAN = [
    {"visit": at(12, "Zero", -0.15), "verdict": at(12, "home")},
    {"visit": at(13, "Three", -0.15), "verdict": at(13, "out of place"), "and": at(13, "AND it in"),
     "dark": at(13, "top lamp")},
    {"visit": at(14, "Two", -0.15), "verdict": at(14, "home")},
    {"visit": at(14, "Five", -0.1), "verdict": at(14, "is not"), "and": at(14, "Now only", -0.3),
     "dark": at(14, "last lamp")},
    {"visit": at(15, "Four", -0.15), "verdict": at(15, "home")},
    {"visit": at(15, "One is", -0.1), "verdict": at(15, "misplaced"), "and": at(15, "but its"),
     "dark": at(15, "stays at")},
    {"visit": at(16, "Six", -0.15), "verdict": at(16, "home")},
]

ans, steps = (1 << BITS) - 1, []
for i, x in enumerate(NUMS):
    st = {"i": i, "x": x, "home": x == i, "before": ans, **PLAN[i]}
    if x != i:
        assert "and" in st, i
        ans &= x
    st["after"] = ans
    steps.append(st)

walk = {
    "first": 11, "last": 16, "nums": NUMS, "bits": BITS, "ores": [ORE[x] for x in NUMS], "answer": ans,
    "intro_row": at(11, "walk the row"), "panel_in": at(11, "with a panel"), "lit": at(11, "fully lit"),
    "running": at(11, "That panel"), "toast": at(16, "Advancement", 0.05), "answer_t": at(16, "The answer"),
    "steps": steps,
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for s in steps:
    print(s)
print("answer", ans)
