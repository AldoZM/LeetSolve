from manim import *
import math
import random
import json

FPS = 30
config.pixel_width, config.pixel_height = 1080, 1440
config.frame_width, config.frame_height = 9, 12
config.frame_rate = FPS

# Palette shared with the three.js scenes (three/lib/stage.js)
BG = "#0B0E1A"
PANEL = "#141B2F"
CODE_BG = "#11162A"
CYAN = "#22D3EE"
MAGENTA = "#F472B6"
YELLOW = "#FACC15"
GREEN = "#34D399"
RED = "#F87171"
VIOLET = "#A78BFA"
ORANGE = "#FB923C"
MUTED = "#64748B"
INK = "#E2E8F0"
ARROW = "#8291AD"

TOP_Y = 5.4

# Narration lines and their exact durations (from the TTS step)
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']
DUR = [x['duration_s'] for x in SUBS]


def T(s, size=36, color=INK, weight=BOLD):
    return Text(s, font="Segoe UI", weight=weight, font_size=size, color=color)


def M(s, size=36, color=INK):
    return Text(s, font="Consolas", weight=BOLD, font_size=size, color=color)


def glow(m, color, layers=8, max_w=26, max_op=0.30):
    # Stacked translucent strokes behind a shape fake a neon bloom
    g = VGroup()
    for k in range(layers):
        frac = (k + 1) / layers
        g.add(m.copy().set_fill(opacity=0).set_stroke(color, width=max_w * frac, opacity=max_op * (1 - frac) + 0.02))
    return g


def ring(m, color, width=8):
    # Light that travels around a shape's border without touching its fill
    return ShowPassingFlash(m.copy().set_fill(opacity=0).set_stroke(color, width=width), time_width=0.5)


def restyle(m, fn):
    # Animate the whole group while changing only part of it; animating just the box lets Manim draw it over the text
    return ApplyFunction(lambda x: (fn(x), x)[1], m)


def pill(text, color, size=24):
    label = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.2, width=label.width + 0.5, height=label.height + 0.3,
                           fill_color=color, fill_opacity=0.12, stroke_color=color, stroke_width=2)
    return VGroup(box, label.move_to(box))


def header(text, color):
    return pill(text, color, 22).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def corner_pill(text, color, size=26):
    return pill(text, color, size).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)


def tags_block(items, y=-3.7):
    # items: [(text, color), ...]; first two on one row, the rest below
    first = VGroup(*[pill(t, c, 26) for t, c in items[:2]]).arrange(RIGHT, buff=0.3)
    rest = VGroup(*[pill(t, c, 26) for t, c in items[2:]]).arrange(RIGHT, buff=0.3)
    return VGroup(first, rest).arrange(DOWN, buff=0.25).move_to([0, y, 0])


def dot_grid():
    return VGroup(*[Dot([x, y, 0], radius=0.016, color=MUTED, fill_opacity=0.35)
                    for x in np.arange(-4.2, 4.3, 0.6) for y in np.arange(-5.7, 5.8, 0.6)])


def gradient_title(lines, size=96, y=3.35, colors=(CYAN, VIOLET, MAGENTA)):
    title = VGroup(*[T(s, size) for s in lines]).arrange(DOWN, buff=0.08)
    title.set_color_by_gradient(*colors).move_to([0, y, 0])
    return title, glow(title, colors[1], layers=6, max_w=20, max_op=0.25)


class Tile(VGroup):
    """Rounded square holding one value; `box` and `num` are animated through restyle()."""

    def __init__(self, value, color, size=0.95, text_color=INK, **kwargs):
        super().__init__(**kwargs)
        self.box = RoundedRectangle(corner_radius=0.14 * size / 0.95, width=size, height=size, fill_color=PANEL,
                                    fill_opacity=1, stroke_color=color, stroke_width=3)
        self.num = M(str(value), int(38 * size / 0.95), text_color).move_to(self.box)
        self.add(self.box, self.num)


