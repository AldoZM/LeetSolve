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

WALK = json.load(open('walk.json', encoding='utf-8'))
S, R = WALK["s"], WALK["rows"]
LET = WALK["letters"]
ROW_COLORS = [CYAN, VIOLET, GREEN]
ROWS = ["".join(e["ch"] for e in LET if e["row"] == r) for r in range(R)]
ANSWER = "".join(ROWS)


def grid_pos():
    # Column of each letter in the drawn zigzag: straight down in one column, then one column per step up
    out, col = [], 0
    for k, e in enumerate(LET):
        if k > 0 and e["row"] < LET[k - 1]["row"]:
            col += 1
        out.append((col, e["row"]))
    return out


GRID = grid_pos()

CODE = """def convert(s, numRows):
    if numRows == 1: return s
    rows = [""] * numRows
    r, step = 0, 1
    for ch in s:
        rows[r] += ch
        if r == 0: step = 1
        elif r == numRows - 1: step = -1
        r += step
    return "".join(rows)"""


def zigzag(center_y, size=0.7, dx=0.95, dy=0.95):
    # Letter tiles at their zigzag cells plus the path that visits them in order
    ncol = GRID[-1][0] + 1
    x0 = -(ncol - 1) * dx / 2
    tiles = VGroup(*[Tile(e["ch"], ROW_COLORS[e["row"]], size).move_to([x0 + c * dx, center_y + (1 - r) * dy, 0])
                     for e, (c, r) in zip(LET, GRID)])
    path = VMobject(stroke_color=YELLOW, stroke_width=4, stroke_opacity=0.6)
    path.set_points_as_corners([t.get_center() for t in tiles])
    return tiles, path


def cover():
    # Opening frame and closing frame are the same, so the video loops seamlessly
    title, tglow = gradient_title(["Zigzag", "Conversion"], size=100, y=3.3)
    tiles, path = zigzag(-0.6)
    return title, tglow, VGroup(path, tiles)


