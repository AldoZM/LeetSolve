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
NODES = WALK["nodes"]
LEVELS = WALK["levels"]
VALS = [n["val"] for n in NODES]
LEVEL_COLORS = [CYAN, VIOLET, MAGENTA, GREEN]

CODE = """def levelOrder(root):
    if not root: return []
    res, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        res.append(level)
    return res"""

# Tree layout in Manim units (shared shape with the 3D scene)
XS = {0: 0.0, 1: -2.0, 2: 2.0, 3: -3.0, 4: -1.0, 5: 1.0, 6: 3.0, 7: -0.5, 8: 0.5}
DEPTH = {i: next(L for L, ids in enumerate(LEVELS) if i in ids) for i in range(len(NODES))}


class TNode(VGroup):
    def __init__(self, value, color, r=0.36, **kwargs):
        super().__init__(**kwargs)
        self.box = Circle(radius=r, fill_color=PANEL, fill_opacity=1, stroke_color=color, stroke_width=3)
        self.num = M(str(value), int(30 * r / 0.36), INK).move_to(self.box)
        self.add(self.box, self.num)


def tree(top_y, dy=1.15, scale=1.0, r=0.36):
    nodes = VGroup(*[TNode(VALS[i], LEVEL_COLORS[DEPTH[i]], r).move_to([XS[i] * scale, top_y - DEPTH[i] * dy, 0])
                     for i in range(len(NODES))])
    edges = VGroup(*[Line(nodes[n["parent"]].get_center(), nodes[i].get_center(), color=ARROW, stroke_width=3,
                          buff=r) for i, n in enumerate(NODES) if n["parent"] is not None])
    return nodes, edges


def res_text(k, size=32):
    # The first k levels of the answer as a nested list
    parts = ",".join("[" + ",".join(str(VALS[i]) for i in LEVELS[L]) + "]" for L in range(k))
    return M(f"[{parts}]", size, YELLOW)


def cover():
    # Opening frame and closing frame are the same, so the video loops seamlessly
    title, tglow = gradient_title(["Binary Tree", "Level Order", "Traversal"], size=72, y=3.6)
    nodes, edges = tree(0.6, dy=1.05, scale=0.95, r=0.34)
    bands = VGroup(*[RoundedRectangle(corner_radius=0.2, width=8.0, height=0.82, fill_color=LEVEL_COLORS[L], fill_opacity=0.08,
                                      stroke_width=0).move_to([0, 0.6 - L * 1.05, 0]) for L in range(len(LEVELS))])
    return title, tglow, VGroup(bands, edges, nodes)


class Scene1_Hook(Base):
    def construct(self):
        title, tglow, art = cover()
        self.add(tglow, title, art)
        bands, edges, nodes = art
        tags = tags_block([("LeetCode #102", CYAN), ("Medium", YELLOW), ("BFS · Queue", VIOLET)], y=-4.1)

        self.seg(0)
        self.beat(LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in [*tags[0], *tags[1]]], lag_ratio=0.3), rt=0.9)
        self.beat(LaggedStart(*[Indicate(b, color=LEVEL_COLORS[L], scale_factor=1.0) for L, b in enumerate(bands)], lag_ratio=0.3),
                  LaggedStart(*[ring(nodes[i].box, WHITE) for ids in LEVELS for i in ids], lag_ratio=0.08), rt=1.6)
        self.finish(FadeOut(VGroup(title, tglow, tags, bands)), art[1:].animate.shift(UP * 1.6), rt=0.6)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        nodes, edges = tree(2.2, dy=1.05, scale=0.95, r=0.34)
        self.add(edges, nodes)
        hdr = header("THE PROBLEM", CYAN)
        order = T("top to bottom, left to right", 28, MUTED).move_to([0, 4.4, 0])

        self.seg(1)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(order), rt=0.5)
        self.beat(LaggedStart(*[ring(nodes[i].box, YELLOW) for ids in LEVELS for i in ids], lag_ratio=0.15), rt=1.6)
        self.close_seg()

        rows = VGroup(*[M("[" + ", ".join(str(VALS[i]) for i in ids) + "]", 40, LEVEL_COLORS[L]) for L, ids in enumerate(LEVELS)])
        rows.arrange(DOWN, buff=0.22).move_to([0, -3.4, 0])
        bands = VGroup(*[RoundedRectangle(corner_radius=0.2, width=8.0, height=0.8, fill_color=LEVEL_COLORS[L], fill_opacity=0.12,
                                          stroke_width=0).move_to([0, 2.2 - L * 1.05, 0]) for L in range(len(LEVELS))])
        self.seg(2)
        per = (DUR[2] - 0.9) / len(LEVELS)
        for L, ids in enumerate(LEVELS):
            self.beat(FadeIn(bands[L]), LaggedStart(*[ring(nodes[i].box, LEVEL_COLORS[L]) for i in ids], lag_ratio=0.1),
                      FadeIn(rows[L], shift=DOWN * 0.2), rt=min(0.8, per))
            self.until((L + 1) * per)
        self.clear_all()
        self.close_seg()


