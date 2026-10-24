# Writes walk.json: the tree with its empty children, the depth first tour around it, and every 3D event of the three
# sharp sections (anatomy, depth first, search tree) anchored to the narration. Shared by scenes.py and three/mundo.html.
import json

TREE = {8: (3, 10), 3: (1, 6), 10: (None, 14), 1: (None, None), 6: (None, None), 14: (13, None), 13: (None, None)}
ORE = {8: "diamond", 3: "iron", 10: "lapis", 1: "coal", 6: "redstone", 14: "gold", 13: "emerald"}
SPREAD = (2.0, 1.0, 0.5, 0.32)
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where the nth `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
    assert k >= 0, (i, phrase)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


def words(i, ws, start=""):
    # [line, seconds] of each word, searched one after another
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(start) if start else 0
    out = []
    for w in ws:
        k = text.find(w, k)
        assert k >= 0, (i, w)
        out.append([i, round(min(dur - 0.1, dur * k / len(text)), 3)])
        k += len(w)
    return out


def end(i, back=0.15):
    return [i, round(SUBS[i]['duration_s'] - back, 3)]


# Tokens in preorder, "#" for an empty child (same layout as comun.py)
toks = []


def lay(v, x, lvl, parent):
    tok = {"x": x, "lvl": lvl, "parent": parent}
    toks.append(tok)
    if v is None:
        tok["tok"] = "#"
        return
    tok.update({"tok": str(v), "value": v, "ore": ORE[v]})
    me = len(toks) - 1
    lay(TREE[v][0], x - SPREAD[lvl], lvl + 1, me)
    lay(TREE[v][1], x + SPREAD[lvl], lvl + 1, me)


lay(8, 0.0, 0, None)

# Euler tour: every block is passed on its left (pre), underneath (in) and on its right (post); an empty child is a bump
tour = []


def walk(v):
    tour.append(["pre", v])
    left, right = TREE[v]
    if left is None:
        tour.append(["nullL", v])
    else:
        walk(left)
    tour.append(["in", v])
    if right is None:
        tour.append(["nullR", v])
    else:
        walk(right)
    tour.append(["post", v])


walk(8)
idx = {tuple(e): k for k, e in enumerate(tour)}
PRE = [8, 3, 1, 6, 10, 14, 13]
IN = [1, 3, 6, 8, 10, 13, 14]
POST = [1, 6, 3, 13, 14, 10, 8]
NAMES = {1: "one", 3: "three", 6: "six", 8: "eight", 10: "ten", 13: "thirteen", 14: "fourteen"}


def keys(pairs):
    return [[k, t] for k, t in pairs]


# First pass (lines 22 and 23): the voice names the stops
w22 = words(22, ["Eight", "three", "one", "three", "six"])
w23 = words(23, ["Three is done", "eight", "Ten", "fourteen", "thirteen"])
first = keys([(idx[("pre", 8)], w22[0]), (idx[("pre", 3)], w22[1]), (idx[("pre", 1)], w22[2]), (idx[("in", 3)], w22[3]),
              (idx[("pre", 6)], w22[4]), (idx[("post", 3)], w23[0]), (idx[("in", 8)], w23[1]), (idx[("pre", 10)], w23[2]),
              (idx[("pre", 14)], w23[3]), (idx[("pre", 13)], w23[4]), (len(tour) - 1, end(23, 0.2))])

# Replays (lines 25 to 27): each number lands on its moment
passes = []
for line, kind, order, start in ((25, "pre", PRE, "preorder"), (26, "in", IN, "inorder"), (27, "post", POST, "postorder")):
    names = [NAMES[v].capitalize() if k == 0 else NAMES[v] for k, v in enumerate(order)]
    ws = words(line, names, start)
    ks = [(idx[(kind, v)], w) for v, w in zip(order, ws)]
    if ks[-1][0] != len(tour) - 1:
        ks.append((len(tour) - 1, end(line, 0.25)))
    if ks[0][0] != 0:
        ks.insert(0, (0, [line, max(0.0, ws[0][1] - 0.6)]))
    passes.append({"kind": kind, "keys": keys(ks), "marks": [[idx[(kind, v)], w] for v, w in zip(order, ws)]})

walk_json = {
    "toks": toks, "tour": tour,
    "anatomy": {
        "first": 5, "last": 15,
        "drop": at(5, "Seven"), "rods": at(5, "rods"),
        "root": at(6, "root"), "reach": at(6, "every block"),
        "parent": at(7, "parent"), "children": at(7, "two children"),
        "binary": at(8, "binary"), "lr": at(8, "a left one"),
        "rule": at(9, "golden rule"), "loop": at(9, "no rod"), "loops": at(9, "loops"),
        "path": at(10, "exactly one"),
        "leaves": words(11, ["One", "six", "thirteen"]),
        "none": at(12, "None"), "mark": at(13, "barrier"), "remember": at(13, "Remember"),
        "levels": at(14, "Each row"), "depth": at(14, "depth of"), "fourteen": at(14, "Fourteen"),
        "height": at(15, "height"), "three": at(15, "three"),
    },
    "dfs": {
        "first": 20, "last": 28, "splits": at(20, "splits"), "lead": at(21, "lead"),
        "pass1": first, "path": at(24, "Look at the path"), "moments": words(24, ["down", "underneath", "back up"]),
        "passes": passes, "pre_note": at(28, "Preorder"), "post_note": at(28, "Postorder"),
    },
    "bst": {
        "first": 35, "last": 42,
        "rule": at(35, "one rule"), "left": at(35, "smaller"), "right": at(35, "bigger"), "name": at(36, "binary search"),
        "hopper": at(37, "hopper"), "drop": at(37, "Drop"), "goleft": at(38, "so it goes left"), "dark": at(38, "goes dark"),
        "goright": at(39, "so it goes right"), "found": at(39, "there it is"), "half": at(40, "half"),
        "sorted": at(41, "sorted"), "lands": at(41, "lands"), "stair": at(42, "staircase"), "costs": at(42, "search costs"),
    },
}
json.dump(walk_json, open('walk.json', 'w'), indent=1)
print(len(toks), "tokens,", len(tour), "tour stops")
