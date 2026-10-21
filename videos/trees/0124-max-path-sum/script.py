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
TRACE = WALK["trace"]
VALS = [n["val"] for n in NODES]
BEST_PATH = WALK["best_path"]

CODE = """def maxPathSum(root):
    best = -inf
    def gain(node):
        nonlocal best
        if not node: return 0
        left = max(gain(node.left), 0)
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)
        return node.val + max(left, right)
    gain(root)
    return best"""

XS = {0: 0.0, 1: -2.0, 2: 2.0, 3: -3.0, 4: -1.0, 5: 1.0, 6: 3.0}
DEPTH = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2}


class TNode(VGroup):
    def __init__(self, value, color, r=0.42, **kwargs):
        super().__init__(**kwargs)
        self.box = Circle(radius=r, fill_color=PANEL, fill_opacity=1, stroke_color=color, stroke_width=3)
        self.num = M(str(value), int(28 * r / 0.42), INK).move_to(self.box)
        self.add(self.box, self.num)


def node_color(v):
    return RED if v < 0 else CYAN


def tree(top_y, dy=1.4, scale=1.0, r=0.42):
    nodes = VGroup(*[TNode(VALS[i], node_color(VALS[i]), r).move_to([XS[i] * scale, top_y - DEPTH[i] * dy, 0])
                     for i in range(len(NODES))])
    edges = {}
    for i, n in enumerate(NODES):
        if n["parent"] is not None:
            edges[i] = Line(nodes[n["parent"]].get_center(), nodes[i].get_center(), color=ARROW, stroke_width=3, buff=r)
    return nodes, edges


def path_edges(edges, ids, color=YELLOW, width=9):
    # Highlight the edges that join consecutive nodes of a path
    out = VGroup()
    for a, b in zip(ids, ids[1:]):
        child = a if NODES[a]["parent"] == b else b
        out.add(edges[child].copy().set_stroke(color, width=width))
    return out


def cover():
    # Opening frame and closing frame are the same, so the video loops seamlessly
    title, tglow = gradient_title(["Binary Tree", "Maximum", "Path Sum"], size=80, y=3.5)
    nodes, edges = tree(0.4, dy=1.25, scale=1.0, r=0.4)
    gold = path_edges(edges, BEST_PATH, YELLOW, 10)
    gglow = glow(gold, YELLOW, layers=5, max_w=22, max_op=0.25)
    total = M("= 42", 44, YELLOW).move_to([2.0, -3.3, 0])
    return title, tglow, VGroup(VGroup(*edges.values()), gglow, gold, nodes, total)


