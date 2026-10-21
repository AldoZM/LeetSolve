# Writes walk.json: the bracket-pairs pass and its event times (shared by scenes.py and three/mundo.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

S = "(a)and(b)make(c)"
KNOWLEDGE = [["a", "iron"], ["b", "gold"], ["d", "coal"]]
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0):
    # [line, seconds] where `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


# The row: brackets become blocks, plain text between them becomes floating words
pieces = []
for k, part in enumerate(S.split("(")):
    if k == 0:
        if part:
            pieces.append({"kind": "word", "text": part})
        continue
    key, rest = part.split(")")
    pieces.append({"kind": "key", "text": key})
    if rest:
        pieces.append({"kind": "word", "text": rest})

# Per bracket: (visit, key sign, ask the chest, hit or miss, value written, cursor on the word, plain text copied).
# Line 13 is short, so the cursor leaves for bracket b at the end of line 12
PLAN = [
    (at(11, "Key A"), at(11, "A."), at(11, "The chest"), at(11, "has it"), at(11, "Iron"), at(12, '"and"'), at(12, "copied")),
    (at(12, "as it is", 0.1), [13, 0.05], [13, 0.22], [13, 0.4], at(13, "Gold"), at(13, "Then the word"), at(13, '"make"')),
    (at(14, "Key C"), at(14, "C."), at(14, "It's not"), at(14, "not in"), at(14, "question"), None, None),
]

chest = dict(KNOWLEDGE)
steps, out = [], ""
keys = [k for k, p in enumerate(pieces) if p["kind"] == "key"]
for n, pi in enumerate(keys):
    key = pieces[pi]["text"]
    nxt = pieces[pi + 1] if pi + 1 < len(pieces) and pieces[pi + 1]["kind"] == "word" else None
    visit, key_t, ask, result, write, word_t, copy = PLAN[n]
    value = chest.get(key, "?")
    out += value
    st = {"piece": pi, "key": key, "value": value, "out_value": out, "visit": visit, "key_t": key_t, "ask": ask,
          "write": write}
    st["hit" if key in chest else "miss"] = result
    if nxt:
        out += nxt["text"]
        st.update({"word": pi + 1, "rest": nxt["text"], "word_t": word_t, "copy": copy, "out_rest": out})
    steps.append(st)

walk = {
    "first": 9, "last": 15, "s": S, "knowledge": KNOWLEDGE, "pieces": pieces, "answer": out,
    "intro_row": at(9, "Here"), "brackets": at(9, "Three brackets"), "words": at(9, "plain words"),
    "chest_in": at(10, "The chest"), "demo_key": at(10, "we read the key"), "demo_ask": at(10, "ask the chest"),
    "toast": at(15, "Advancement", 0.05), "answer_t": at(15, "Iron and gold"),
    "steps": steps,
}
json.dump(walk, open('walk.json', 'w'), indent=1)
print(pieces)
for s in steps:
    print(s)
print(out)
