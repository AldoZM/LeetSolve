# Writes walk.json: one pass counting the blocks smaller than the target and equal to it, then where those
# blocks would land in the sorted row (shared by scenes.py and three/mundo.html). Times follow the narration.
import json

NUMS = [5, 2, 1, 2, 3, 2]
TARGET = 2
ORE = {1: "coal", 2: "iron", 3: "lapis", 5: "diamond"}
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0):
    # [line, seconds] where `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


# Per block: when the voice names it, and when it is counted (or skipped)
PLAN = [
    (at(11, "Five", -0.1), at(11, "bigger")),
    (at(11, "Two is", -0.1), at(11, "Equal is one")),
    (at(12, "One is", -0.1), at(12, "Less is one")),
    (at(12, "Two again", -0.1), at(12, "Equal is two")),
    (at(13, "Three", -0.1), at(13, "bigger")),
    (at(13, "the last two", -0.1), at(13, "Equal is three")),
]
less = equal = 0
steps = []
for i, x in enumerate(NUMS):
    kind = "less" if x < TARGET else "equal" if x == TARGET else "bigger"
    st = {"i": i, "x": x, "kind": kind, "visit": PLAN[i][0], "count": PLAN[i][1]}
    if kind == "less":
        st["pile"] = less
        less += 1
    elif kind == "equal":
        st["pile"] = equal
        equal += 1
    st["less"], st["equal"] = less, equal
    steps.append(st)
answer = list(range(less, less + equal))
assert answer == [i for i, x in enumerate(sorted(NUMS)) if x == TARGET] == [1, 2, 3]

walk = {
    "first": 10, "last": 15, "nums": NUMS, "target": TARGET, "ores": [ORE[x] for x in NUMS], "answer": answer,
    "less": less, "equal": equal,
    "counters": at(10, "two counters"), "place_less": at(14, "start at index less"), "place_equal": at(14, "take equal"),
    "toast": at(15, "Advancement", 0.05), "answer_t": at(15, "The answer"), "steps": steps,
}
json.dump(walk, open('walk.json', 'w'), indent=1)
print("less", less, "equal", equal, "answer", answer)
