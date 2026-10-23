# Writes walk.json: the binary search of the cut and its event times (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

A = [1, 3, 8, 9, 15]
B = [7, 11, 18, 19, 21, 25]
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']
INF = 10 ** 9


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where the nth `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
        assert k >= 0, (i, phrase, nth)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


PLAN = [
    {"cutA": at(10, "i equals"), "cutB": at(10, "forces j"), "sides": at(10, "The left side"),
     "chk1": at(11, "Check across"), "chk2": at(11, "Nineteen"), "move": at(11, "too far")},
    {"cutA": at(12, "Now i"), "cutB": at(12, "j is two"),
     "chk1": at(13, "Nine is"), "chk2": at(13, "eleven is"), "valid": at(13, "Both checks")},
]

m, n = len(A), len(B)
half = (m + n + 1) // 2
lo, hi, steps = 0, m, []
while lo <= hi:
    i = (lo + hi) // 2
    j = half - i
    L1 = A[i - 1] if i else -INF
    R1 = A[i] if i < m else INF
    L2 = B[j - 1] if j else -INF
    R2 = B[j] if j < n else INF
    st = {"lo": lo, "hi": hi, "i": i, "j": j, "L1": L1, "R1": R1, "L2": L2, "R2": R2,
          "ok1": L1 <= R2, "ok2": L2 <= R1, **PLAN[len(steps)]}
    steps.append(st)
    if L1 <= R2 and L2 <= R1:
        median = max(L1, L2)
        break
    if L1 > R2:
        hi = i - 1
    else:
        lo = i + 1
assert median == 11 and [(s["i"], s["j"]) for s in steps] == [(2, 4), (4, 2)]

walk = {
    "first": 9, "last": 14, "a": A, "b": B, "half": half, "median": median,
    "row_in": at(9, "search"), "range": at(9, "anywhere"), "toast": at(14, "Advancement", 0.05),
    "odd": at(14, "The total"), "largest": at(14, "largest"), "answer": at(14, "That's eleven"),
    "steps": steps,
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for s in steps:
    print(s)
print({k: walk[k] for k in ("row_in", "range", "toast", "odd", "largest", "answer")})
