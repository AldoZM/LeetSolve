# Writes walk.json: the half-reversal of 12321 with the time of every event (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

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
    # The real algorithm; every pass of the loop is one step
    steps, half = [], 0
    while x > half:
        d = x % 10
        steps.append({"x_before": x, "half_before": half, "d": d, "x_after": x // 10, "half_after": half * 10 + d})
        half = half * 10 + d
        x //= 10
    return steps, x, half


X = 12321
steps, x_end, half_end = run(X)
assert [s["d"] for s in steps] == [1, 2, 3] and (x_end, half_end) == (12, 123)
assert x_end == half_end // 10  # odd length: drop the middle digit
PLAN = [(at(10, "Pop one"), at(10, "x is"), at(10, "the half is")),
        (at(11, "Pop two"), at(11, "x is"), at(11, "the half is")),
        (at(12, "Pop three"), at(12, "x is"), at(12, "the half is"))]
for s, (pop, xs, hs) in zip(steps, PLAN):
    s.update({"pop": pop, "x_t": xs, "half_t": hs})

walk = {
    "first": 9, "last": 14, "x": X, "steps": steps, "x_end": x_end, "half_end": half_end,
    "row_in": at(9, "one two three two one"), "zero": at(9, "starts at zero"),
    "stop": at(12, "Now the half"), "stop_t": at(12, "so we stop"),
    "odd": at(13, "The length is odd"), "middle": at(13, "the middle digit"), "drop": at(13, "Divide it by ten"),
    "equal": at(14, "Twelve equals"), "toast": at(14, "Advancement", 0.05), "yes": at(14, "palindrome"),
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for s in steps:
    print(s)
print({k: v for k, v in walk.items() if k not in ("steps",)})
