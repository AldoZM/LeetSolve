# Writes walk.json: every divisor k of the row, how it is cut, which pieces spin, where the drops are,
# and whether k counts (shared by scenes.py and three/mundo.html). Times are anchored to phrases of the narration.
import json

NUMS = [1, 2, 3, 3, 4, 3]
ORE = {1: "coal", 2: "iron", 3: "lapis", 4: "gold"}
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0):
    # [line, seconds] where `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


def drops(block):
    # Positions i (inside the piece) where block[i] > block[i + 1], going around the circle
    k = len(block)
    return [i for i in range(k) if block[i] > block[(i + 1) % k]]


def check(k):
    # The pieces of size k: their drops, how far each one spins, and whether k counts
    n, prev, ok, pieces = len(NUMS), 0, True, []
    for s in range(0, n, k):
        b = NUMS[s:s + k]
        d = drops(b)
        lo, hi = (b[(d[0] + 1) % k], b[d[0]]) if d else (b[0], b[0])
        # Rotating left by `shift` puts the smallest block (right after the drop) first
        shift = (d[0] + 1) % k if len(d) == 1 else 0
        ok = ok and len(d) <= 1 and lo >= prev
        prev = hi
        pieces.append({"start": s, "drops": [s + i for i in d], "shift": shift})
    return ok, pieces


n = len(NUMS)
ks = [k for k in range(1, n + 1) if n % k == 0]
results = {k: check(k) for k in ks}
answer = sum(k for k in ks if results[k][0])
assert answer == 5 and [k for k in ks if results[k][0]] == [2, 3]


def spun(k):
    # Slot order (original indices) once every piece of size k has spun into place
    order = []
    for p in results[k][1]:
        idx = list(range(p["start"], p["start"] + k))
        order += idx[p["shift"]:] + idx[:p["shift"]]
    return order


ident = list(range(n))
# The row's arrangements over time: [time, piece size, slot order]; blocks glide from one to the next
arrangements = [
    [at(10, "Size one"), 1, ident],
    [at(11, "Size two"), 2, ident], [at(11, "spins into"), 2, spun(2)],
    [at(13, "Size three"), 3, ident], [at(13, "spin into place"), 3, spun(3)],
    [at(14, "Size six"), 6, ident],
]
# Drop marks: [time on, time off, slot a, slot b]; b < a is a wrap from the end of a piece back to its start
marks = [
    [at(10, "Four sits"), at(11, "Size two"), 4, 5],
    [at(11, "has one drop"), at(11, "spins into"), 4, 5],
    [at(13, "One drop each"), at(13, "spin into place"), 2, 0], [at(13, "One drop each"), at(13, "spin into place"), 4, 5],
    [at(14, "drop from four"), at(15, "Advancement"), 4, 5], [at(14, "back to one"), at(15, "Advancement"), 5, 0],
]
verdicts = [[1, at(10, "fails"), False], [2, at(12, "Size two works"), True], [3, at(13, "Size three works"), True],
            [6, at(14, "it fails"), False]]
for k, _, ok in verdicts:
    assert results[k][0] == ok

walk = {
    "first": 10, "last": 15, "nums": NUMS, "ores": [ORE[x] for x in NUMS], "answer": answer,
    "arrangements": arrangements, "marks": marks, "verdicts": verdicts,
    "chain": at(12, "Each piece starts"), "toast": at(15, "Advancement", 0.05), "sum_t": at(15, "Two plus"),
}
json.dump(walk, open('walk.json', 'w'), indent=1)
print("answer", answer, {k: (r[0], [p["drops"] for p in r[1]]) for k, r in results.items()}, "spun2", spun(2), "spun3", spun(3))