class Scene1_Hook(Base):
    def construct(self):
        title, tglow, art = cover()
        self.add(tglow, title, art)
        path, tiles = art
        rng = random.Random(6)
        bg = VGroup(*[
            M(rng.choice("PAYLISHRNG"), rng.randint(18, 34), rng.choice([CYAN, MAGENTA, VIOLET])).set_opacity(rng.uniform(0.12, 0.28))
            .move_to([rng.uniform(-4.1, 4.1), rng.choice([rng.uniform(-5.6, -4.3), rng.uniform(5.0, 5.7)]), 0])
            for _ in range(20)
        ])
        tags = tags_block([("LeetCode #6", CYAN), ("Medium", YELLOW), ("Simulation", VIOLET)], y=-3.5)

        self.seg(0)
        self.beat(LaggedStart(*[FadeIn(d, scale=0.4) for d in bg], lag_ratio=0.04),
                  LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in [*tags[0], *tags[1]]], lag_ratio=0.3), rt=0.9)
        self.beat(ShowPassingFlash(path.copy().set_stroke(WHITE, width=8, opacity=1), time_width=0.4), rt=1.2)
        self.finish(FadeOut(VGroup(title, tglow, tags, bg, path, tiles)), rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        hdr = header("THE PROBLEM", CYAN)
        line = tile_row(list(S), CYAN, 3.6, size=0.52, gap=0.08)
        rows_lab = T("numRows = 3", 28, YELLOW).move_to([0, 2.7, 0])

        self.seg(1)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in line], lag_ratio=0.05), rt=1.0)
        self.beat(FadeIn(rows_lab), rt=0.4)
        self.close_seg()

        tiles, path = zigzag(0.6, size=0.66, dx=0.95, dy=1.0)
        row_labs = VGroup(*[T(f"row {r}", 22, ROW_COLORS[r]).move_to([-4.0, tiles[0].get_y() - r * 1.0, 0]) for r in range(R)])

        self.seg(2)
        self.beat(FadeIn(row_labs), rt=0.4)
        per = (DUR[2] - 1.4) / len(S)
        for k in range(len(S)):
            self.beat(ReplacementTransform(line[k].copy(), tiles[k]), rt=per)
        self.beat(Create(path), rt=0.8)
        self.close_seg()

        out_rows = VGroup(*[M(s, 40, ROW_COLORS[r]) for r, s in enumerate(ROWS)]).arrange(RIGHT, buff=0.25).move_to([0, -2.4, 0])
        res = VGroup(T("output", 26, MUTED), M(f'"{ANSWER}"', 40, YELLOW)).arrange(DOWN, buff=0.15).move_to([0, -3.9, 0])

        self.seg(3)
        self.beat(FadeOut(path), rt=0.3)
        for r in range(R):
            members = [tiles[k] for k, e in enumerate(LET) if e["row"] == r]
            self.beat(LaggedStart(*[ring(t.box, YELLOW) for t in members], lag_ratio=0.1),
                      FadeIn(out_rows[r], shift=DOWN * 0.2), rt=1.1)
            self.hold(0.3)
        self.beat(FadeIn(res, shift=UP * 0.2), rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene3_Grid(Base):
    def construct(self):
        hdr = header("FULL GRID?", RED)
        ncol = GRID[-1][0] + 1
        cs = 0.95
        x0 = -(ncol - 1) * cs / 2
        used = {(c, r) for c, r in GRID}
        cells = VGroup()
        for r in range(R):
            for c in range(ncol):
                box = Square(cs - 0.1, stroke_color=MUTED, stroke_width=1.5, fill_opacity=0).move_to([x0 + c * cs, 2.2 - r * cs, 0])
                cells.add(box)
        tiles, _ = zigzag(2.2 - cs, size=0.7, dx=cs, dy=cs)
        empty = [cells[r * ncol + c] for r in range(R) for c in range(ncol) if (c, r) not in used]
        note = T(f"{len(empty)} of {R * ncol} cells wasted", 28, RED).move_to([0, -1.2, 0])
        o, o_lab, o_glow = big_o(r"O(\text{rows} \times n)", RED, -3.0, "space", size=64)

        self.seg(4)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), LaggedStart(*[Create(c) for c in cells], lag_ratio=0.02), rt=0.9)
        self.beat(LaggedStart(*[FadeIn(t, scale=0.6) for t in tiles], lag_ratio=0.05), rt=0.9)
        self.until(DUR[4] * 0.5)
        self.beat(*[c.animate.set_fill(RED, opacity=0.25).set_stroke(RED) for c in empty], FadeIn(note), rt=0.6)
        self.beat(Write(o), FadeIn(o_glow), FadeIn(o_lab), rt=0.8)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        hdr = header("THE TRICK", YELLOW)
        tiles, path = zigzag(2.4, size=0.66, dx=0.95, dy=1.0)
        top_y = tiles[0].get_y()
        packed = []
        count = [0] * R
        for e in LET:
            packed.append([-2.4 + count[e["row"]] * 0.78, top_y - e["row"] * 1.0, 0])
            count[e["row"]] += 1
        labs = VGroup(*[T(f"rows[{r}]", 22, ROW_COLORS[r]).move_to([-3.25, top_y - r * 1.0, 0]) for r in range(R)])

        self.seg(5)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(tiles), FadeIn(path), rt=0.6)
        self.until(DUR[5] * 0.3)
        self.beat(FadeOut(path), *[t.animate.move_to(p).shift(RIGHT * 0.45) for t, p in zip(tiles, packed)], rt=1.2)
        self.beat(FadeIn(labs), rt=0.4)
        self.close_seg()

        ptr = Triangle(color=YELLOW, fill_opacity=1).scale(0.16).rotate(-PI / 2).move_to([-4.2, top_y, 0])
        steps_lab = VGroup(T("step = +1  going down", 26, YELLOW), T("step = −1  going up", 26, MAGENTA)).arrange(DOWN, buff=0.25)
        steps_lab.move_to([0, -1.2, 0])
        bounce = [0, 1, 2, 1, 0, 1, 2]

        self.seg(6)
        self.beat(FadeIn(ptr), FadeIn(steps_lab[0]), rt=0.5)
        for k, r in enumerate(bounce[1:], 1):
            going_up = r < bounce[k - 1]
            anims = [ptr.animate.move_to([-4.2, top_y - r * 1.0, 0]).set_color(MAGENTA if going_up else YELLOW)]
            if k == 3:
                anims.append(FadeIn(steps_lab[1]))
            self.beat(*anims, rt=0.45)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        hdr = header("BOUNCING POINTER", YELLOW)
        code = code_panel(CODE, -3.85)

        def readout(ch, r, step):
            parts = VGroup(pill(f"ch {ch}", CYAN, 28), pill(f"r {r}", ROW_COLORS[r] if r != "-" else MUTED, 28),
                           pill(f"step {step}", YELLOW if step == "+1" else MAGENTA, 28))
            return parts.arrange(RIGHT, buff=0.3).move_to([0, -1.35, 0])

        st = {"ch": "-", "r": 0, "step": "+1"}
        ro = readout("-", 0, "+1")
        bar = line_bar(code, 2, 3)
        ev = []
        for k, e in enumerate(LET):
            ev.append((seg_time(WALK["first"], e["t"]), "place", k))
            if e["turn"]:
                ev.append((seg_time(WALK["first"], e["tturn"]), "turn", k))
        ev.append((seg_time(WALK["first"], WALK["join"]), "join", 0))
        ev.sort(key=lambda x: x[0])

        def intro():
            self.until(0.3)
            self.beat(FadeIn(hdr, shift=RIGHT * 0.3), rt=0.5)
            self.until(1.0)
            self.beat(FadeIn(code, shift=UP * 0.3), rt=0.8)
            self.until(2.4)
            self.beat(FadeIn(bar), FadeIn(ro), rt=0.4)

        def on(kind, k):
            e = LET[k]
            fast = k >= 5
            if kind == "place":
                st["ch"], st["r"] = e["ch"], e["row"]
                self.beat(Transform(bar, line_bar(code, 5, 5, ROW_COLORS[e["row"]])), Transform(ro, readout(st["ch"], st["r"], st["step"])),
                          rt=0.2 if fast else 0.3)
            elif kind == "turn":
                st["step"] = "-1" if e["row"] == R - 1 else "+1"
                line = 7 if e["row"] == R - 1 else 6
                self.beat(Transform(bar, line_bar(code, line, line, MAGENTA if st["step"] == "-1" else YELLOW)),
                          Transform(ro, readout(st["ch"], st["r"], st["step"])), rt=0.2 if fast else 0.3)
            elif kind == "join":
                self.beat(Transform(bar, line_bar(code, 9, 9, GREEN)), rt=0.3)

        def outro():
            self.finish(FadeOut(VGroup(hdr, ro, code, bar)), rt=0.5)

        self.run_events(WALK, ev, on, intro, outro)


