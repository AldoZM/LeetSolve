# Writes walk.json: the fast and slow pointers on 1 -> 2 -> 3 -> 4 -> 5 with n = 2, and the time of every event
# (shared by scenes.py and three/mundo.html). Event times are anchored to phrases of the narration, assuming a roughly
# even speaking rate inside a line.
import json

VALS, N = [1, 2, 3, 4, 5], 2
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where the nth `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
        assert k >= 0, (i, phrase, nth)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


def run(vals, n):
    # The real algorithm on slot indices: 0 is the dummy, 1..len are the nodes, len + 1 is null
    end = len(vals) + 1
    moves, fast, slow = [], 0, 0
    for _ in range(n + 1):
        fast += 1
        moves.append({"who": "fast", "to": fast})
    while fast != end:
        slow += 1
        moves.append({"who": "slow", "to": slow})
        fast += 1
        moves.append({"who": "fast", "to": fast})
    return moves, slow


moves, slow = run(VALS, N)
removed = slow + 1
result = VALS[:removed - 1] + VALS[removed:]
assert VALS[removed - 1] == 4 and result == [1, 2, 3, 5] and slow == 3
assert [m["to"] for m in moves] == [1, 2, 3, 1, 4, 2, 5, 3, 6]
# The voice: three head-start hops, then each pair of moves named one by one
TIMES = [at(9, "Fast moves"), at(9, "three steps"), at(9, "to the three"),
         at(10, "Slow goes"), at(10, "fast to four"),
         at(11, "Slow to two"), at(11, "fast to five"), at(11, "Slow to three"), at(11, "fast falls")]
for m, t in zip(moves, TIMES):
    m["t"] = t

walk = {
    "first": 9, "last": 13, "vals": VALS, "n": N, "moves": moves, "slow": slow, "removed": removed, "result": result,
    "start": at(9, "start on the dummy"), "together": at(10, "Now they move"),
    "sits": at(12, "Slow sits"), "before": at(12, "before the four"), "skip": at(12, "Skip it"),
    "relink": at(12, "points straight"), "toast": at(13, "Advancement", 0.05),
    "read": [at(13, "one,"), at(13, "two,"), at(13, "three,"), at(13, "five")],
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for m in moves:
    print(m)
print({k: v for k, v in walk.items() if k != "moves"})
