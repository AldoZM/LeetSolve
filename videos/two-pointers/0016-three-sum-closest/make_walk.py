# Writes walk.json: the 3Sum Closest sweep and its event times (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

RAW = [4, -5, 7, 2, 3]          # the row as given (Problem and Brute scenes)
NUMS = sorted(RAW)              # [-5, 2, 3, 4, 7]
TARGET = 10
ORES = ["coal", "iron", "redstone", "lapis", "diamond"]   # one ore per sorted value
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where the nth `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
        assert k >= 0, (i, phrase, nth)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


def sweep(nums, target):
    # The real algorithm; every evaluated (i, l, r) is one step
    best, out = nums[0] + nums[1] + nums[2], []
    for i in range(len(nums) - 2):
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            better = abs(s - target) < abs(best - target)
            if better:
                best = s
            move = "L" if s < target else "R"
            out.append({"i": i, "l": l, "r": r, "sum": s, "better": better, "best": best, "move": move})
            if s < target:
                l += 1
            else:
                r -= 1
    return best, out


BEST, steps = sweep(NUMS, TARGET)
assert BEST == 9
assert [(s["i"], s["l"], s["r"], s["sum"], s["better"], s["move"]) for s in steps] == [
    (0, 1, 4, 4, True, "L"), (0, 2, 4, 5, True, "L"), (0, 3, 4, 6, True, "L"),
    (1, 2, 4, 12, True, "R"), (1, 2, 3, 9, True, "L"), (2, 3, 4, 14, False, "R")]

# Per step: when it is fixed/visited, when its sum is said, when best is judged, when the pointer moves (None = not shown;
# the next "Fix" resets the pointers)
PLAN = [
    {"visit": at(10, "Left on two"), "fix": at(10, "Fix minus five"), "sum_t": at(10, "The sum is four"),
     "judge": at(10, "our best"), "move_t": at(10, "Too small")},
    # "Five, then six" is quick: the sum and the new best land together, then left slides on
    {"visit": at(11, "Five", 0.0), "sum_t": at(11, "Five", 0.0), "judge": at(11, "Five", 0.18), "move_t": at(11, "then")},
    {"visit": at(11, "six", 0.0), "sum_t": at(11, "six", 0.05), "judge": at(11, "Each one"), "move_t": at(11, "still too small")},
    {"visit": at(12, "Fix two"), "fix": at(12, "Fix two"), "sum_t": at(12, "is twelve"), "judge": at(12, "Only two away"),
     "move_t": at(12, "Too big")},
    {"visit": at(13, "Two plus", 0.0), "sum_t": at(13, "is nine"), "judge": at(13, "Just one away"), "move_t": None},
    {"visit": at(14, "Fix three"), "fix": at(14, "Fix three"), "sum_t": at(14, "make fourteen"), "judge": at(14, "That's four away"),
     "move_t": None},
]
for s, p in zip(steps, PLAN):
    s.update(p)

walk = {
    "first": 9, "last": 15, "raw": RAW, "nums": NUMS, "target": TARGET, "ores": ORES, "answer": BEST,
    "row_in": at(9, "Sorted"),
    "names": [at(9, "minus five"), at(9, "two"), at(9, "three"), at(9, "four"), at(9, "seven")],
    "target_t": at(9, "The target"),
    "stays": at(14, "so nine stays"),
    "toast": at(15, "Advancement", 0.05), "answer_t": at(15, "The closest"),
    "steps": steps,
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for s in steps:
    print(s)
