# Writes walk.json: the tree and the BFS events with their times (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']

# id: (value, parent id, side)
NODES = [(3, None, None), (9, 0, "L"), (20, 0, "R"), (4, 1, "L"), (7, 1, "R"), (15, 2, "L"), (8, 2, "R"), (6, 4, "R"), (2, 5, "L")]
ORE = {3: "gold", 9: "diamond", 20: "emerald", 4: "redstone", 7: "lapis", 15: "iron", 8: "coal", 6: "diamond", 2: "redstone"}


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where the nth `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
        assert k >= 0, (i, phrase, nth)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


def end(i, back):
    return [i, round(SUBS[i]['duration_s'] - back, 3)]


def children(i):
    kids = [j for j, (_, p, side) in enumerate(NODES) if p == i]
    return sorted(kids, key=lambda j: 0 if NODES[j][2] == "L" else 1)


# Per level: when its size is read, when each node is popped, when each child is pushed, when the level is stored
TIMES = {
    0: {"size": at(8, "holds one"), "pops": [at(8, "Pop three")], "pushes": [[at(8, "push nine"), at(8, "and twenty")]],
        "done": end(8, 0.35)},
    1: {"size": at(9, "Two blocks"), "pops": [at(9, "Pop nine"), at(9, "Pop twenty")],
        "pushes": [[at(9, "push four"), at(9, "and seven")], [at(9, "push fifteen"), at(9, "and eight")]], "done": end(9, 0.3)},
    2: {"size": at(10, "holds four"), "pops": [at(10, "Pop them"), at(10, "Seven brings", -0.2), at(10, "fifteen brings", -0.2),
                                               at(10, "brings two", 0.3)],
        "pushes": [[], [at(10, "brings six")], [at(10, "brings two")], []], "done": end(10, 0.22)},
    3: {"size": at(11, "Level three", 0.3), "pops": [at(11, "Six and"), at(11, "have no", 0.1)], "pushes": [[], []],
        "done": at(11, "nothing new")},
}

levels, frontier = [], [0]
while frontier:
    levels.append(frontier)
    frontier = [c for i in frontier for c in children(i)]
assert [[NODES[i][0] for i in l] for l in levels] == [[3], [9, 20], [4, 7, 15, 8], [6, 2]]

events = []
for L, ids in enumerate(levels):
    tm = TIMES[L]
    events.append({"kind": "size", "level": L, "n": len(ids), "t": tm["size"]})
    for k, i in enumerate(ids):
        events.append({"kind": "pop", "level": L, "node": i, "t": tm["pops"][k]})
        for c, tp in zip(children(i), tm["pushes"][k]):
            events.append({"kind": "push", "level": L, "node": c, "parent": i, "t": tp})
    events.append({"kind": "done", "level": L, "t": tm["done"]})

# Layout of the drawing: x per node (level 0 on top)
SPREAD = [2.4, 1.2, 0.6]
xs = {0: 0.0}
for i, (_, p, side) in enumerate(NODES):
    if p is not None:
        lvl = next(L for L, ids in enumerate(levels) if p in ids)
        xs[i] = xs[p] + (-1 if side == "L" else 1) * SPREAD[lvl]

walk = {
    "first": 7, "last": 13, "levels": levels, "events": sorted(events, key=lambda e: (e["t"][0], e["t"][1])),
    "nodes": [{"val": v, "parent": p, "side": s, "ore": ORE[v], "x": xs[i],
               "lvl": next(L for L, ids in enumerate(levels) if i in ids)} for i, (v, p, s) in enumerate(NODES)],
    "init": at(7, "starts with"), "tree_in": at(7, "run it"), "empty": at(12, "queue is empty"), "all": at(12, "all four"),
    "toast": at(13, "Advancement", 0.05), "rows": at(13, "four clean"),
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for e in walk["events"]:
    print(e)
