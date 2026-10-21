# Writes walk.json: where each letter lands, when, and when the pointer turns (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

S, R = "PAYPALISHIRING", 3
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


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


# The first five letters follow the narration; the rest go quickly, and the last one lands on "last letter lands"
TIMES = {0: at(9, "P goes", 0.2), 1: at(9, "A in"), 2: at(9, "Y in"), 3: at(10, "P goes", 0.2), 4: at(10, "A reaches")}
for k in range(5, 13):
    TIMES[k] = [11, round(0.15 + (k - 5) * 0.45, 3)]
TIMES[13] = at(12, "lands")
TURNS = {2: at(9, "turns around"), 4: at(10, "turns down")}

letters, r, step = [], 0, 1
cycle = 2 * (R - 1)
for k, ch in enumerate(S):
    col = (k // cycle) * (R - 1) + (0 if k % cycle < R else k % cycle - (R - 1))
    e = {"k": k, "ch": ch, "row": r, "col": col, "t": TIMES[k]}
    turn = (r == R - 1) or (r == 0 and k > 0)
    if turn:
        e["turn"] = TURNS.get(k, plus(TIMES[k], 0.2))
    letters.append(e)
    if r == 0:
        step = 1
    elif r == R - 1:
        step = -1
    r += step

rows = ["".join(e["ch"] for e in letters if e["row"] == q) for q in range(R)]
assert "".join(rows) == "PAHNAPLSIIGYIR", rows
# Reading order after the join: row by row, left to right
order = [e["k"] for q in range(R) for e in letters if e["row"] == q]

walk = {
    "first": 8, "last": 13, "s": S, "rows": R, "letters": letters, "row_strings": rows, "read_order": order,
    "row_in": at(8, "run it"), "rows_in": at(8, "Three empty"), "pointer": at(8, "pointer starts"),
    "holds": at(12, "each row holds"), "toast": at(13, "Advancement", 0.05), "join": at(13, "Join"), "read": at(13, "we get"),
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for e in letters:
    print(e)
print(rows, order)
