# Writes walk.json: the 4Sum search and its event times (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

RAW = [1, 0, -1, 0, -2, 2]      # the row as given (Problem and Brute scenes)
NUMS = sorted(RAW)              # [-2, -1, 0, 0, 1, 2]
TARGET = 0
ORE = {-2: "coal", -1: "iron", 0: "redstone", 1: "lapis", 2: "diamond"}   # equal values share their ore
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where the nth `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
        assert k >= 0, (i, phrase, nth)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


def search(nums, target):
    # The real algorithm; records every evaluated (i, j, l, r) and every skipped j
    n, out, trace = len(nums), [], []
    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i - 1]:
            trace.append({"kind": "skip_i", "i": i})
            continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j - 1]:
                trace.append({"kind": "skip_j", "i": i, "j": j})
                continue
            l, r = j + 1, n - 1
            while l < r:
                s = nums[i] + nums[j] + nums[l] + nums[r]
                e = {"kind": "check", "i": i, "j": j, "l": l, "r": r, "sum": s}
                trace.append(e)
                if s < target:
                    e["verdict"] = "small"
                    l += 1
                elif s > target:
                    e["verdict"] = "big"
                    r -= 1
                else:
                    e["verdict"] = "found"
                    out.append([nums[i], nums[j], nums[l], nums[r]])
                    l, r = l + 1, r - 1
                    while l < r and nums[l] == nums[l - 1]:
                        l += 1
    return out, trace


GROUPS, trace = search(NUMS, TARGET)
assert GROUPS == [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
short = [(e["kind"], e.get("i"), e.get("j"), e.get("l"), e.get("r"), e.get("sum")) for e in trace]
assert short == [("check", 0, 1, 2, 5, -1), ("check", 0, 1, 3, 5, -1), ("check", 0, 1, 4, 5, 0), ("check", 0, 2, 3, 5, 0),
                 ("skip_j", 0, 3, None, None, None), ("check", 1, 2, 3, 5, 1), ("check", 1, 2, 3, 4, 0),
                 ("skip_j", 1, 3, None, None, None), ("check", 2, 3, 4, 5, 3)], short

# Timing per shown event. fix: the two fixed blocks (and fresh pointers) arrive; sum_t: the total is said;
# found / move_t: the verdict. The second skip_j (i = 1) is not narrated, so it is not shown.
checks = [e for e in trace if e["kind"] == "check"]
PLAN = [
    {"fix": at(9, "Fix minus two"), "ptrs": at(9, "Pointers on"), "sum_t": at(9, "The total"), "move_t": at(10, "Left moves")},
    {"sum_t": at(10, "still minus one"), "move_t": at(10, "Then to the one")},
    {"sum_t": at(10, "Total zero"), "found": at(10, "first group")},
    {"fix": at(11, "Next, minus two"), "sum_t": at(11, "The other zero"), "found": at(11, "Second group")},
    {"fix": at(13, "Now minus one"), "sum_t": at(13, "Zero and two make one"), "move_t": at(13, "so right moves left")},
    {"sum_t": at(13, "Zero and one."), "found": at(13, "Third group")},
    {"fix": at(14, "Last"), "sum_t": at(14, "make three"), "move_t": at(14, "Too big")},
]
assert len(PLAN) == len(checks)
for e, p in zip(checks, PLAN):
    e.update(p)
skip = next(e for e in trace if e["kind"] == "skip_j")
skip.update({"fix": at(12, "Minus two with"), "skip_t": at(12, "so we skip")})

walk = {
    "first": 8, "last": 15, "raw": RAW, "nums": NUMS, "target": TARGET, "ores": [ORE[v] for v in NUMS], "groups": GROUPS,
    "row_in": at(8, "Sorted"),
    "names": [at(8, "minus two"), at(8, "minus one"), at(8, "zero"), at(8, "zero", nth=1), at(8, "one, two"), at(8, "two.")],
    "target_t": at(8, "The target"),
    "ends": at(14, "the search ends"),
    "toast": at(15, "Advancement", 0.05), "answer_t": at(15, "Three groups"),
    "checks": checks, "skip": skip,
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for e in checks + [skip]:
    print(e)
