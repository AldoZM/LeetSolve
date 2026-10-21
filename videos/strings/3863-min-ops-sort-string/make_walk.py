# Writes walk.json: event timings for Scene5_Walk (3863 Minimum Operations to Sort a String)
import json

SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0):
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase, text)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


walk = {
    "first": 9,
    "last": 15,
    "chars": ["d", "b", "c", "a"],
    "ores": ["diamond", "lapis", "coal", "iron"],
    "target": ["a", "b", "c", "d"],
    "events": {
        "intro_row": at(9, "Our string"),
        "checks_in": at(9, "checks"),
        "check_sorted": at(10, "already sorted"),
        "check_len2": at(10, "just two"),
        "check_min_first": at(11, "Is a"),
        "check_max_last": at(11, "Is d"),
        "check_min_prefix": at(12, "Does a appear"),
        "check_max_suffix": at(12, "Does d appear"),
        "stuck": at(13, "Both letters"),
        "answer_three": at(13, "answer is three"),
        "watch": at(13, "watch"),
        "op1_select": at(14, "Sort d b c"),
        "op1_sort": at(14, "into b c d"),
        "op2_select": at(14, "Then sort c d a"),
        "op2_sort": at(14, "into a c d"),
        "op3_select": at(14, "Then sort b a c"),
        "op3_sort": at(14, "into a b c"),
        "sorted_done": at(14, "Sorted!"),
        "toast": at(15, "Advancement", 0.05),
        "answer": at(15, "Three operations"),
    }
}

json.dump(walk, open('walk.json', 'w'), indent=2)
print("walk.json successfully written.")
for k, v in walk["events"].items():
    print(f"  {k}: {v}")