def tile_row(values, color, y, size=0.8, gap=0.12, x=0.0, text_color=INK):
    row = VGroup(*[Tile(v, color, size, text_color) for v in values]).arrange(RIGHT, buff=gap)
    row.move_to([x, y, 0])
    return row  # returned separately so the linter stub keeps the children


def index_labels(row, size=18, color=MUTED, buff=0.12, start=0):
    return VGroup(*[M(str(start + k), size, color).next_to(t, DOWN, buff=buff) for k, t in enumerate(row)])


def code_panel(src, y, width=8.4, max_h=None):
    code = Code(code_string=src, language="python", formatter_style="monokai", background="rectangle",
                background_config={"fill_color": CODE_BG, "stroke_color": VIOLET, "stroke_width": 2},
                paragraph_config={"font": "Consolas"})
    code.scale_to_fit_width(width)
    if max_h and code.height > max_h:
        code.scale_to_fit_height(max_h)
    return code.move_to([0, y, 0])


def line_bar(code, k0, k1=None, color=YELLOW):
    k1 = k0 if k1 is None else k1
    lines = code.code_lines
    step = abs(lines[1].get_y() - lines[0].get_y())
    top, bottom = lines[k0].get_y() + step / 2, lines[k1].get_y() - step / 2
    bar = Rectangle(width=code.background.width - 0.12, height=(top - bottom) * 0.97, fill_color=color, fill_opacity=0.16,
                    stroke_color=color, stroke_width=1.5)
    return bar.move_to([code.background.get_x(), (top + bottom) / 2, 0])


def big_o(tex, color, y, label, size=80):
    o = MathTex(tex, font_size=size, color=color).move_to([0, y, 0])
    lab = T(label, 30, MUTED).next_to(o, DOWN, buff=0.15)
    return o, lab, glow(o, color, layers=6, max_w=14, max_op=0.3)


class Base(Scene):
    scene_budget = 0.0
    scene_used = 0.0
    seg_begin = 0.0

    def setup(self):
        self.camera.background_color = BG
        self.add(dot_grid())

    # Manim renders whole frames; keep animations on frame boundaries so audio stays in sync
    def frames(self, t):
        return math.ceil(t * FPS - 1e-6) / FPS

    def seg(self, i):
        text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
        self.add_subcaption(text, duration=dur)
        self.seg_begin = self.scene_budget
        self.scene_budget += dur

    def beat(self, *anims, rt=1.0, **kwargs):
        rt = self.frames(rt)
        self.play(*anims, run_time=rt, **kwargs)
        self.scene_used += rt

    def hold(self, t):
        t = self.frames(t)
        self.wait(t)
        self.scene_used += t

    def until(self, u):
        # Wait until u seconds into the current narration segment
        gap = self.seg_begin + u - self.scene_used
        if gap > 1e-6:
            self.hold(gap)

    def close_seg(self):
        rest = self.scene_budget - self.scene_used
        if rest > 0:
            self.wait(rest)
            self.scene_used += rest

    def finish(self, *anims, rt=0.5):
        # Play so the animation ends right at the close of the current segment
        rt = self.frames(rt)
        self.until(self.scene_budget - self.seg_begin - rt - 1.0 / FPS)
        self.beat(*anims, rt=rt)

    def clear_all(self, rt=0.5):
        self.finish(FadeOut(Group(*self.mobjects[1:])), rt=rt)


def seg_time(first, spec):
    # [segment index, seconds into it] -> seconds since the start of segment `first`
    return sum(DUR[first:spec[0]]) + spec[1]


def walk_events(walk, kinds):
    # walk.json is shared with three/walk.html; each step lists [segment, seconds] per event kind
    ev = []
    for k, st in enumerate(walk["steps"]):
        for kind in kinds:
            if kind in st:
                ev.append((seg_time(walk["first"], st[kind]), kind, k))
    return sorted(ev, key=lambda e: e[0])


