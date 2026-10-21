# Writes walk.json: the tree, its preorder tokens and the time of every save/load event (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']

# Tree [5, 8, 2, null, null, 7]: name -> value, children (left, right)
TREE = {"a": (5, "b", "c"), "b": (8, None, None), "c": (2, "d", None), "d": (7, None, None)}
ORE = {5: "gold", 8: "diamond", 2: "redstone", 7: "lapis"}
SPREAD = [1.8, 0.9, 0.6]  # horizontal distance from a node to its children, per level


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where the nth `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
        assert k >= 0, (i, phrase, nth)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


def serialize(name, x, lvl, parent, side, out):
    # Preorder with "#" for every empty child; each token keeps its spot in the drawing
    tok = {"x": x, "lvl": lvl, "parent": parent, "side": side}
    out.append(tok)
    if name is None:
        tok["tok"] = "#"
        return
    value, left, right = TREE[name]
    tok.update({"tok": str(value), "value": value, "ore": ORE[value]})
    me = len(out) - 1
    serialize(left, x - SPREAD[lvl], lvl + 1, me, "L", out)
    serialize(right, x + SPREAD[lvl], lvl + 1, me, "R", out)


tokens = []
serialize("a", 0.0, 0, None, None, tokens)
text = ",".join(t["tok"] for t in tokens)
assert text == "5,8,#,#,2,7,#,#,#", text

SAVE = [at(10, "Five"), at(10, "eight"), at(10, "pair"), at(10, "barriers"),
        at(11, "two"), at(11, "seven"), at(11, "another"), at(11, "pair"), at(12, "One last")]
SAY = [at(13, "Five"), at(13, "eight"), at(13, "hash"), at(13, "hash", nth=1), at(13, "two"), at(13, "seven"),
       at(13, "hash", nth=2), at(13, "hash", nth=3), at(13, "hash", nth=4)]
LOAD = [at(15, "Five"), at(15, "Eight"), at(15, "pair"), at(15, "barriers"),
        at(16, "Two"), at(16, "seven"), at(16, "last"), at(16, "barriers"), at(16, "every")]
for k, t in enumerate(tokens):
    t.update({"save": SAVE[k], "say": SAY[k], "load": LOAD[k]})

walk = {
    "first": 9, "last": 17, "text": text, "tokens": tokens, "ores": sorted(set(ORE.values())),
    "inv_in": at(9, "save"), "cursor": at(9, "walk"), "slot_demo": at(9, "each step"),
    "saved": at(12, "save is done"), "clear": at(14, "clear"), "load": at(14, "load"), "read_demo": at(14, "reading"),
    "climb": at(15, "climb"), "toast": at(17, "Advancement", 0.05), "back": at(17, "The tree"),
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for t in tokens:
    print(t["tok"], t["save"], t["say"], t["load"])
