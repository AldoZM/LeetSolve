# Writes walk.json: per center, the time of each comparison (shared by script.py and three/walk.html)
import json

S = "abaracecar"


def compare_list(c):
    # Each comparison (l, r, kind): kind is "match", "miss" or "edge" (ran off the string)
    l, r = c // 2, (c + 1) // 2
    out = []
    while True:
        if l < 0 or r >= len(S):
            out.append((l, r, "edge"))
            break
        if S[l] != S[r]:
            out.append((l, r, "miss"))
            break
        out.append((l, r, "match"))
        l, r = l - 1, r + 1
    return out


# Slow centers get hand-placed times that follow the narration; the rest are spread evenly
slow = {
    2: {"times": [[8, 0.9], [8, 1.7], [8, 3.0]], "best": [8, 3.8]},
    12: {"times": [[10, 0.5], [10, 1.3], [10, 2.25], [10, 3.2], [11, 0.5]], "best": [11, 3.0]},
}
plan = {0: [7, 3.4], 1: [7, 4.4], 2: [8, 0.2]}
for k, c in enumerate(range(3, 12)):
    plan[c] = [9, 0.2 + k * 0.5]
plan[12] = [10, 0.05]
for k, c in enumerate(range(13, 19)):
    plan[c] = [12, 0.15 + k * 0.42]

best = 0
centers = []
for c in range(2 * len(S) - 1):
    cmps = compare_list(c)
    length = cmps[-1][1] - cmps[-1][0] - 1
    entry = {"c": c, "start": plan[c], "cmps": [list(x) for x in cmps], "len": length}
    if c in slow:
        entry["times"] = slow[c]["times"]
        entry["best"] = slow[c]["best"]
    else:
        seg, u = plan[c]
        entry["times"] = [[seg, u + 0.12 + 0.12 * k] for k in range(len(cmps))]
        if length > best:
            entry["best"] = [seg, u + 0.12 + 0.12 * len(cmps)]
    if length > best:
        best = length
    entry["fast"] = c not in slow
    centers.append(entry)

json.dump({"first": 7, "last": 12, "s": S, "centers": centers, "final": [12, 2.85]}, open("walk.json", "w"), indent=1)
print([(e["c"], e["len"], "best" in e) for e in centers])