class Overlay(Base):
    """Transparent layer composited over a three.js clip (rendered with -t)."""

    def setup(self):
        pass

    def run_events(self, walk, events, handler, on_first=None, on_last=None):
        # Plays each narration segment of the walk, firing handler(kind, step) at the shared event times
        first, last = walk["first"], walk["last"]
        ei = 0
        for i in range(first, last + 1):
            self.seg(i)
            s0 = seg_time(first, [i, 0])
            if i == first and on_first:
                on_first()
            while ei < len(events) and events[ei][0] < s0 + DUR[i] - 0.05:
                t, kind, k = events[ei]
                ei += 1
                self.until(t - s0)
                handler(kind, k)
            if i == last and on_last:
                on_last()
            self.close_seg()

# ---------------------------------------------------------------- video-specific code below

A = [1, 3, 8, 9, 15]
B = [7, 11, 18, 19, 21, 25]
HALF = (len(A) + len(B) + 1) // 2
MERGED = sorted([(v, "A") for v in A] + [(v, "B") for v in B])
WALK = json.load(open('walk.json', encoding='utf-8'))

CODE = """def findMedianSortedArrays(A, B):
    if len(A) > len(B): A, B = B, A
    m, n = len(A), len(B)
    half = (m + n + 1) // 2
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i
        L1 = A[i-1] if i > 0 else -inf
        R1 = A[i] if i < m else inf
        L2 = B[j-1] if j > 0 else -inf
        R2 = B[j] if j < n else inf
        if L1 <= R2 and L2 <= R1:
            if (m + n) % 2: return max(L1, L2)
            return (max(L1, L2) + min(R1, R2)) / 2
        if L1 > R2: hi = i - 1
        else: lo = i + 1"""

SIZE, GAP, X0 = 0.78, 0.14, -2.3


def arr_row(values, color, y, size=SIZE):
    row = VGroup(*[Tile(v, color, size) for v in values]).arrange(RIGHT, buff=GAP)
    row.move_to([X0 + row.width / 2, y, 0])
    return row


def rows(ya):
    a = arr_row(A, CYAN, ya)
    b = arr_row(B, VIOLET, ya - 1.3)
    labs = VGroup(T("A", 34, CYAN).move_to([X0 - 0.75, ya, 0]), T("B", 34, VIOLET).move_to([X0 - 0.75, ya - 1.3, 0]))
    return a, b, labs


def cut_x(row, k):
    # x of the cut before element k (k = len means after the last one)
    if k == 0:
        return row[0].get_left()[0] - GAP / 2
    return row[k - 1].get_right()[0] + GAP / 2


def cut_bar(row, k, color=YELLOW, h=1.15):
    y = row.get_y()
    return Line([cut_x(row, k), y + h / 2, 0], [cut_x(row, k), y - h / 2, 0], color=color, stroke_width=7)


def cover():
    # Opening frame and closing frame are the same, so the video loops seamlessly
    title, tglow = gradient_title(["Median of Two", "Sorted Arrays"], size=84, y=3.3)
    a, b, labs = rows(0.4)
    cuts = VGroup(cut_bar(a, 4), cut_bar(b, 2))
    return title, tglow, VGroup(a, b, labs, cuts)


