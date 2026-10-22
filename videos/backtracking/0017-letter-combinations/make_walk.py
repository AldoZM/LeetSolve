# Writes walk.json: the letter tree of digits = "23" and the backtracking events with their times
# (shared by scenes.py and three/mundo.html).
# Event times are anchored to phrases of the narration. Inside a line the speaking rate is taken as even between
# anchors measured on voiceover.mp3 (speech start/end of every line, and the pauses of the walk lines).
import json

SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']

DIGITS = "23"
KEYS = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}

# Speech start and end (seconds into each line), measured with an energy threshold of -38 dB
SPEECH = [[0.33, 5.47], [0.33, 4.6], [0.31, 6.23], [0.31, 3.41], [0.31, 6.17], [0.31, 4.97], [0.3, 6.58], [0.31, 3.43],
          [0.31, 6.1], [0.3, 3.77], [0.3, 3.91], [0.33, 3.3], [0.33, 2.41], [0.31, 3.24], [0.32, 5.91], [0.31, 4.46],
          [0.32, 3.48], [0.34, 3.47]]
# Where a phrase starts, measured on the pauses of the walk lines (seconds into the line)
ANCHORS = {
    # (a pause starts where the punctuation is, the next phrase starts after the pause)
    8: [(". Digit two", 2.14), ("Digit two", 2.68), (", b and", 3.58), ("b and", 3.63), (". Digit three", 4.48),
        ("Digit three", 4.56), (", e and", 5.34), ("e and f", 5.58)],
    9: [("Then add", 0.64), ("A d is", 1.32), (". Save", 2.3), ("Save it", 2.66), (", and", 3.1), ("and step", 3.18)],
    10: [(", then", 1.22), ("then for", 1.56), (". A e", 2.3), ("A e and", 2.32), ("go into", 2.9)],
    11: [(". Now", 1.42), ("Now b", 1.8), (", with", 2.36), ("with d", 2.44), (", e and", 2.76), ("e and f", 2.84)],
    12: [(", with", 0.8), ("with d", 0.9), (", e and", 1.42), ("e and f", 1.56)],
    13: [(". Nine", 1.16), ("Nine words", 1.55)],
}


def char_time(i, k):
    # Seconds into line i where character k is spoken: linear between the anchors of that line
    text = SUBS[i]['text']
    pts = [(0, SPEECH[i][0])] + [(text.index(p), t) for p, t in ANCHORS.get(i, [])] + [(len(text), SPEECH[i][1])]
    pts.sort()
    for (k0, t0), (k1, t1) in zip(pts, pts[1:]):
        if k0 <= k <= k1:
            return t0 + (t1 - t0) * (k - k0) / max(k1 - k0, 1)
    return SPEECH[i][1]


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where the nth `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
        assert k >= 0, (i, phrase, nth)
    return [i, round(min(dur - 0.1, max(0.0, char_time(i, k) + shift)), 3)]


def plus(spec, dt):
    return [spec[0], round(spec[1] + dt, 3)]


# The tree: root (the digits), level 1 = letters of digit 2, level 2 = letters of digit 3 under each of them.
# x is in units of the block spacing: leaves at -4..4, level 1 at -3, 0, 3
nodes = [{"label": DIGITS, "ore": "stone", "lvl": 0, "parent": None, "x": 0, "path": ""}]
for a, ca in enumerate(KEYS[DIGITS[0]]):
    nodes.append({"label": ca, "ore": "gold", "lvl": 1, "parent": 0, "x": (a - 1) * 3, "path": ca})
for a, ca in enumerate(KEYS[DIGITS[0]]):
    for b, cb in enumerate(KEYS[DIGITS[1]]):
        nodes.append({"label": cb, "ore": "diamond", "lvl": 2, "parent": 1 + a, "x": (a - 1) * 3 + (b - 1), "path": ca + cb})
by_path = {n["path"]: i for i, n in enumerate(nodes)}

# The real recursion, recorded as push / save / pop
trace, out = [], []


def go(i, path):
    if i == len(DIGITS):
        out.append(path)
        trace.append(("save", path))
        return
    for ch in KEYS[DIGITS[i]]:
        trace.append(("push", path + ch))
        go(i + 1, path + ch)
        trace.append(("pop", path + ch))


go(0, "")
assert out == ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]

# When each step happens, in trace order (the narration names the letter as it is chosen)
TIMES = [
    at(9, "a."),                                                               # push a
    at(9, "d."), at(9, "Save it"), at(9, "step back"),                         # ad
    at(10, "e,", -0.15), at(10, "e,", 0.15), at(10, "then for", -0.12),        # ae
    at(10, "f.", -0.2), at(10, "f.", 0.1), at(11, "Back up"),                  # af
    at(11, "the first level"),                                                 # pop a
    at(11, "b,"),                                                              # push b
    at(11, "d,"), plus(at(11, "d,"), 0.08), at(11, "e and", -0.02),            # bd
    at(11, "e and"), plus(at(11, "e and"), 0.08), at(11, "f.", -0.02),         # be
    at(11, "f."), plus(at(11, "f."), 0.08), at(12, "Then c", -0.12),           # bf
    at(12, "Then c"),                                                          # pop b
    at(12, "c,"),                                                              # push c
    at(12, "d,"), plus(at(12, "d,"), 0.08), at(12, "e and", -0.02),            # cd
    at(12, "e and"), plus(at(12, "e and"), 0.08), at(12, "f again", -0.02),    # ce
    at(12, "f again"), plus(at(12, "f again"), 0.08), at(13, "Advancement", -0.3),  # cf
    at(13, "Advancement", -0.2),                                               # pop c
]
assert len(TIMES) == len(trace), (len(TIMES), len(trace))

events, slot = [], 0
for (kind, path), t in zip(trace, TIMES):
    e = {"kind": kind, "node": by_path[path], "path": path, "t": t}
    if kind == "save":
        e["slot"] = slot
        slot += 1
    events.append(e)
# Times must grow with the trace (each step after the one before)
flat = [SUBS[e["t"][0]]["start_s"] + e["t"][1] for e in events]
assert all(b > a for a, b in zip(flat, flat[1:])), flat

walk = {
    "first": 8, "last": 13, "digits": DIGITS, "keys": KEYS, "words": out, "nodes": nodes, "events": events,
    "speech": SPEECH,
    # Line 8: the chest, then each letter drops in as the voice names it
    "inv_in": at(8, "chest", -0.5), "root_in": [8, 0.15],
    "keys_bar": at(8, "Digit two"),
    "drop": {"a": at(8, "a,", -0.1), "b": at(8, "b and", -0.05), "c": at(8, "c.", -0.1),
             "d": at(8, "d,", -0.1), "e": at(8, "e and", -0.05), "f": at(8, "f.", -0.1)},
    "complete": at(9, "A d is", 0.15),
    "recap": [at(10, "A e"), at(10, "a f")],
    "toast": at(13, "Advancement", 0.05), "nine": at(13, "Nine words"), "full": at(13, "chest is full"),
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for e in events:
    print(e["kind"], e["path"], e["t"], e.get("slot", ""))
print({k: walk[k] for k in ("inv_in", "keys_bar", "drop", "complete", "recap", "toast", "nine", "full")})
