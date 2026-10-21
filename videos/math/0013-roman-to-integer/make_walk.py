# Writes walk.json: the Roman to Integer pass and its event times (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

SYMS = list("MCMXCIV")
VAL = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
ORE = {"M": "diamond", "C": "gold", "X": "iron", "I": "coal", "V": "redstone", "D": "emerald", "L": "lapis"}
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0):
    # [line, seconds] where `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


# Per symbol: (visit, peek at the next one, verdict)
PLAN = [
    (at(10, "M is"), at(10, "followed"), at(10, "Add")),
    (at(11, "C is"), at(11, "followed"), at(11, "Subtract")),
    (at(12, "M, then"), at(12, "then X"), at(12, "Add")),
    (at(13, "X before"), at(13, "before C"), at(13, "Subtract")),
    (at(13, "C before"), at(13, "before I"), at(13, "Add")),
    (at(14, "I before"), at(14, "before V"), at(14, "Subtract")),
    (at(14, "And the last"), at(14, "nothing after"), at(14, "Add five")),
]

steps, total = [], 0
for i, ch in enumerate(SYMS):
    v = VAL[ch]
    sub = i + 1 < len(SYMS) and v < VAL[SYMS[i + 1]]
    total += -v if sub else v
    visit, peek, verdict = PLAN[i]
    steps.append({"i": i, "sym": ch, "v": v, "sub": sub, "total": total, "visit": visit, "peek": peek, "verdict": verdict})
assert total == 1994

walk = {
    "first": 9, "last": 15, "syms": SYMS, "vals": [VAL[c] for c in SYMS], "ores": [ORE[c] for c in SYMS],
    "intro_row": at(9, "walk the row"), "xp_in": at(9, "experience"), "hundred": at(12, "We're at"),
    "toast": at(15, "Advancement", 0.05), "answer": at(15, "The total"),
    "steps": steps,
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for s in steps:
    print(s)
