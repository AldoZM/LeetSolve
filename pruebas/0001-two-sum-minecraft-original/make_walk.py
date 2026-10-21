# Writes walk.json: the Two Sum pass and its event times (shared by scenes.py and three/walk.html)
# Event times are anchored to phrases of the narration, assuming a roughly even speaking rate inside a line.
import json

NUMS = [5, 12, 1, 14, 8, 15]
TARGET = 23
ORES = ["coal", "iron", "redstone", "lapis", "gold", "diamond"]
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0):
    # [line, seconds] where `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


def spread(visit, end):
    # Misses go fast: need, ask, result and store are spread between this visit and the next one
    span = end - visit[1]
    return tuple([visit[0], round(visit[1] + f * span, 3)] for f in (0.0, 0.15, 0.38, 0.58, 0.78))


VISITS = [at(11, "Five"), at(12, "Twelve"), at(12, "One"), at(13, "Fourteen"), at(13, "Eight")]
ENDS = [SUBS[11]['duration_s'], VISITS[2][1], SUBS[12]['duration_s'], VISITS[4][1], SUBS[13]['duration_s']]
# Per block: (visit, need, ask, result, store)
PLAN = [spread(v, e) for v, e in zip(VISITS, ENDS)]
PLAN.append((at(14, "fifteen", -0.2), at(14, "needs"), at(14, "and eight"), at(14, "already"), None))

seen, steps = {}, []
for i, x in enumerate(NUMS):
    need = TARGET - x
    visit, need_t, ask, result, store = PLAN[i]
    st = {"i": i, "x": x, "need": need, "visit": visit, "need_t": need_t, "ask": ask}
    if need in seen:
        st.update({"hit": result, "found": seen[need]})
        steps.append(st)
        break
    st.update({"miss": result, "store": store})
    seen[x] = i
    steps.append(st)

walk = {
    "first": 9, "last": 15, "nums": NUMS, "target": TARGET, "ores": ORES,
    "intro_row": at(9, "walk"), "chest_in": at(9, "with a chest"), "hashmap": at(9, "That chest"),
    "demo_cursor": at(10, "At each"), "demo_ask": at(10, "Is my"),
    "index_four": at(14, "at index"), "toast": at(15, "Advancement", 0.05), "answer": at(15, "The answer"),
    "steps": steps,
}
json.dump(walk, open('walk.json', 'w'), indent=1)
for s in steps:
    print(s)
