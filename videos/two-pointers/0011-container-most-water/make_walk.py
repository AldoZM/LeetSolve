# Writes walk.json: the two-pointer pass of Container With Most Water and its event times
# (shared by scenes.py and three/mundo.html). Times are anchored to phrases of the narration.
import json

H = [2, 4, 1, 6, 3, 5, 3]
ORES = ["coal", "iron", "redstone", "lapis", "gold", "diamond", "emerald"]
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0):
    # [line, seconds] where `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


# Per step: (measure, area said, pointer moves)
PLAN = [
    (at(10, "Heights"), at(10, "Twelve"), at(10, "so it moves")),
    (at(11, "Four and three"), at(11, "Fifteen"), at(11, "Now the right")),
    (at(12, "Four and five"), at(12, "Sixteen"), at(12, "The left wall")),
    (at(13, "One and five"), at(13, "gives only"), at(13, "Six and five", -0.35)),
    (at(13, "Six and five"), at(13, "gives ten"), at(13, "The right wall")),
    (at(14, "Six and three"), at(14, "Just three"), at(14, "The pointers meet")),
]

steps, best = [], 0
l, r = 0, len(H) - 1
for measure, said, move in PLAN:
    h = min(H[l], H[r])
    area = h * (r - l)
    new = area > best
    best = max(best, area)
    side = "l" if H[l] < H[r] else "r"
    steps.append({"l": l, "r": r, "h": h, "area": area, "best": best, "new": new, "side": side,
                  "measure": measure, "said": said, "move": move})
    if side == "l":
        l += 1
    else:
        r -= 1
assert l == r and best == 16

walk = {
    "first": 9, "last": 15, "heights": H, "ores": ORES, "best": best, "best_pair": [1, 5],
    "intro": at(9, "Two pointers"), "measure_demo": at(9, "we measure"), "stop": at(14, "we stop"),
    "toast": at(15, "Advancement", 0.05), "answer": at(15, "The most water"),
    "steps": steps,
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for s in steps:
    print(s)
