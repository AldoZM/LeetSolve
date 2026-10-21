# Writes walk.json: pop, check and push times for both runs (shared by script.py and three/walk.html)
import json

LIMIT = 2**31 - 1


def run(x):
    ops, rev = [], 0
    while x:
        x, d = divmod(x, 10)
        overflow = rev > (LIMIT - d) // 10
        ops.append({"d": d, "x_after": x, "rev_before": rev, "overflow": overflow,
                    "rev_after": None if overflow else rev * 10 + d})
        if overflow:
            break
        rev = rev * 10 + d
    return ops


first = run(1463)
for op, t in zip(first, [[8, 0.3], [9, 0.3], [10, 0.3], [10, 2.6]]):
    op["pop"] = t
    op["check"] = [t[0], round(t[1] + 0.4, 3)]
    op["push"] = [t[0], round(t[1] + 0.8, 3)]

second = run(1534236469)
for k, op in enumerate(second):
    if not op["overflow"]:
        u = round(3.0 + 0.48 * k, 3)
        op["pop"], op["check"], op["push"] = [11, u], [11, round(u + 0.2, 3)], [11, round(u + 0.35, 3)]
    else:
        op["pop"], op["check"], op["stop"] = [12, 1.0], [12, 2.2], [12, 4.0]

walk = {"first": 7, "last": 12, "limit": LIMIT, "x1": 1463, "x2": 1534236469, "run1": first, "run2": second,
        "zero": [7, 2.0], "done1": [10, 4.4], "reset": [11, 0.1], "limit_in": [11, 2.2]}
json.dump(walk, open("walk.json", "w"), indent=1)
print([(o["d"], o["rev_after"]) for o in first], [(o["d"], o["rev_after"], o["overflow"]) for o in second])
