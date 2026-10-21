# Writes walk.json: every center, its comparisons and their times (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

S = "abaracecar"
ORE = {"a": "gold", "b": "diamond", "c": "redstone", "e": "emerald", "r": "lapis"}
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where the nth `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
        assert k >= 0, (i, phrase, nth)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


def compare_list(c):
    # Each comparison (l, r, kind): kind is "match", "miss" or "edge" (ran off the row)
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


# Two slow centers follow the narration; the rest are quick and evenly spread
SLOW = {
    2: {"start": at(9, "Center on"), "times": [at(9, "Center on", 0.5), at(9, "a matches"), at(9, "so a b a")],
        "best": at(9, "Our best")},
    12: {"start": at(11, "Now center"), "times": [at(11, "on e"), at(11, "c matches"), at(11, "a matches"), at(11, "r matches"),
                                                  at(12, "hit the end")], "best": at(13, "Racecar")},
}
START = {0: [8, 3.6], 1: [8, 4.5]}
for k, c in enumerate(range(3, 12)):
    START[c] = [10, round(0.2 + k * 0.5, 3)]
for k, c in enumerate(range(13, 19)):
    START[c] = [14, round(0.15 + k * 0.5, 3)]

best, centers = 0, []
for c in range(2 * len(S) - 1):
    cmps = compare_list(c)
    length = cmps[-1][1] - cmps[-1][0] - 1
    e = {"c": c, "cmps": [list(x) for x in cmps], "len": length, "fast": c not in SLOW}
    if c in SLOW:
        e.update(SLOW[c])
    else:
        line, u = START[c]
        e["start"] = [line, u]
        e["times"] = [[line, round(u + 0.1 + 0.08 * k, 3)] for k in range(len(cmps))]
        if length > best:
            e["best"] = [line, round(u + 0.15 + 0.08 * len(cmps), 3)]
    if length > best:
        best = length
        e["new_best"] = True
    centers.append(e)
assert best == 7 and [e["c"] for e in centers if e.get("new_best")] == [0, 2, 12]

walk = {
    "first": 8, "last": 14, "s": S, "ores": [ORE[ch] for ch in S], "ore_of": ORE, "letters": sorted(ORE),
    "row_in": at(8, "run it"), "toast": at(13, "Advancement", 0.05), "beats": at(14, "nothing beats"),
    "centers": centers,
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for e in centers:
    print(e["c"], e["len"], e["start"], e.get("best"), [x[2] for x in e["cmps"]])
