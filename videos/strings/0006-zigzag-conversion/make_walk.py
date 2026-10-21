# Writes walk.json: when each letter is placed and when the pointer turns (shared by script.py and three/walk.html)
import json

S, R = "PAYPALISHIRING", 3

rows, r, step = [], 0, 1
for k, ch in enumerate(S):
    turn = (r == R - 1) or (r == 0 and k > 0)
    rows.append({"k": k, "ch": ch, "row": r, "turn": turn})
    if r == 0:
        step = 1
    elif r == R - 1:
        step = -1
    r += step

slow = {0: [8, 0.3], 1: [8, 1.6], 2: [8, 2.9], 3: [9, 0.3], 4: [9, 2.0]}
slow_turn = {2: [8, 4.6], 4: [9, 3.6]}
for k, e in enumerate(rows):
    if k in slow:
        e["t"] = slow[k]
    else:
        e["t"] = [10, round(0.15 + (k - 5) * 0.42, 3)]
    if e["turn"]:
        e["tturn"] = slow_turn.get(k, [e["t"][0], round(e["t"][1] + 0.3, 3)])

walk = {"first": 7, "last": 12, "s": S, "rows": R, "letters": rows,
        "glow": [[11, 1.2], [11, 2.0], [11, 2.8]], "join": [12, 0.6], "final": [12, 2.6]}
json.dump(walk, open("walk.json", "w"), indent=1)
print([(e["ch"], e["row"], e["turn"]) for e in rows])
