# Writes walk.json: the tree, the post-order trace and its event times (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']

# id: (value, parent id, side)
NODES = [(-10, None, None), (9, 0, "L"), (20, 0, "R"), (-4, 1, "L"), (2, 1, "R"), (15, 2, "L"), (7, 2, "R")]
ORE = {-10: "coal", 9: "diamond", 20: "gold", -4: "redstone", 2: "lapis", 15: "emerald", 7: "iron"}
X = [0.0, -2.0, 2.0, -3.0, -1.0, 1.0, 3.0]
LVL = [0, 1, 1, 2, 2, 2, 2]


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


TIMES = {  # visit, path (score through the node), ret (what it offers up); best when it improves
    3: {"visit": at(8, "Minus four"), "path": at(8, "is negative"), "ret": at(8, "drop it")},
    4: {"visit": at(8, "Two offers"), "path": at(8, "Two offers", 0.4), "ret": at(8, "gain of two")},
    1: {"visit": at(9, "At nine"), "path": at(9, "nine plus"), "best": at(9, "eleven"), "ret": at(9, "It offers")},
    # Two leaves in one short line: spaced by hand so their steps don't pile up
    5: {"visit": [10, 0.6], "path": [10, 0.6], "best": [10, 0.95], "ret": [10, 1.3]},
    6: {"visit": [10, 1.65], "path": [10, 1.65], "ret": [10, 2.45]},
    2: {"visit": at(11, "At twenty"), "path": at(11, "the path"), "best": at(11, "new best"), "ret": at(11, "It offers")},
    0: {"visit": at(12, "At the root"), "path": at(12, "minus ten"), "ret": at(12, "So the answer")},
}


def kids(i):
    out = {"L": None, "R": None}
    for j, (_, p, side) in enumerate(NODES):
        if p == i:
            out[side] = j
    return out


trace, best = [], float("-inf")


def gain(i):
    global best
    if i is None:
        return 0
    k = kids(i)
    raw_l, raw_r = gain(k["L"]), gain(k["R"])
    left, right = max(raw_l, 0), max(raw_r, 0)
    path = NODES[i][0] + left + right
    improved = path > best
    best = max(best, path)
    ret = NODES[i][0] + max(left, right)
    trace.append({"node": i, "val": NODES[i][0], "left": left, "right": right, "lkid": k["L"], "rkid": k["R"],
                  "raw_left": raw_l if k["L"] is not None else None, "raw_right": raw_r if k["R"] is not None else None,
                  "path": path, "best": best, "improved": improved, "ret": ret, "t": TIMES[i]})
    return ret


gain(0)
assert best == 42 and [e["val"] for e in trace] == [-4, 2, 9, 15, 7, 20, -10]
for e in trace:
    if e["improved"] and "best" not in e["t"]:
        e["t"]["best"] = plus(e["t"]["path"], 0.25)

walk = {
    "first": 7, "last": 13, "trace": trace, "best_path": [5, 2, 6],
    "nodes": [{"val": v, "parent": p, "side": s, "ore": ORE[v], "x": X[i], "lvl": LVL[i]} for i, (v, p, s) in enumerate(NODES)],
    "tree_in": at(7, "run it"), "leaves": at(7, "the leaves"), "stays": at(12, "stays"),
    "toast": at(13, "Advancement", 0.05), "show": at(13, "best path is"),
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for e in trace:
    print(e["val"], e["path"], e["ret"], e["best"], e["improved"], e["t"])