class Scene6_Complexity(Base):
    def construct(self):
        hdr = header("COMPLEXITY", GREEN)
        line = tile_row(list(S), CYAN, 3.6, size=0.52, gap=0.08)
        dot = Triangle(color=YELLOW, fill_opacity=1).scale(0.12).rotate(PI).next_to(line[0], UP, buff=0.1)
        o, o_lab, o_glow = big_o(r"O(n)", GREEN, 1.4, "time")

        self.seg(13)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(line), FadeIn(dot), rt=0.5)
        self.beat(dot.animate.next_to(line[-1], UP, buff=0.1),
                  LaggedStart(*[restyle(t, lambda x: x.box.set_stroke(YELLOW, width=4)) for t in line], lag_ratio=0.1), rt=1.6)
        self.beat(Write(o), FadeIn(o_glow), FadeIn(o_lab), rt=0.8)
        self.close_seg()

        rows = VGroup(*[M(s, 40, ROW_COLORS[r]) for r, s in enumerate(ROWS)]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([0, -1.4, 0])
        so, so_lab, so_glow = big_o(r"O(n)", VIOLET, -3.7, "extra space", size=72)

        self.seg(14)
        self.beat(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.2), rt=0.8)
        self.beat(Write(so), FadeIn(so_glow), FadeIn(so_lab), rt=0.8)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.0)
        cglow = glow(code.background, VIOLET, max_w=22, max_op=0.25)
        bar = line_bar(code, 2, 2, CYAN)

        self.seg(15)
        self.beat(FadeIn(code.background), FadeIn(cglow), rt=0.3)
        self.beat(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08),
                  FadeIn(code.line_numbers), rt=0.8)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(DUR[15] * 0.55)
        self.beat(Transform(bar, line_bar(code, 6, 8, YELLOW)), rt=0.4)
        self.close_seg()

        tag = VGroup(T("Down and up.", 64), T("Row by row.", 64)).arrange(DOWN, buff=0.15)
        tag.set_color_by_gradient(CYAN, VIOLET, MAGENTA).move_to([0, 0.8, 0])
        tag_glow = glow(tag, VIOLET, layers=6, max_w=18, max_op=0.22)
        title, tglow, art = cover()

        self.seg(16)
        self.beat(FadeOut(VGroup(code, cglow, bar), shift=UP * 0.4), FadeIn(tag), FadeIn(tag_glow), rt=0.6)
        self.hold(0.5)
        # Morph into the opening frame so the loop closes seamlessly
        self.finish(ReplacementTransform(tag, title), FadeOut(tag_glow), FadeIn(tglow), FadeIn(art, shift=UP * 0.3), rt=1.1)
        self.add(tglow, title, art)
        self.close_seg()