class Scene1_Hook(Base):
    def construct(self):
        title, tglow, art = cover()
        self.add(tglow, title, art)
        edges, gglow, gold, nodes, total = art
        tags = tags_block([("LeetCode #124", CYAN), ("Hard", RED), ("DFS · post-order", VIOLET)], y=-4.6)

        self.seg(0)
        self.beat(LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in [*tags[0], *tags[1]]], lag_ratio=0.3), rt=0.9)
        self.beat(ShowPassingFlash(gold.copy().set_stroke(WHITE, width=14), time_width=0.6),
                  *[ring(nodes[i].box, YELLOW) for i in BEST_PATH], rt=1.2)
        self.beat(Indicate(total, color=WHITE), rt=0.8)
        self.finish(FadeOut(VGroup(title, tglow, tags, gglow, gold, total)), VGroup(edges, nodes).animate.shift(UP * 2.0), rt=0.6)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        nodes, edges = tree(2.4, dy=1.25, scale=1.0, r=0.4)
        self.add(VGroup(*edges.values()), nodes)
        hdr = header("THE PROBLEM", CYAN)
        ex = [3, 1, 4]
        ex_edges = path_edges(edges, ex, VIOLET, 9)
        ex_sum = MathTex(r"-4 + 9 + 2 = 7", font_size=50, color=VIOLET).move_to([0, -1.6, 0])
        rule = T("each node used at most once", 26, MUTED).move_to([0, -2.6, 0])

        self.seg(1)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), rt=0.4)
        self.until(DUR[1] * 0.2)
        self.beat(Create(ex_edges), *[restyle(nodes[i], lambda m: m.box.set_stroke(VIOLET, width=5)) for i in ex], rt=0.9)
        self.beat(Write(ex_sum), FadeIn(rule), rt=0.7)
        self.close_seg()

        gold = path_edges(edges, BEST_PATH, YELLOW, 10)
        best = MathTex(r"15 + 20 + 7 = 42", font_size=58, color=YELLOW).move_to([0, -1.6, 0])
        bglow = glow(best, YELLOW, layers=6, max_w=14, max_op=0.28)
        no_root = T("the root is not on it", 28, RED).next_to(nodes[0], UP, buff=0.25)

        self.seg(2)
        self.beat(FadeOut(VGroup(ex_edges, ex_sum, rule)), *[restyle(nodes[i], lambda m: m.box.set_stroke(node_color(VALS[i]), width=3))
                                                           for i in ex], rt=0.4)
        self.beat(FadeIn(no_root), restyle(nodes[0], lambda m: m.set_opacity(0.45)), rt=0.6)
        self.until(DUR[2] * 0.4)
        self.beat(Create(gold), *[restyle(nodes[i], lambda m: m.box.set_stroke(YELLOW, width=5)) for i in BEST_PATH], rt=0.8)
        self.beat(Write(best), FadeIn(bglow), rt=0.8)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        hdr = header("BRUTE FORCE", RED)
        nodes, edges = tree(3.0, dy=1.25, scale=1.0, r=0.4)
        pairs = [(3, 4), (3, 0), (4, 5), (3, 6), (1, 2), (5, 6), (4, 6), (3, 5)]

        def path_between(a, b):
            up_a, x = [a], a
            while NODES[x]["parent"] is not None:
                x = NODES[x]["parent"]
                up_a.append(x)
            up_b, x = [b], b
            while x not in up_a:
                x = NODES[x]["parent"]
                up_b.append(x)
            top = up_b[-1]
            return up_a[:up_a.index(top) + 1] + list(reversed(up_b[:-1]))

        o, o_lab, o_glow = big_o(r"O(n^2)\ \text{pairs}", RED, -2.6, "far too slow", size=70)

        self.seg(3)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(VGroup(*edges.values())), FadeIn(nodes), rt=0.5)
        hi = path_edges(edges, path_between(*pairs[0]), RED, 8)
        self.beat(Create(hi), rt=0.25)
        for a, b in pairs[1:]:
            self.beat(Transform(hi, path_edges(edges, path_between(a, b), RED, 8)), rt=0.25)
        self.beat(Write(o), FadeIn(o_glow), FadeIn(o_lab), rt=0.7)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        hdr = header("THE KEY IDEA", YELLOW)
        nodes, edges = tree(3.2, dy=1.3, scale=1.0, r=0.42)
        sub = VGroup(nodes[2], nodes[5], nodes[6], edges[5], edges[6])
        rest = VGroup(*[nodes[i] for i in (0, 1, 3, 4)], *[edges[i] for i in (1, 2, 3, 4)])
        top_lab = T("top of the path", 26, YELLOW).next_to(nodes[2], UP, buff=0.25)
        lb = path_edges(edges, [5, 2], CYAN, 9)
        rb = path_edges(edges, [2, 6], MAGENTA, 9)
        formula = MathTex(r"\text{path} = \text{val} + L + R", font_size=56, color=YELLOW).move_to([0, -1.2, 0])

        self.seg(4)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(rest), FadeIn(sub), rt=0.5)
        self.until(DUR[4] * 0.2)
        self.beat(rest.animate.set_opacity(0.3), restyle(nodes[2], lambda m: m.box.set_stroke(YELLOW, width=6)), FadeIn(top_lab), rt=0.7)
        self.until(DUR[4] * 0.5)
        self.beat(Create(lb), rt=0.6)
        self.until(DUR[4] * 0.75)
        self.beat(Create(rb), rt=0.6)
        self.beat(Write(formula), rt=0.8)
        self.close_seg()

        up = Arrow(nodes[2].get_top() + UP * 0.05, nodes[0].get_bottom() + DOWN * 0.05, buff=0.1, color=GREEN, stroke_width=7)
        ret = MathTex(r"\text{report up: val} + \max(L, R)", font_size=50, color=GREEN).move_to([0, -2.4, 0])
        bend = T("one branch only, a path bends once", 26, MUTED).move_to([0, -3.3, 0])

        self.seg(5)
        self.beat(rest.animate.set_opacity(1), FadeOut(top_lab), rt=0.5)
        self.beat(GrowArrow(up), FadeOut(rb), rt=0.7)
        self.beat(Write(ret), rt=0.9)
        self.until(DUR[5] * 0.6)
        self.beat(FadeIn(bend, shift=UP * 0.2), rt=0.5)
        self.close_seg()

        neg = nodes[3]
        cross = Cross(neg, stroke_color=RED, stroke_width=6).scale(0.8)
        zero = M("0", 34, MUTED).next_to(neg, DOWN, buff=0.2)
        clamp = MathTex(r"L = \max(\text{gain}, 0)", font_size=50, color=RED).move_to([0, -4.4, 0])

        self.seg(6)
        self.beat(Indicate(neg, color=RED, scale_factor=1.15), rt=0.6)
        self.beat(Create(cross), FadeIn(zero, shift=DOWN * 0.2), rt=0.6)
        self.beat(Write(clamp), rt=0.8)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        hdr = header("POST-ORDER DFS", YELLOW)
        code = code_panel(CODE, -4.1, max_h=3.6)

        def readout(node, path, best):
            parts = VGroup(pill(f"node {node}", CYAN, 26), pill(f"path {path}", YELLOW, 26), pill(f"best {best}", GREEN, 26))
            return parts.arrange(RIGHT, buff=0.25).move_to([0, -1.75, 0])

        st = {"node": "-", "path": "-", "best": "-inf"}
        ro = readout("-", "-", "-inf")
        bar = line_bar(code, 1)
        ev = []
        for k, e in enumerate(TRACE):
            for kind in ("visit", "path", "best", "ret", "drop"):
                if f"t_{kind}" in e:
                    ev.append((seg_time(WALK["first"], e[f"t_{kind}"]), kind, k))
        ev.append((seg_time(WALK["first"], WALK["final"]), "final", 0))
        ev.sort(key=lambda x: x[0])

        def intro():
            self.until(0.2)
            self.beat(FadeIn(hdr, shift=RIGHT * 0.3), rt=0.4)
            self.until(0.6)
            self.beat(FadeIn(code, shift=UP * 0.3), FadeIn(ro), rt=0.7)
            self.beat(FadeIn(bar), rt=0.3)
            self.until(2.0)
            self.beat(Transform(bar, line_bar(code, 9)), rt=0.3)

        def on(kind, k):
            e = TRACE[k]
            if kind == "visit":
                st["node"], st["path"] = e["val"], "-"
                leaf = e["lkid"] is None and e["rkid"] is None
                self.beat(Transform(bar, line_bar(code, 4) if leaf else line_bar(code, 5, 6)),
                          Transform(ro, readout(st["node"], st["path"], st["best"])), rt=0.3)
            elif kind == "path":
                st["path"] = e["path"]
                self.beat(Transform(bar, line_bar(code, 7, 7, YELLOW)), Transform(ro, readout(st["node"], st["path"], st["best"])), rt=0.3)
            elif kind == "best":
                st["best"] = e["best"]
                self.beat(Transform(bar, line_bar(code, 7, 7, GREEN)), Transform(ro, readout(st["node"], st["path"], st["best"])), rt=0.3)
            elif kind == "ret":
                self.beat(Transform(bar, line_bar(code, 8, 8, CYAN)), rt=0.3)
            elif kind == "drop":
                self.beat(Transform(bar, line_bar(code, 5, 5, RED)), rt=0.3)
            elif kind == "final":
                self.beat(Transform(bar, line_bar(code, 10, 10, GREEN)), rt=0.3)

        def outro():
            self.finish(FadeOut(VGroup(hdr, ro, code, bar)), rt=0.5)

        self.run_events(WALK, ev, on, intro, outro)