class Scene1_Hook(Base):
    def construct(self):
        title, tglow, art = cover()
        self.add(tglow, title, art)
        a, b, labs, cuts = art
        rng = random.Random(4)
        bg = VGroup(*[
            M(str(rng.randint(0, 99)), rng.randint(18, 34), rng.choice([CYAN, MAGENTA, VIOLET])).set_opacity(rng.uniform(0.12, 0.28))
            .move_to([rng.uniform(-4.1, 4.1), rng.choice([rng.uniform(-5.6, -3.4), rng.uniform(5.0, 5.7), rng.uniform(1.5, 1.9)]), 0])
            for _ in range(24)
        ])
        tags = tags_block([("LeetCode #4", CYAN), ("Hard", RED), ("Binary search", VIOLET)], y=-3.3)

        self.seg(0)
        self.beat(Indicate(title, color=WHITE, scale_factor=1.04), rt=0.7)
        self.beat(LaggedStart(*[FadeIn(d, scale=0.4) for d in bg], lag_ratio=0.04),
                  LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in [*tags[0], *tags[1]]], lag_ratio=0.3), rt=1.2)
        self.beat(LaggedStart(*[ring(t.box, CYAN) for t in a], *[ring(t.box, VIOLET) for t in b], lag_ratio=0.08), rt=1.3)
        self.beat(Indicate(cuts, color=WHITE), rt=0.8)
        self.until(DUR[0] - 1.1)
        self.beat(FadeOut(VGroup(title, tglow, tags, bg, cuts)), rt=0.45)
        self.beat(VGroup(a, b, labs).animate.shift(UP * 2.6), rt=0.55)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        a, b, labs = rows(3.0)
        self.add(a, b, labs)
        hdr = header("THE PROBLEM", CYAN)
        ma = T("m = 5", 26, CYAN).next_to(a, RIGHT, buff=0.35)
        nb = T("n = 6", 26, VIOLET).next_to(b, RIGHT, buff=0.25)
        sorted_lab = T("both sorted", 26, MUTED).move_to([0, 4.35, 0])

        self.seg(1)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(sorted_lab), rt=0.5)
        self.beat(LaggedStart(*[ring(t.box, CYAN) for t in a], lag_ratio=0.12), FadeIn(ma), rt=0.8)
        self.beat(LaggedStart(*[ring(t.box, VIOLET) for t in b], lag_ratio=0.12), FadeIn(nb), rt=0.8)
        self.close_seg()

        merged = VGroup(*[Tile(v, CYAN if s == "A" else VIOLET, 0.62) for v, s in MERGED]).arrange(RIGHT, buff=0.08).move_to([0, 0.2, 0])
        nums = index_labels(merged, 18, MUTED, start=1)
        src = []
        ia = ib = 0
        for v, s in MERGED:
            if s == "A":
                src.append(a[ia]); ia += 1
            else:
                src.append(b[ib]); ib += 1
        mid = merged[HALF - 1]
        med = VGroup(T("median", 34, MUTED), M("11", 96, YELLOW)).arrange(DOWN, buff=0.1).move_to([0, -2.1, 0])
        mglow = glow(med[1], YELLOW, layers=6, max_w=16, max_op=0.3)
        arrow = Arrow(mid.get_bottom() + DOWN * 0.45, med.get_top() + UP * 0.1, buff=0.05, color=YELLOW, stroke_width=5)

        self.seg(2)
        self.beat(LaggedStart(*[TransformFromCopy(s, m) for s, m in zip(src, merged)], lag_ratio=0.08), rt=1.6)
        self.beat(FadeIn(nums), rt=0.4)
        self.until(DUR[2] * 0.45)
        self.beat(restyle(mid, lambda x: x.box.set_stroke(YELLOW, width=5).set_fill(YELLOW, opacity=0.2)), ring(mid.box, YELLOW),
                  restyle(nums[HALF - 1], lambda x: x.set_color(YELLOW)), rt=0.6)
        self.beat(GrowArrow(arrow), FadeIn(med, shift=UP * 0.2), FadeIn(mglow), rt=0.7)
        self.clear_all()
        self.close_seg()


