# Writes walk.json: pop, check and push times for both runs (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

LIMIT = 2 ** 31 - 1
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where the nth `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
        assert k >= 0, (i, phrase, nth)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


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


def to_abs(spec):
    return sum(s['duration_s'] for s in SUBS[:spec[0]]) + spec[1]


def to_spec(t):
    # Absolute seconds back to [line, seconds into it]
    for i, s in enumerate(SUBS):
        if t < s['start_s'] + s['duration_s']:
            return [i, round(t - s['start_s'], 3)]
    return [len(SUBS) - 1, SUBS[-1]['duration_s']]


first = run(1463)
PLAN1 = [(at(8, "Pop three"), at(8, "push it")), (at(9, "Pop six"), at(9, "thirty six")),
         (at(10, "Pop four"), at(10, "three hundred")), (at(10, "Pop one"), at(10, "three thousand"))]
for op, (pop, push) in zip(first, PLAN1):
    op.update({"pop": pop, "check": [pop[0], round(pop[1] + 0.35, 3)], "push": push})

second = run(1534236469)
assert second[-1]["overflow"] and len(second) == 10
# Nine quick pushes, from "The reverse keeps growing" until "With nine digits pushed"
t0, t1 = to_abs(at(11, "The reverse")), to_abs(at(12, "pushed"))
for k, op in enumerate(second[:9]):
    u = t0 + (t1 - t0) * k / 9
    op.update({"pop": to_spec(u), "check": to_spec(u + 0.12), "push": to_spec(u + 0.26)})
second[9].update({"pop": at(12, "one more"), "check": at(12, "would pass"), "stop": at(12, "So we stop"),
                  "zero": at(12, "return zero")})

walk = {
    "first": 7, "last": 13, "limit": LIMIT, "x1": 1463, "x2": 1534236469, "run1": first, "run2": second,
    "row1_in": at(7, "reverse one"), "zero": at(7, "starts at zero"), "reset": at(11, "Now"), "row2_in": at(11, "One five"),
    "growing": at(11, "toward the limit"), "toast": at(13, "Advancement", 0.05), "caught": at(13, "caught"),
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for o in first + second:
    print(o)
