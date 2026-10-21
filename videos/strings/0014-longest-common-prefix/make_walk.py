# Writes walk.json: the vertical scan of Longest Common Prefix and its event times (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

WORDS = ["diamond", "diorite", "dirt"]
TEX = ["diamond_ore", "diorite", "dirt"]  # each word is built from the block it names
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0):
    # [line, seconds] where `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


# Per column: (column shown, one time per word read, verdict)
PLAN = [
    (at(10, "Column"), [at(10, "Diamond"), at(10, "diorite"), at(10, "dirt has")], at(10, "All match")),
    (at(11, "Column"), [at(11, "I,"), at(11, "i and"), at(11, "and i")], at(11, "Still")),
    (at(12, "Column"), [at(12, "Diamond"), at(12, "diorite")], at(12, "They differ")),
]

cols, prefix = [], ""
for c, (show, reads, verdict) in enumerate(PLAN):
    ch = WORDS[0][c]
    match = all(c < len(w) and w[c] == ch for w in WORDS)
    cols.append({"c": c, "ch": ch, "match": match, "show": show, "reads": reads, "verdict": verdict,
                 "letters": [w[c] for w in WORDS[:len(reads)]]})
    if not match:
        break
    prefix += ch
assert prefix == "di"

walk = {
    "first": 9, "last": 15, "words": WORDS, "tex": TEX, "prefix": prefix,
    "intro_rows": at(9, "Each word"), "scan": at(9, "We scan"), "grows": at(11, "The prefix grows"),
    "stop": at(13, "We stop"), "unread": at(13, "The rest"), "ret": at(14, "We return"),
    "toast": at(15, "Advancement", 0.05), "answer": at(15, "The longest"),
    "cols": cols,
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for c in cols:
    print(c)
