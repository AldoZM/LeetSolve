# Writes walk.json: the Permutation Sequence step-by-step math and event times
# Shared by scenes.py (Manim) and three/mundo.html (Three.js)
import json

SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']
NUMS = [1, 2, 3, 4]
ORES = ["coal", "iron", "gold", "diamond"]
ORE_MAP = dict(zip(NUMS, ORES))
N = 4
K = 9
K_0 = K - 1  # 8


def at(i, phrase, shift=0.0):
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, f"Phrase '{phrase}' not found in line {i}: '{text}'"
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


steps = [
    {
        "step": 0,
        "n_rem": 4,
        "k_in": 8,
        "fact": 6,
        "idx": 1,
        "picked_val": 2,
        "ore": "iron",
        "rem_list_before": [1, 2, 3, 4],
        "rem_list_after": [1, 3, 4],
        "calc_t": at(10, "Divide eight"),
        "quot_t": at(10, "Quotient is one"),
        "pick_t": at(11, "picks index one"),
        "store_t": at(11, "iron block"),
    },
    {
        "step": 1,
        "n_rem": 3,
        "k_in": 2,
        "fact": 2,
        "idx": 1,
        "picked_val": 3,
        "ore": "gold",
        "rem_list_before": [1, 3, 4],
        "rem_list_after": [1, 4],
        "show_rem_t": at(12, "Now with blocks"),
        "calc_t": at(12, "divide remainder two"),
        "quot_t": at(12, "two factorial"),
        "store_t": at(12, "Quotient one picks three!"),
    },
    {
        "step": 2,
        "n_rem": 2,
        "k_in": 0,
        "fact": 1,
        "idx": 0,
        "picked_val": 1,
        "ore": "coal",
        "rem_list_before": [1, 4],
        "rem_list_after": [4],
        "calc_t": at(13, "Remainder is zero"),
        "quot_t": at(13, "Divide by one factorial"),
        "store_t": at(13, "picking block one"),
    },
    {
        "step": 3,
        "n_rem": 1,
        "k_in": 0,
        "fact": 1,
        "idx": 0,
        "picked_val": 4,
        "ore": "diamond",
        "rem_list_before": [4],
        "rem_list_after": [],
        "pick_t": at(14, "Only block four"),
        "store_t": at(14, "final slot"),
    },
]

walk = {
    "first": 9,
    "last": 15,
    "n": N,
    "k": K,
    "k_0": K_0,
    "nums": NUMS,
    "ores": ORES,
    "result": [2, 3, 1, 4],
    "result_ores": ["iron", "gold", "coal", "diamond"],
    "result_str": "2314",
    "k_zero": at(9, "zero-based"),
    "chest_in": at(9, "Our chest"),
    "steps": steps,
    "toast": at(15, "Advancement", 0.05),
    "answer": at(15, "The ninth permutation"),
}

with open('walk.json', 'w', encoding='utf-8') as f:
    json.dump(walk, f, indent=2)

print("walk.json successfully generated!")
for s in steps:
    print(f"Step {s['step']}: k={s['k_in']} // {s['fact']} -> idx {s['idx']} (val {s['picked_val']} {s['ore']})")