class Scene3_Merge(Base):
    def construct(self):
        hdr = header("THE EASY WAY", RED)
        a, b, labs = rows(3.6)
        slots = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.62, height=0.62, stroke_color=MUTED, stroke_width=1.5,
                                          fill_opacity=0) for _ in MERGED]).arrange(RIGHT, buff=0.08).move_to([0, 0.6, 0])
        merged = VGroup(*[Tile(v, CYAN if s == "A" else VIOLET, 0.62) for v, s in MERGED]).arrange(RIGHT, buff=0.08).move_to([0, 0.6, 0])
        pa = Triangle(color=CYAN, fill_opacity=1).scale(0.12).rotate(PI).next_to(a[0], UP, buff=0.1)
        pb = Triangle(color=VIOLET, fill_opacity=1).scale(0.12).next_to(b[0], DOWN, buff=0.1)
        o, o_lab, o_glow = big_o(r"O(m + n)", RED, -1.6, "time")

        self.seg(3)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(a), FadeIn(b), FadeIn(labs), FadeIn(slots), FadeIn(pa), FadeIn(pb), rt=0.6)
        ia = ib = 0
        per = 2.9 / len(MERGED)
        for k, (v, s) in enumerate(MERGED):
            if s == "A":
                anims = [TransformFromCopy(a[ia], merged[k])]
                ia += 1
                if ia < len(A):
                    anims.append(pa.animate.next_to(a[ia], UP, buff=0.1))
            else:
                anims = [TransformFromCopy(b[ib], merged[k])]
                ib += 1
                if ib < len(B):
                    anims.append(pb.animate.next_to(b[ib], DOWN, buff=0.1))
            self.beat(*anims, rt=per)
        self.beat(Write(o), FadeIn(o_glow), FadeIn(o_lab), rt=0.7)
        self.close_seg()

        goal, g_lab, g_glow = big_o(r"O(\log(m + n))", YELLOW, -4.0, "required", size=72)

        self.seg(4)
        self.beat(FadeIn(goal, shift=UP * 0.2), FadeIn(g_glow), FadeIn(g_lab), rt=0.7)
        self.until(DUR[4] * 0.45)
        self.beat(*[restyle(t, lambda x: x.set_opacity(0.25)) for t in [*a, *b, *merged]],
                  FadeOut(VGroup(pa, pb)), rt=0.6)
        self.beat(*[restyle(t, lambda x: x.set_opacity(1)) for t in (a[2], b[3], a[4])], rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        hdr = header("THE KEY IDEA", YELLOW)
        merged = VGroup(*[Tile(v, CYAN if s == "A" else VIOLET, 0.62) for v, s in MERGED]).arrange(RIGHT, buff=0.08).move_to([0, 2.6, 0])
        split_x = (merged[HALF - 1].get_right()[0] + merged[HALF].get_left()[0]) / 2
        split = Line([split_x, 3.3, 0], [split_x, 1.9, 0], color=YELLOW, stroke_width=7)
        lb = Brace(VGroup(*merged[:HALF]), DOWN, color=CYAN, buff=0.15)
        rb = Brace(VGroup(*merged[HALF:]), DOWN, color=MAGENTA, buff=0.15)
        lt = T("left half: 6", 26, CYAN).next_to(lb, DOWN, buff=0.1)
        rt_ = T("right half: 5", 26, MAGENTA).next_to(rb, DOWN, buff=0.1)

        self.seg(5)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in merged], lag_ratio=0.05), rt=0.9)
        self.until(DUR[5] * 0.45)
        self.beat(Create(split), rt=0.4)
        self.beat(GrowFromCenter(lb), FadeIn(lt), GrowFromCenter(rb), FadeIn(rt_), rt=0.7)
        self.close_seg()

        a, b, labs = rows(-0.2)
        cut_a = cut_bar(a, 1)
        cut_b = cut_bar(b, 5)
        i_lab = MathTex(r"i = 1", font_size=46, color=CYAN).move_to([-1.6, -2.9, 0])
        j_lab = MathTex(r"j = 6 - i = 5", font_size=46, color=VIOLET).move_to([1.6, -2.9, 0])
        rule = MathTex(r"i + j = 6", font_size=56, color=YELLOW).move_to([0, -4.0, 0])

        self.seg(6)
        self.beat(FadeIn(a), FadeIn(b), FadeIn(labs), rt=0.5)
        self.beat(Create(cut_a), FadeIn(i_lab), rt=0.5)
        self.until(DUR[6] * 0.4)
        self.beat(Create(cut_b), FadeIn(j_lab), rt=0.5)
        for k in (2, 3):
            self.beat(Transform(cut_a, cut_bar(a, k)), Transform(cut_b, cut_bar(b, HALF - k)),
                      Transform(i_lab, MathTex(rf"i = {k}", font_size=46, color=CYAN).move_to(i_lab)),
                      Transform(j_lab, MathTex(rf"j = 6 - i = {HALF - k}", font_size=46, color=VIOLET).move_to(j_lab)), rt=0.6)
        self.beat(Write(rule), rt=0.6)
        self.close_seg()

        brace = Brace(a, UP, color=CYAN, buff=0.12)
        btxt = T("binary search i in [0, m]", 26, CYAN).next_to(brace, UP, buff=0.08)

        self.seg(7)
        self.beat(FadeOut(VGroup(merged, split, lb, rb, lt, rt_)), rt=0.4)
        self.beat(GrowFromCenter(brace), FadeIn(btxt), *[restyle(t, lambda x: x.set_opacity(0.45)) for t in b],
                  LaggedStart(*[ring(t.box, CYAN) for t in a], lag_ratio=0.1), rt=0.9)
        self.close_seg()

        # Valid cut at i = 4, j = 2: check across the cut
        x1 = MathTex(r"A[i-1] \le B[j]", font_size=46, color=GREEN).move_to([0, -2.6, 0])
        x2 = MathTex(r"B[j-1] \le A[i]", font_size=46, color=GREEN).move_to([0, -3.4, 0])
        sub = T("sorted rows cover the rest", 26, MUTED).move_to([0, -4.5, 0])
        arr1 = Arrow(a[3].get_bottom(), b[2].get_top(), buff=0.06, color=GREEN, stroke_width=5, tip_length=0.18)
        arr2 = Arrow(b[1].get_top(), a[4].get_bottom(), buff=0.06, color=GREEN, stroke_width=5, tip_length=0.18)

        self.seg(8)
        self.beat(FadeOut(VGroup(brace, btxt, i_lab, j_lab, rule)), *[restyle(t, lambda x: x.set_opacity(1)) for t in b],
                  Transform(cut_a, cut_bar(a, 4)), Transform(cut_b, cut_bar(b, 2)), rt=0.6)
        self.until(DUR[8] * 0.2)
        self.beat(GrowArrow(arr1), FadeIn(x1, shift=UP * 0.2), rt=0.7)
        self.beat(GrowArrow(arr2), FadeIn(x2, shift=UP * 0.2), rt=0.7)
        self.until(DUR[8] * 0.6)
        self.beat(FadeIn(sub), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        hdr = header("BINARY SEARCH THE CUT", YELLOW)
        code = code_panel(CODE, -3.85, max_h=4.2)

        def readout(d):
            parts = VGroup(*[pill(f"{k} {d[k]}", c, 26) for k, c in [("lo", MUTED), ("hi", MUTED), ("i", CYAN), ("j", VIOLET)]])
            return parts.arrange(RIGHT, buff=0.25).move_to([0, -1.3, 0])

        st = {"lo": 0, "hi": 5, "i": "-", "j": "-"}
        ro = readout(st)
        bar = line_bar(code, 4)
        events = walk_events(WALK, ["cutA", "cutB", "sides", "chk1", "chk2", "move", "valid", "median"])
        it = WALK["steps"]

        def intro():
            self.until(0.3)
            self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(ro), rt=0.5)
            self.until(1.0)
            self.beat(FadeIn(code, shift=UP * 0.3), rt=0.8)
            self.until(2.0)
            self.beat(FadeIn(bar), rt=0.4)

        def show(*anims, k0, k1=None, color=YELLOW):
            self.beat(Transform(bar, line_bar(code, k0, k1, color)), *anims, rt=0.3)

        def on(kind, k):
            s = it[k]
            if kind == "cutA":
                st["i"] = s["i"]
                show(Transform(ro, readout(st)), k0=6)
            elif kind == "cutB":
                st["j"] = s["j"]
                show(Transform(ro, readout(st)), k0=7)
            elif kind == "sides":
                show(k0=8, k1=11)
            elif kind == "chk1":
                show(k0=12)
            elif kind == "chk2":
                show(k0=12, color=GREEN if s["ok"] else RED)
            elif kind == "move":
                st["lo"] = s["i"] + 1
                show(Transform(ro, readout(st)), k0=16, color=MAGENTA)
            elif kind == "valid":
                show(k0=12, color=GREEN)
            elif kind == "median":
                show(k0=13, color=GREEN)

        def outro():
            self.until(DUR[WALK["last"]] - 0.55)
            self.beat(FadeOut(VGroup(hdr, ro, code, bar)), rt=0.5)

        self.run_events(WALK, events, on, intro, outro)


