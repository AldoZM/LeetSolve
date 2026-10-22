# Writes walk.json: the string, what happens at each character and when (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

S = "  -042a7"
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0, nth=0):
    # [line, seconds] where the nth `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
        assert k >= 0, (i, phrase, nth)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


def atoi(s):
    # The same parse as the video's code, recording every step
    steps, i, n, sign, res = [], 0, len(s), 1, 0
    while i < n and s[i] == ' ':
        steps.append({"i": i, "kind": "space"})
        i += 1
    if i < n and s[i] in '+-':
        sign = -1 if s[i] == '-' else 1
        steps.append({"i": i, "kind": "sign", "sign": sign})
        i += 1
    while i < n and s[i].isdigit():
        d = int(s[i])
        assert res <= (2 ** 31 - 1 - d) // 10
        res = res * 10 + d
        steps.append({"i": i, "kind": "digit", "d": d, "res": res})
        i += 1
    if i < n:
        steps.append({"i": i, "kind": "stop"})
    return steps, sign * res


steps, answer = atoi(S)
assert answer == -42
# What each character is drawn as: stone for spaces, redstone for the sign, iron for digits, planks for letters
looks = ["stone" if c == ' ' else "redstone_ore" if c in '+-' else "iron_ore" if c.isdigit() else "planks" for c in S]
TIMES = [
    {"visit": at(10, "The pointer"), "skip": at(10, "skips")},
    {"visit": at(10, "both"), "skip": at(10, "spaces.")},
    {"visit": at(10, "finds a minus"), "sign_t": at(10, "negative")},
    {"visit": at(11, "Zero."), "push": at(11, "The result stays")},
    {"visit": at(11, "Four."), "push": at(11, "is four")},
    {"visit": at(12, "Two."), "push": at(12, "forty two")},
    {"visit": at(13, "the letter a"), "stop_t": at(13, "stops right")},
]
for st, tm in zip(steps, TIMES):
    st.update(tm)

walk = {
    "first": 9, "last": 14, "s": S, "looks": looks, "steps": steps, "answer": answer,
    "row_in": at(9, "Our string"),
    # Each character lights up as the narration names it
    "names": [at(9, "two spaces"), at(9, "two spaces", 0.25), at(9, "a minus"), at(9, "zero"), at(9, "four"),
              at(9, "two,"), at(9, "the letter a"), at(9, "a seven")],
    "seven": at(13, "The seven"), "toast": at(14, "Advancement", 0.05), "apply": at(14, "Apply the sign"),
    "answer_t": at(14, "minus forty two"),
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for s in steps:
    print(s)
