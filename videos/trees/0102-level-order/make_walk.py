# Writes walk.json: the tree and the BFS event times (shared by script.py and three/walk.html)
import json

# id: (value, parent id, side)
NODES = [(3, None, None), (9, 0, "L"), (20, 0, "R"), (4, 1, "L"), (7, 1, "R"), (15, 2, "L"), (8, 2, "R"), (6, 4, "R"), (2, 5, "L")]

# Per level: when the size is read, when each node is popped, when each child is pushed, when the level is stored
TIMES = {
    0: {"size": [8, 0.9], "pops": [[8, 2.3]], "pushes": [[[8, 3.9], [8, 4.4]]], "done": [8, 5.2]},
    1: {"size": [9, 0.8], "pops": [[9, 1.6], [9, 3.6]], "pushes": [[[9, 2.4], [9, 2.9]], [[9, 4.6], [9, 5.1]]], "done": [9, 5.75]},
    2: {"size": [10, 1.0], "pops": [[10, 1.8], [10, 2.4], [10, 3.9], [10, 5.2]], "pushes": [[], [[10, 3.2]], [[10, 4.7]], []],
        "done": [10, 5.75]},
    3: {"size": [11, 0.8], "pops": [[11, 1.6], [11, 2.4]], "pushes": [[], []], "done": [11, 3.4]},
}


def children(i):
    kids = [j for j, (_, p, side) in enumerate(NODES) if p == i]
    return sorted(kids, key=lambda j: 0 if NODES[j][2] == "L" else 1)


levels, frontier = [], [0]
while frontier:
    levels.append(frontier)
    frontier = [c for i in frontier for c in children(i)]

events = []
for L, ids in enumerate(levels):
    tm = TIMES[L]
    events.append({"kind": "size", "level": L, "n": len(ids), "t": tm["size"]})
    for k, i in enumerate(ids):
        events.append({"kind": "pop", "level": L, "node": i, "t": tm["pops"][k]})
        events.append({"kind": "record", "level": L, "node": i, "t": [tm["pops"][k][0], round(tm["pops"][k][1] + 0.3, 3)]})
        for c, tp in zip(children(i), tm["pushes"][k]):
            events.append({"kind": "push", "level": L, "node": c, "parent": i, "side": NODES[c][2], "t": tp})
    events.append({"kind": "done", "level": L, "t": tm["done"]})

walk = {"first": 7, "last": 12, "nodes": [{"val": v, "parent": p, "side": s} for v, p, s in NODES], "levels": levels,
        "init": [7, 2.0], "events": events, "final": [12, 0.9]}
json.dump(walk, open("walk.json", "w"), indent=1)
print(levels, [[NODES[i][0] for i in l] for l in levels])