class Scene6_Complexity(Base):
    def construct(self):
        hdr = header("COMPLEXITY", GREEN)
        nodes, edges = tree(3.6, dy=1.1, scale=0.85, r=0.36)
        o, o_lab, o_glow = big_o(r"O(n)", GREEN, 0.0, "time")

        self.seg(13)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(VGroup(*edges.values())), FadeIn(nodes), rt=0.5)
        self.beat(LaggedStart(*[ring(nodes[e["node"]].box, YELLOW) for e in TRACE], lag_ratio=0.12), rt=1.2)
        self.beat(Write(o), FadeIn(o_glow), FadeIn(o_lab), rt=0.8)
        self.close_seg()

        stack = VGroup(*[RoundedRectangle(corner_radius=0.1, width=2.6, height=0.5, fill_color=PANEL, fill_opacity=1,
                                          stroke_color=VIOLET, stroke_width=2) for _ in range(3)]).arrange(UP, buff=0.08)
        labels = VGroup(*[M(f"gain({v})", 22, VIOLET) for v in (-10, 20, 15)])
        for b, l in zip(stack, labels):
            l.move_to(b)
        stk = VGroup(stack, labels).move_to([-2.2, -3.2, 0])
        h_brace = Brace(stack, RIGHT, color=VIOLET, buff=0.1)
        so, so_lab, so_glow = big_o(r"O(h)", VIOLET, -3.0, "space, h = height", size=72)
        VGroup(so, so_lab, so_glow).shift(RIGHT * 1.6)

        self.seg(14)
        self.beat(LaggedStart(*[FadeIn(VGroup(b, l), shift=DOWN * 0.3) for b, l in zip(stack, labels)], lag_ratio=0.25), GrowFromCenter(h_brace), rt=0.9)
        self.beat(Write(so), FadeIn(so_glow), FadeIn(so_lab), rt=0.8)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.0)
        cglow = glow(code.background, VIOLET, max_w=22, max_op=0.25)
        bar = line_bar(code, 8, 8, CYAN)

        self.seg(15)
        self.beat(FadeIn(code.background), FadeIn(cglow), rt=0.3)
        self.beat(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.06),
                  FadeIn(code.line_numbers), rt=0.8)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(DUR[15] * 0.55)
        self.beat(Transform(bar, line_bar(code, 7, 7, YELLOW)), rt=0.4)
        self.close_seg()

        tag = VGroup(T("Bend once.", 66), T("Keep the best.", 66)).arrange(DOWN, buff=0.15)
        tag.set_color_by_gradient(CYAN, VIOLET, MAGENTA).move_to([0, 0.8, 0])
        tag_glow = glow(tag, VIOLET, layers=6, max_w=18, max_op=0.22)
        title, tglow, art = cover()

        self.seg(16)
        self.beat(FadeOut(VGroup(code, cglow, bar), shift=UP * 0.4), FadeIn(tag), FadeIn(tag_glow), rt=0.5)
        self.hold(0.3)
        # Morph into the opening frame so the loop closes seamlessly
        self.finish(ReplacementTransform(tag, title), FadeOut(tag_glow), FadeIn(tglow), FadeIn(art, shift=UP * 0.3), rt=1.1)
        self.add(tglow, title, art)
        self.close_seg()