class Scene6_Complexity(Base):
    def construct(self):
        hdr = header("COMPLEXITY", GREEN)
        a = arr_row(A, CYAN, 3.4)
        ticks = VGroup(*[Line([cut_x(a, k), 3.95, 0], [cut_x(a, k), 2.85, 0], color=MUTED, stroke_width=2) for k in range(6)])
        rng_ = lambda lo, hi: Rectangle(width=cut_x(a, hi) - cut_x(a, lo) + 0.1, height=0.16, fill_color=YELLOW, fill_opacity=0.7,
                                        stroke_width=0).move_to([(cut_x(a, lo) + cut_x(a, hi)) / 2, 2.55, 0])
        r = rng_(0, 5)
        o, o_lab, o_glow = big_o(r"O(\log \min(m, n))", GREEN, 0.6, "time", size=70)
        note = T("each step halves the range", 26, MUTED).move_to([0, 1.85, 0])

        self.seg(15)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(a), FadeIn(ticks), FadeIn(r), rt=0.6)
        self.beat(Transform(r, rng_(3, 5)), FadeIn(note), rt=0.6)
        self.beat(Transform(r, rng_(4, 4).stretch_to_fit_width(0.2)), rt=0.6)
        self.until(DUR[15] * 0.5)
        self.beat(Write(o), FadeIn(o_glow), FadeIn(o_lab), rt=0.8)
        self.close_seg()

        ptrs = VGroup(*[pill(s, c, 28) for s, c in [("lo", MUTED), ("hi", MUTED), ("i", CYAN), ("j", VIOLET)]]).arrange(RIGHT, buff=0.3)
        ptrs.move_to([0, -1.5, 0])
        so, so_lab, so_glow = big_o(r"O(1)", VIOLET, -3.3, "extra space", size=72)

        self.seg(16)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in ptrs], lag_ratio=0.15), rt=0.8)
        self.beat(Write(so), FadeIn(so_glow), FadeIn(so_lab), rt=0.8)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 0.6, max_h=6.0)
        cglow = glow(code.background, VIOLET, max_w=22, max_op=0.25)
        bar = line_bar(code, 6, 7, CYAN)
        d = DUR[17]

        self.seg(17)
        self.beat(FadeIn(code.background), FadeIn(cglow), rt=0.3)
        self.beat(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.05),
                  FadeIn(code.line_numbers), rt=0.8)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(d * 0.5)
        self.beat(Transform(bar, line_bar(code, 12, 12, GREEN)), rt=0.4)
        self.close_seg()

        tag = VGroup(T("One cut.", 64), T("Two arrays.", 64), T("Log time.", 64)).arrange(DOWN, buff=0.15)
        tag.set_color_by_gradient(CYAN, VIOLET, MAGENTA).move_to([0, 0.8, 0])
        tag_glow = glow(tag, VIOLET, layers=6, max_w=18, max_op=0.22)
        title, tglow, art = cover()

        self.seg(18)
        self.beat(FadeOut(VGroup(code, cglow, bar), shift=UP * 0.4), FadeIn(tag), FadeIn(tag_glow), rt=0.6)
        self.hold(0.6)
        # Morph into the opening frame so the loop closes seamlessly
        self.finish(ReplacementTransform(tag, title), FadeOut(tag_glow), FadeIn(tglow), FadeIn(art, shift=UP * 0.3), rt=1.1)
        self.add(tglow, title, art)
        self.close_seg()
