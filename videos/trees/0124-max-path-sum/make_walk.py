# Writes walk.json: the tree, the post-order trace and its event times (shared by script.py and three/walk.html)
import json

# id: (value, parent id, side)
NODES = [(-10, None, None), (9, 0, "L"), (20, 0, "R"), (-4, 1, "L"), (2, 1, "R"), (15, 2, "L"), (7, 2, "R")]
TIMES = {  # visit, path, ret (+ best when it improves)
    3: {"visit": [8, 0.2], "path": [8, 0.6], "ret": [8, 1.2], "drop": [8, 2.0]},
    4: {"visit": [8, 2.9], "path": [8, 3.3], "ret": [8, 3.9]},
    1: {"visit": [9, 0.2], "path": [9, 1.8], "best": [9, 2.6], "ret": [9, 3.8]},
    5: {"visit": [10, 0.2], "path": [10, 0.5], "ret": [10, 1.0]},
    6: {"visit": [10, 1.5], "path": [10, 1.8], "ret": [10, 2.3]},
    2: {"visit": [11, 0.3], "path": [11, 2.4], "best": [11, 3.6], "ret": [11, 5.6]},
    0: {"visit": [12, 0.2], "path": [12, 2.6], "ret": [12, 4.2]},
}


def kids(i):
    out = {"L": None, "R": None}
    for j, (_, p, side) in enumerate(NODES):
        if p == i:
            out[side] = j
    return out


trace, best = [], float("-inf")
gains = {}


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
    gains[i] = ret
    trace.append({"node": i, "val": NODES[i][0], "left": left, "right": right, "raw_left": raw_l if k["L"] is not None else None,
                  "raw_right": raw_r if k["R"] is not None else None, "path": path, "best": best, "improved": improved, "ret": ret,
                  "lkid": k["L"], "rkid": k["R"]})
    return ret


gain(0)
for e in trace:
    tm = TIMES[e["node"]]
    e.update({"t_" + k: v for k, v in tm.items()})
    if e["improved"] and "best" not in tm:
        e["t_best"] = [tm["path"][0], round(tm["path"][1] + 0.25, 3)]

walk = {"first": 7, "last": 12, "nodes": [{"val": v, "parent": p, "side": s} for v, p, s in NODES], "trace": trace,
        "best_path": [5, 2, 6], "final": [12, 4.8]}
json.dump(walk, open("walk.json", "w"), indent=1)
print([(e["val"], e["path"], e["ret"], e["best"], e["improved"]) for e in trace])
