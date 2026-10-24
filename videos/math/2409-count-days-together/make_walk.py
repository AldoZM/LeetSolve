# Writes walk.json: the dates turned into days of the year and the overlap of the two stays
# (shared by scenes.py and three/mundo.html). Event times are anchored to phrases of the narration.
import json

DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
ALICE = ("10-28", "11-03")
BOB = ("10-30", "11-05")
# The row of days shown in the world: October 27 to November 5
ROW = [("10", d) for d in range(27, 32)] + [("11", d) for d in range(1, 6)]
ORE = {"10": "redstone", "11": "lapis"}
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']


def at(i, phrase, shift=0.0):
    # [line, seconds] where `phrase` starts being spoken in line i
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase)
    return [i, round(min(dur - 0.1, max(0.0, dur * k / len(text) + shift)), 3)]


def day(d):
    m, dd = int(d[:2]), int(d[3:])
    return sum(DAYS[:m - 1]) + dd


def slot(d):
    # Index in ROW of a "MM-DD" date
    return ROW.index((d[:2], int(d[3:])))


doy = [sum(DAYS[:int(m) - 1]) + dd for m, dd in ROW]
start, end = max(day(ALICE[0]), day(BOB[0])), min(day(ALICE[1]), day(BOB[1]))
answer = max(0, end - start + 1)
assert answer == 5

walk = {
    "first": 10, "last": 15, "row": [dd for _, dd in ROW], "months": [m for m, _ in ROW], "doy": doy,
    "ores": [ORE[m] for m, _ in ROW], "before_oct": sum(DAYS[:9]),
    "alice": [slot(d) for d in ALICE], "bob": [slot(d) for d in BOB],
    "alice_doy": [day(d) for d in ALICE], "bob_doy": [day(d) for d in BOB],
    "start": start, "end": end, "answer": answer,
    "months_t": at(10, "nine months"), "sum_t": at(10, "two hundred"),
    "alice_in": at(11, "Alice arrives"), "alice_in_doy": at(11, "three hundred one"),
    "alice_out": at(11, "leaves"), "alice_out_doy": at(11, "three hundred seven"),
    "bob_in": at(12, "Bob arrives"), "bob_in_doy": at(12, "three hundred three"),
    "bob_out": at(12, "leaves"), "bob_out_doy": at(12, "three hundred nine"),
    "start_t": at(13, "later arrival"), "end_t": at(13, "earlier departure"),
    "minus_t": at(14, "minus"), "count_t": at(14, "plus one"), "five_t": at(14, "is five"), "neg_t": at(14, "If that"),
    "toast": at(15, "Advancement", 0.05), "answer_t": at(15, "share five"),
}
json.dump(walk, open('walk.json', 'w'), indent=1)
print("doy", doy, "start", start, "end", end, "answer", answer, "alice", walk["alice"], "bob", walk["bob"])
