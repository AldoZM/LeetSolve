# Writes walk.json: the sliding window over the string and its event times (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

S = "abcbdea"
ORE = {"a": "gold", "b": "diamond", "c": "redstone", "d": "lapis", "e": "emerald"}
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where the nth `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
        assert k >= 0, (i, phrase, nth)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


def plus(spec, s):
    return [spec[0], round(spec[1] + s, 3)]


# Per block: visit (the right edge reaches it), check (the chest is asked; only for repeats), jump, store
# Short words like "a, b, and c" are spoken slower than their letter count says, so those visits are spaced by hand
PLAN = [
    {"visit": [10, 0.1]},
    {"visit": [10, 0.6]},
    {"visit": [10, 1.1]},
    {"visit": at(11, "b shows"), "check": at(11, "The chest says"), "jump": at(11, "jumps")},
    {"visit": [12, 0.1]},
    {"visit": [12, 0.75]},
    {"visit": at(13, "comes a"), "check": at(13, "The chest says"), "ignore": at(13, "So we")},
]
# New letters are stored right after their visit; repeats update their slot after the decision
for k, d in enumerate((0.0, 0.45, 0.9)):
    PLAN[k]["store"] = at(10, "Each goes", d)
PLAN[3]["store"] = plus(PLAN[3]["jump"], 0.55)
PLAN[4]["store"] = plus(PLAN[4]["visit"], 0.45)
PLAN[5]["store"] = plus(PLAN[5]["visit"], 0.45)
PLAN[6]["store"] = plus(PLAN[6]["ignore"], 0.4)

last, left, best, steps = {}, 0, 0, []
for r, ch in enumerate(S):
    prev = last.get(ch, -1)
    jump = prev >= left
    new_left = prev + 1 if jump else left
    best = max(best, r - new_left + 1)
    st = {"r": r, "ch": ch, "ore": ORE[ch], "prev": prev, "repeat": jump, "left0": left, "left": new_left, "best": best,
          **PLAN[r]}
    steps.append(st)
    last[ch] = r
    left = new_left
assert best == 5 and [s["repeat"] for s in steps] == [False, False, False, True, False, False, False]

walk = {
    "first": 9, "last": 14, "s": S, "ores": [ORE[c] for c in S], "letters": sorted(ORE), "ore_of": ORE,
    "row_in": at(9, "run it"), "window_in": at(9, "window starts"), "chest_in": at(9, "chest has"),
    "grows3": at(10, "window grows"), "four": at(12, "Length four"), "toast": at(14, "Advancement", 0.05),
    "five": at(14, "grows to five"), "answer": at(14, "That's the answer"),
    "steps": steps,
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for s in steps:
    print({k: v for k, v in s.items() if k not in ("ore",)})