class Scene3_DFS(Base):
    def construct(self):
        hdr = header("DEPTH FIRST?", RED)
        nodes, edges = tree(3.0, dy=1.1, scale=0.95, r=0.34)
        dfs = [0, 1, 3, 4, 7, 2, 5, 8, 6]
        dot = Dot(nodes[0].get_center(), radius=0.13, color=RED)
        seq = VGroup(*[M(str(VALS[i]), 34, RED) for i in dfs]).arrange(RIGHT, buff=0.3).move_to([0, -2.2, 0])
        bad = T("✗  wrong order", 34, RED).move_to([0, -3.4, 0])

        self.seg(3)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(edges), FadeIn(nodes), rt=0.5)
        self.beat(FadeIn(dot), FadeIn(seq[0]), rt=0.25)
        for k, i in enumerate(dfs[1:], 1):
            self.beat(dot.animate.move_to(nodes[i].get_center()), FadeIn(seq[k]), rt=0.36)
        self.beat(FadeIn(bad, scale=1.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene4_BFS(Base):
    def construct(self):
        hdr = header("BREADTH FIRST", GREEN)
        nodes, edges = tree(3.4, dy=1.05, scale=0.95, r=0.34)
        wave = Line([-4.2, 3.4, 0], [4.2, 3.4, 0], color=YELLOW, stroke_width=6)

        self.seg(4)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(edges), FadeIn(nodes), rt=0.5)
        self.beat(Create(wave), rt=0.3)
        self.bring_to_front(nodes)
        for L, ids in enumerate(LEVELS):
            self.beat(wave.animate.move_to([0, 3.4 - L * 1.05, 0]),
                      *[restyle(nodes[i], lambda m: m.box.set_stroke(YELLOW, width=5)) for i in ids], rt=0.7)
        self.close_seg()

        slots = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.85, height=0.85, stroke_color=MUTED, stroke_width=2)
                         for _ in range(5)]).arrange(RIGHT, buff=0.12).move_to([0, -1.2, 0])
        qbox = SurroundingRectangle(slots, color=VIOLET, buff=0.15, corner_radius=0.15)
        q_in = T("in →", 26, GREEN).next_to(qbox, RIGHT, buff=0.15)
        q_out = T("← out", 26, MAGENTA).next_to(qbox, LEFT, buff=0.15)
        q_lab = T("queue: first in, first out", 28, VIOLET).next_to(qbox, DOWN, buff=0.3)
        items = [Tile(v, VIOLET, 0.7) for v in (9, 20)]

        self.seg(5)
        self.beat(FadeOut(wave), Create(qbox), FadeIn(slots), FadeIn(q_in), FadeIn(q_out), FadeIn(q_lab), rt=0.6)
        for k, it in enumerate(items):
            it.move_to(slots[k])
            self.beat(FadeIn(it, shift=LEFT * 0.6), rt=0.45)
        self.beat(FadeOut(items[0], shift=LEFT * 0.8), items[1].animate.move_to(slots[0]), rt=0.5)
        self.close_seg()

        lvl = [Tile(VALS[i], MAGENTA, 0.7).move_to(slots[k]) for k, i in enumerate(LEVELS[2])]
        brace = Brace(VGroup(*lvl), DOWN, color=YELLOW, buff=0.5)
        size = MathTex(r"\text{len(queue)} = 4", font_size=46, color=YELLOW).next_to(brace, DOWN, buff=0.15)
        note = T("exactly this level", 28, YELLOW).next_to(size, DOWN, buff=0.2)

        self.seg(6)
        self.beat(FadeOut(items[1]), FadeOut(q_lab), LaggedStart(*[FadeIn(t, shift=LEFT * 0.4) for t in lvl], lag_ratio=0.15), rt=0.8)
        self.beat(*[restyle(nodes[i], lambda m: m.box.set_stroke(MAGENTA, width=5).set_fill(MAGENTA, opacity=0.2)) for i in LEVELS[2]], rt=0.5)
        self.until(DUR[6] * 0.45)
        self.beat(GrowFromCenter(brace), Write(size), rt=0.7)
        self.beat(FadeIn(note, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        hdr = header("BFS WITH A QUEUE", YELLOW)
        code = code_panel(CODE, -4.25, max_h=3.4)

        def readout(k):
            return res_text(k, 30).move_to([0, -2.05, 0])

        def size_pill(n):
            return corner_pill(f"size {n}", MAGENTA)

        ro = readout(0)
        sp = size_pill("-")
        bar = line_bar(code, 2)
        ev = [(seg_time(WALK["first"], WALK["init"]), "init", None)]
        ev += [(seg_time(WALK["first"], e["t"]), e["kind"], e) for e in WALK["events"]]
        ev.append((seg_time(WALK["first"], WALK["final"]), "final", None))
        ev.sort(key=lambda x: x[0])
        st = {"done": 0}

        def intro():
            self.until(0.2)
            self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(sp), rt=0.4)
            self.until(0.6)
            self.beat(FadeIn(code, shift=UP * 0.3), FadeIn(ro), rt=0.7)

        def on(kind, e):
            if kind == "init":
                self.beat(FadeIn(bar), rt=0.3)
            elif kind == "size":
                self.beat(Transform(bar, line_bar(code, 5, 5, MAGENTA)), Transform(sp, size_pill(e["n"])), rt=0.3)
            elif kind == "pop":
                self.beat(Transform(bar, line_bar(code, 6)), rt=0.25)
            elif kind == "record":
                self.beat(Transform(bar, line_bar(code, 7, 7, GREEN)), rt=0.25)
            elif kind == "push":
                line = 8 if e["side"] == "L" else 9
                self.beat(Transform(bar, line_bar(code, line, line, VIOLET)), rt=0.25)
            elif kind == "done":
                st["done"] += 1
                self.beat(Transform(bar, line_bar(code, 10, 10, GREEN)), Transform(ro, readout(st["done"])), rt=0.3)
            elif kind == "final":
                self.beat(Transform(bar, line_bar(code, 11, 11, GREEN)), rt=0.3)

        def outro():
            self.finish(FadeOut(VGroup(hdr, ro, sp, code, bar)), rt=0.5)

        self.run_events(WALK, ev, on, intro, outro)


class Scene6_Complexity(Base):
    def construct(self):
        hdr = header("COMPLEXITY", GREEN)
        nodes, edges = tree(3.6, dy=0.9, scale=0.8, r=0.3)
        o, o_lab, o_glow = big_o(r"O(n)", GREEN, -0.2, "time")

        self.seg(13)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(edges), FadeIn(nodes), rt=0.5)
        self.beat(LaggedStart(*[ring(nodes[i].box, YELLOW) for ids in LEVELS for i in ids], lag_ratio=0.1), rt=1.4)
        self.beat(Write(o), FadeIn(o_glow), FadeIn(o_lab), rt=0.8)
        self.close_seg()

        widest = SurroundingRectangle(VGroup(*[nodes[i] for i in LEVELS[2]]), color=MAGENTA, buff=0.15, corner_radius=0.2)
        wl = T("widest level", 24, MAGENTA).next_to(widest, DOWN, buff=0.12).align_to(widest, LEFT)
        so, so_lab, so_glow = big_o(r"O(w)", VIOLET, -3.0, "space, w = max width", size=72)

        self.seg(14)
        self.beat(Create(widest), FadeIn(wl), rt=0.6)
        self.beat(Write(so), FadeIn(so_glow), FadeIn(so_lab), rt=0.8)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.0)
        cglow = glow(code.background, VIOLET, max_w=22, max_op=0.25)
        bar = line_bar(code, 2, 2, VIOLET)

        self.seg(15)
        self.beat(FadeIn(code.background), FadeIn(cglow), rt=0.3)
        self.beat(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.06),
                  FadeIn(code.line_numbers), rt=0.8)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(DUR[15] * 0.5)
        self.beat(Transform(bar, line_bar(code, 5, 5, MAGENTA)), rt=0.4)
        self.close_seg()

        tag = VGroup(T("Level by level,", 64), T("in rows.", 64)).arrange(DOWN, buff=0.15)
        tag.set_color_by_gradient(CYAN, VIOLET, MAGENTA).move_to([0, 0.8, 0])
        tag_glow = glow(tag, VIOLET, layers=6, max_w=18, max_op=0.22)
        title, tglow, art = cover()

        self.seg(16)
        self.beat(FadeOut(VGroup(code, cglow, bar), shift=UP * 0.4), FadeIn(tag), FadeIn(tag_glow), rt=0.6)
        self.hold(0.6)
        # Morph into the opening frame so the loop closes seamlessly
        self.finish(ReplacementTransform(tag, title), FadeOut(tag_glow), FadeIn(tglow), FadeIn(art, shift=UP * 0.3), rt=1.1)
        self.add(tglow, title, art)
        self.close_seg()
