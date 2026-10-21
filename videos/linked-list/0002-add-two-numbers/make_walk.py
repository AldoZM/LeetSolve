# Writes walk.json: the column-by-column addition and its event times (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

L1 = [2, 4, 9]
L2 = [5, 6, 4, 9]
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where the nth `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
        assert k >= 0, (i, phrase, nth)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


# Per column: (visit, sum, place, carry or None)
PLAN = [
    (at(10, "First"), at(10, "is seven"), at(10, "is seven", 0.45), None),
    (at(11, "Next"), at(11, "is ten"), at(11, "place a zero"), at(11, "carry the one")),
    (at(12, "Then"), at(12, "is fourteen"), at(12, "Place a four"), at(12, "carry one")),
    (at(13, "The first"), at(13, "is ten"), at(13, "Zero"), at(13, "carry one")),
    (at(14, "Both"), at(14, "still hold"), at(14, "one final"), None),
]

steps, carry = [], 0
for k, (visit, sum_t, place, carry_t) in enumerate(PLAN):
    a = L1[k] if k < len(L1) else None
    b = L2[k] if k < len(L2) else None
    total = (a or 0) + (b or 0) + carry
    st = {"k": k, "a": a, "b": b, "cin": carry, "total": total, "digit": total % 10, "cout": total // 10,
          "visit": visit, "sum": sum_t, "place": place}
    if total // 10:
        st["carry"] = carry_t
    steps.append(st)
    carry = total // 10
assert [s["digit"] for s in steps] == [7, 0, 4, 0, 1]

walk = {
    "first": 9, "last": 15, "l1": L1, "l2": L2, "result": [s["digit"] for s in steps],
    "rows_in": at(9, "walk"), "cursor": at(9, "one block"), "hold": at(9, "holding"),
    "run_out": at(13, "run out"), "toast": at(15, "Advancement", 0.05),
    "read": [at(15, "Seven"), at(15, "zero"), at(15, "four"), at(15, "zero", nth=1), at(15, "one")],
    "number": at(15, "That's"),
    "steps": steps,
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for s in steps:
    print(s)
