# Writes walk.json: the sort + two pointers pass of 3Sum and its event times (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

NUMS = [-1, 0, 1, 2, -1, -4]
ORE = {-4: "coal", -1: "iron", 0: "redstone", 1: "lapis", 2: "gold"}
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0):
    # [line, seconds] where `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


def spread(i, phrase, n, end_pad=0.5):
    # n moments evenly spread from `phrase` to the end of line i
    a = at(i, phrase)[1]
    b = SUBS[i]['duration_s'] - end_pad
    return [[i, round(a + (b - a) * k / max(n - 1, 1), 3)] for k in range(n)]


S = sorted(NUMS)
# Times of each sum checked, in order, and of the fixes
CHECKS = spread(10, "Every pair", 4) + [at(11, "Minus one, plus"), at(12, "Zero plus"), at(14, "One plus two")]
FIX = {0: at(10, "Fix"), 1: at(11, "Fix"), 2: at(13, "The next"), 3: at(14, "Fix")}

events, res, c = [], [], 0
for i in range(len(S) - 2):
    if i and S[i] == S[i - 1]:
        events.append({"kind": "skip", "i": i, "t": FIX[i]})
        continue
    events.append({"kind": "fix", "i": i, "t": FIX[i]})
    l, r = i + 1, len(S) - 1
    while l < r:
        s = S[i] + S[l] + S[r]
        verdict = "small" if s < 0 else "big" if s > 0 else "zero"
        events.append({"kind": "check", "i": i, "l": l, "r": r, "s": s, "verdict": verdict, "t": CHECKS[c]})
        c += 1
        if s < 0:
            l += 1
        elif s > 0:
            r -= 1
        else:
            res.append([S[i], S[l], S[r]])
            l, r = l + 1, r - 1
            while l < r and S[l] == S[l - 1]:
                l += 1
assert res == [[-1, -1, 2], [-1, 0, 1]] and c == len(CHECKS)
# The found triples are spoken at "Found one" / "Found another"
found_t = [at(11, "Found one"), at(12, "Found another")]
for e, t in zip([e for e in events if e["kind"] == "check" and e["verdict"] == "zero"], found_t):
    e["found"] = t

walk = {
    "first": 9, "last": 15, "nums": NUMS, "sorted": S, "ores": [ORE[v] for v in S], "res": res,
    "sort_t": at(9, "Sorted"), "step_in": at(12, "Both pointers"), "meet": at(14, "the pointers meet"),
    "toast": at(15, "Advancement", 0.05), "answer": at(15, "Two triples"),
    "events": events,
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for e in events:
    print(e)
