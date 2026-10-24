# Writes walk.json: finding zero, reading the circle, and the two forward plans with their moves
# (shared by scenes.py and three/mundo.html). Event times are anchored to phrases of the narration.
import json

NUMS = [1, 2, 3, 4, 5, 0]
# One ore per value (value -> ore), so a block keeps its look wherever it moves
ORE = ["coal", "iron", "redstone", "lapis", "gold", "diamond"]
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where `phrase` starts being spoken in line i (nth occurrence)
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
        assert k >= 0, (i, phrase)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


def reverse(row):
    return row[::-1]


def rotate(row):
    return row[1:] + row[:1]


n, p = len(NUMS), NUMS.index(0)
forward = all(NUMS[(p + i) % n] == i for i in range(n))
assert forward
plan1, plan2 = p, (n - p) % n + 2
answer = min(plan1, plan2)

# Plan two, move by move: the row after each pull
moves = [("reverse", at(13, "Reverse,")), ("rotate", at(14, "Rotate once")), ("reverse", at(14, "Reverse again"))]
rows = [NUMS]
for kind, _ in moves:
    rows.append(reverse(rows[-1]) if kind == "reverse" else rotate(rows[-1]))
assert rows[-1] == sorted(NUMS) and len(moves) == plan2

# Reading the circle forwards from zero: value v is read at the word that names it
WORDS = ["zero,", "one,", "two,", "three,", "four,", "five."]
reads = [at(11, w, -0.05) for w in WORDS]

walk = {
    "first": 10, "last": 15, "nums": NUMS, "ores": [ORE[x] for x in NUMS], "p": p,
    "plan1": plan1, "plan2": plan2, "answer": answer,
    "find": at(10, "First we find"), "found": at(10, "index five"),
    "reads": reads, "holds": at(11, "The circle holds"), "compare": at(11, "compare the two"),
    "plan1_t": at(12, "Plan one"), "plan1_cost": at(12, "five pulls"),
    "plan2_t": at(13, "Plan two"), "backwards": at(13, "runs backwards"),
    "moves": [{"kind": k, "t": t, "after": r} for (k, t), r in zip(moves, rows[1:])],
    "sorted": at(14, "it's sorted"),
    "toast": at(15, "Advancement", 0.05), "beat": at(15, "Three pulls"), "answer_t": at(15, "The answer"),
}
json.dump(walk, open('walk.json', 'w'), indent=1)
print("p", p, "plan1", plan1, "plan2", plan2, "answer", answer)
for m in walk["moves"]:
    print(m)
