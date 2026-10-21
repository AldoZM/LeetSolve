from manim import *
import math
import random

FPS = 30
config.pixel_width, config.pixel_height = 1080, 1440
config.frame_width, config.frame_height = 9, 12
config.frame_rate = FPS

# Palette shared with the three.js scene
BG = "#0B0E1A"
PANEL = "#141B2F"
CODE_BG = "#11162A"
CYAN = "#22D3EE"
MAGENTA = "#F472B6"
YELLOW = "#FACC15"
GREEN = "#34D399"
RED = "#F87171"
VIOLET = "#A78BFA"
MUTED = "#64748B"
INK = "#E2E8F0"
ARROW = "#8291AD"

L1 = [2, 4, 9]
L2 = [5, 6, 4, 9]
STEPS = []
_carry = 0
for _k in range(5):
    _a = L1[_k] if _k < len(L1) else None
    _b = L2[_k] if _k < len(L2) else None
    _total = (_a or 0) + (_b or 0) + _carry
    STEPS.append({"k": _k, "a": _a, "b": _b, "cin": _carry, "total": _total, "digit": _total % 10, "cout": _total // 10})
    _carry = _total // 10
RESULT = [s["digit"] for s in STEPS]

# Must match STEP_B in three/walk.html: when the digits start flying in each step
STEP_B = [0.7, 0.7, 1.2, 2.4, 2.4]

TOP_Y = 5.4

ADD_CODE = """def addTwoNumbers(l1, l2):
    dummy = tail = ListNode()
    carry = 0
    while l1 or l2 or carry:
        a = l1.val if l1 else 0
        b = l2.val if l2 else 0
        carry, digit = divmod(a + b + carry, 10)
        tail.next = ListNode(digit)
        tail = tail.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next"""


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
    # Animate the whole node while changing only part of it; animating just the box lets Manim draw it over the text
    return ApplyFunction(lambda x: (fn(x), x)[1], m)


def pill(text, color, size=24):
    label = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.2, width=label.width + 0.5, height=label.height + 0.3,
                           fill_color=color, fill_opacity=0.12, stroke_color=color, stroke_width=2)
    return VGroup(box, label.move_to(box))


def header(text, color):
    return pill(text, color, 22).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def dot_grid():
    return VGroup(*[Dot([x, y, 0], radius=0.016, color=MUTED, fill_opacity=0.35)
                    for x in np.arange(-4.2, 4.3, 0.6) for y in np.arange(-5.7, 5.8, 0.6)])


class LNode(VGroup):
    def __init__(self, value, color, size=0.95, **kwargs):
        super().__init__(**kwargs)
        self.box = RoundedRectangle(corner_radius=0.14, width=size, height=size, fill_color=PANEL,
                                    fill_opacity=1, stroke_color=color, stroke_width=3)
        self.num = M(str(value), int(38 * size / 0.95)).move_to(self.box)
        self.add(self.box, self.num)


class LList(VGroup):
    """Linked list drawn left to right: nodes, arrows and a trailing null."""

    def __init__(self, values, color, y, x0=-3.0, step=1.55, size=0.95, null=True, **kwargs):
        super().__init__(**kwargs)
        self.nodes = VGroup(*[LNode(v, color, size).move_to([x0 + k * step, y, 0]) for k, v in enumerate(values)])
        ends = [n.box.get_right() for n in self.nodes]
        self.null = M("null", int(20 * size / 0.95), MUTED).move_to([x0 + len(values) * step - 0.1, y, 0])
        targets = [n.box.get_left() for n in self.nodes[1:]] + ([self.null.get_left()] if null else [])
        self.arrows = VGroup(*[Arrow(s, e, buff=0.06, stroke_width=3, tip_length=0.14, color=ARROW,
                                     max_tip_length_to_length_ratio=0.4) for s, e in zip(ends, targets)])
        self.add(self.nodes, self.arrows)
        if null:
            self.add(self.null)


def row_label(text, color, y):
    return T(text, 24, color).move_to([-3.95, y, 0])


def make_lists(y1, y2):
    l1 = LList(L1, CYAN, y1)
    l2 = LList(L2, VIOLET, y2)
    labels = VGroup(row_label("l1", CYAN, y1), row_label("l2", VIOLET, y2))
    return l1, l2, labels


def cover():
    # Opening frame and closing frame are the same, so the video loops seamlessly
    title = VGroup(T("Add Two", 96), T("Numbers", 96)).arrange(DOWN, buff=0.08)
    title.set_color_by_gradient(CYAN, VIOLET, MAGENTA).move_to([0, 3.35, 0])
    tglow = glow(title, VIOLET, layers=6, max_w=20, max_op=0.25)
    l1, l2, labels = make_lists(0.2, -1.3)
    return title, tglow, VGroup(l1, l2, labels)


def code_panel(src, y, width=8.4):
    code = Code(code_string=src, language="python", formatter_style="monokai", background="rectangle",
                background_config={"fill_color": CODE_BG, "stroke_color": VIOLET, "stroke_width": 2},
                paragraph_config={"font": "Consolas"})
    code.scale_to_fit_width(width).move_to([0, y, 0])
    return code


def line_bar(code, k0, k1=None, color=YELLOW):
    k1 = k0 if k1 is None else k1
    lines = code.code_lines
    step = abs(lines[1].get_y() - lines[0].get_y())
    top, bottom = lines[k0].get_y() + step / 2, lines[k1].get_y() - step / 2
    bar = Rectangle(width=code.background.width - 0.12, height=(top - bottom) * 0.97, fill_color=color, fill_opacity=0.16,
                    stroke_color=color, stroke_width=1.5)
    return bar.move_to([code.background.get_x(), (top + bottom) / 2, 0])


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

    def seg(self, text, dur):
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


class Scene1_Hook(Base):
    def construct(self):
        title, tglow, lists = cover()
        self.add(tglow, title, lists)
        l1, l2 = lists[0], lists[1]

        rng = random.Random(11)
        digits = VGroup(*[
            M(str(rng.randint(0, 9)), rng.randint(18, 36), rng.choice([CYAN, MAGENTA, VIOLET])).set_opacity(rng.uniform(0.12, 0.28))
            .move_to([rng.uniform(-4.1, 4.1), rng.choice([rng.uniform(-5.6, -3.0), rng.uniform(4.9, 5.7), rng.uniform(1.25, 1.75)]), 0])
            for _ in range(26)
        ])
        tags = VGroup(pill("LeetCode #2", CYAN, 26), pill("Medium", YELLOW, 26)).arrange(RIGHT, buff=0.3)
        tags2 = pill("Linked lists", VIOLET, 26)
        tag_block = VGroup(tags, tags2).arrange(DOWN, buff=0.25).move_to([0, -3.7, 0])

        self.seg("Add Two Numbers. Problem number two on LeetCode, and the classic linked list warm up.", 5.85)
        self.beat(Indicate(title, color=WHITE, scale_factor=1.06), rt=0.7)
        self.beat(LaggedStart(*[FadeIn(d, scale=0.4) for d in digits], lag_ratio=0.04),
                  LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in [*tags, tags2]], lag_ratio=0.3), rt=1.2)
        self.beat(LaggedStart(*[ring(n.box, CYAN) for n in l1.nodes], *[ring(n.box, VIOLET) for n in l2.nodes], lag_ratio=0.12), rt=1.3)
        self.hold(1.0)
        self.beat(FadeOut(VGroup(title, tglow, tag_block, digits)), lists.animate.shift(UP * 2.8), rt=0.8)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        l1, l2, labels = make_lists(3.0, 1.5)
        self.add(l1, l2, labels)
        hdr = header("THE PROBLEM", CYAN)

        # Anatomy of one node: a value and a pointer to the next node
        cell_v = Rectangle(width=1.5, height=1.3, fill_color=PANEL, fill_opacity=1, stroke_color=CYAN, stroke_width=3)
        cell_n = Rectangle(width=1.5, height=1.3, fill_color=PANEL, fill_opacity=1, stroke_color=CYAN, stroke_width=3)
        cells = VGroup(cell_v, cell_n).arrange(RIGHT, buff=0).move_to([-0.9, -1.3, 0])
        val = M("2", 60, INK).move_to(cell_v)
        dot = Dot(cell_n.get_center(), radius=0.1, color=ARROW)
        out = Arrow(dot.get_center(), dot.get_center() + RIGHT * 2.1, buff=0, stroke_width=4, color=ARROW, tip_length=0.2)
        nxt = T("next node", 24, MUTED).next_to(out, RIGHT, buff=0.1)
        cap_v = T("val", 26, MUTED).next_to(cell_v, DOWN, buff=0.18)
        cap_n = T("next", 26, MUTED).next_to(cell_n, DOWN, buff=0.18)
        anatomy = VGroup(cells, val, dot, out, nxt, cap_v, cap_n)
        anatomy_title = T("one node", 26, CYAN).next_to(cells, UP, buff=0.25).align_to(cells, LEFT)
        anatomy.add(anatomy_title)

        self.seg("You get two linked lists, and each one stores a number, one digit per node.", 4.75)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), rt=0.5)
        self.beat(LaggedStart(*[ring(n.box, CYAN) for n in l1.nodes], lag_ratio=0.15), rt=0.8)
        self.beat(LaggedStart(*[ring(n.box, VIOLET) for n in l2.nodes], lag_ratio=0.15), rt=0.8)
        self.beat(FadeIn(anatomy, shift=UP * 0.3), rt=0.8)
        self.close_seg()

        places = ["ones", "tens", "hundreds", "thousands"]
        place_labels = VGroup(*[T(p, 18, MUTED).move_to([-3.0 + k * 1.55, 3.85, 0]) for k, p in enumerate(places)])
        place_labels[0].set_color(YELLOW)
        ones = [l1.nodes[0], l2.nodes[0]]

        self.seg("The digits are stored in reverse order, so the ones digit comes first.", 4.5)
        self.beat(FadeOut(anatomy, shift=DOWN * 0.3), rt=0.4)
        self.beat(LaggedStart(*[FadeIn(p, shift=DOWN * 0.15) for p in place_labels], lag_ratio=0.25), rt=1.2)
        self.beat(*[restyle(n, lambda x: x.box.set_stroke(YELLOW, width=5)) for n in ones], ring(l1.nodes[0].box, YELLOW),
                  ring(l2.nodes[0].box, YELLOW), rt=0.7)
        self.close_seg()

        def reading(values, color, y, name):
            lab = T(f"{name}  =", 40, color)
            digs = VGroup(*[M(str(v), 60, color) for v in reversed(values)]).arrange(RIGHT, buff=0.08)
            row = VGroup(lab, digs).arrange(RIGHT, buff=0.3).move_to([0, y, 0])
            return lab, digs

        lab1, digs1 = reading(L1, CYAN, -0.4, "l1")
        lab2, digs2 = reading(L2, VIOLET, -1.9, "l2")
        n = len(L1)
        fly1 = [l1.nodes[k].num.copy() for k in range(n)]
        fly2 = [l2.nodes[k].num.copy() for k in range(len(L2))]

        self.seg("So this list is nine hundred forty two, and this one is nine thousand four hundred sixty five.", 6.15)
        self.beat(restyle(ones[0], lambda x: x.box.set_stroke(CYAN, width=3)),
                  restyle(ones[1], lambda x: x.box.set_stroke(VIOLET, width=3)), FadeIn(lab1), rt=0.4)
        self.beat(*[f.animate.move_to(digs1[n - 1 - k]).set_color(CYAN).scale(60 / 38) for k, f in enumerate(fly1)], rt=1.3)
        self.until(2.6)
        self.beat(FadeIn(lab2), rt=0.3)
        self.beat(*[f.animate.move_to(digs2[len(L2) - 1 - k]).set_color(VIOLET).scale(60 / 38) for k, f in enumerate(fly2)], rt=1.4)
        self.close_seg()

        eq = VGroup(M("942", 50, CYAN), M("+", 50, MUTED), M("9465", 50, VIOLET), M("=", 50, MUTED), M("10407", 50, YELLOW))
        eq.arrange(RIGHT, buff=0.22).move_to([0, -3.2, 0])
        res = LList(RESULT, GREEN, -4.5, x0=-3.0, step=1.3, size=0.8)
        res_lab = row_label("sum", GREEN, -4.5)

        self.seg("Return their sum as a linked list, in the same reversed order.", 4.075)
        self.beat(FadeIn(eq, shift=UP * 0.2), rt=0.6)
        self.beat(FadeIn(res_lab), LaggedStart(*[GrowFromCenter(nd) for nd in res.nodes], lag_ratio=0.15),
                  LaggedStart(*[GrowArrow(a) for a in res.arrows], lag_ratio=0.15), FadeIn(res.null), rt=1.4)
        self.hold(1.2)
        self.beat(FadeOut(Group(*self.mobjects[1:])), rt=0.5)
        self.close_seg()


class Scene3_Shortcut(Base):
    def construct(self):
        hdr = header("SHORTCUT?", RED)
        code = M("int(l1) + int(l2)", 46, INK).move_to([0, 3.6, 0])
        code[4:6].set_color(CYAN)
        code[12:14].set_color(VIOLET)
        eq = VGroup(M("942", 50, CYAN), M("+", 50, MUTED), M("9465", 50, VIOLET), M("=", 50, MUTED), M("10407", 50, YELLOW))
        eq.arrange(RIGHT, buff=0.22).move_to([0, 2.2, 0])
        ok = T("✓  works for small numbers", 30, GREEN).move_to([0, 1.1, 0])

        self.seg("The tempting shortcut is to turn both lists into integers and just add them.", 5.1)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), rt=0.5)
        self.beat(Write(code), rt=1.0)
        self.beat(FadeIn(eq, shift=UP * 0.2), rt=0.8)
        self.beat(FadeIn(ok, scale=1.2), rt=0.5)
        self.close_seg()

        rng = random.Random(5)
        cs = 0.56
        cells = VGroup()
        for r in range(10):
            for c in range(10):
                box = RoundedRectangle(corner_radius=0.06, width=cs, height=cs, fill_color=PANEL, fill_opacity=1,
                                       stroke_color=VIOLET, stroke_width=1.5)
                box.move_to([(c - 4.5) * (cs + 0.08), 0.3 - (r - 4.5) * (cs + 0.08), 0])
                cells.add(VGroup(box, M(str(rng.randint(0, 9)), 20, INK).move_to(box)))
        caption = T("one list, 100 digits", 28, VIOLET).next_to(cells, UP, buff=0.25)
        fits = cells[:19]
        spill = cells[19:]
        fit_lab = T("a 64-bit integer holds 19 digits", 24, GREEN).next_to(cells, DOWN, buff=0.3)
        stamp = T("OVERFLOW", 88, RED).rotate(-10 * DEGREES).move_to([0, -4.3, 0])
        sglow = glow(stamp, RED, layers=6, max_w=18, max_op=0.3)

        self.seg("But a list can hold a hundred digits. That overflows any normal integer type.", 5.325)
        self.beat(FadeOut(VGroup(code, eq, ok), shift=UP * 0.3), FadeIn(caption), rt=0.5)
        self.beat(LaggedStart(*[FadeIn(c, scale=0.6) for c in cells], lag_ratio=0.012), rt=1.4)
        self.beat(*[restyle(c, lambda x: x[0].set_stroke(GREEN, width=2.5)) for c in fits], FadeIn(fit_lab, shift=UP * 0.2), rt=0.6)
        self.beat(LaggedStart(*[restyle(c, lambda x: x[0].set_stroke(RED).set_fill(RED, opacity=0.35)) for c in spill], lag_ratio=0.01),
                  FadeOut(fit_lab), rt=0.9)
        self.beat(FadeIn(sglow), FadeIn(stamp, scale=1.6), rt=0.5)
        self.hold(0.8)
        self.beat(FadeOut(Group(*self.mobjects[1:])), rt=0.5)
        self.close_seg()


class Scene4_Insight(Base):
    def construct(self):
        hdr = header("THE TRICK", YELLOW)
        xs = [2.4, 1.4, 0.4, -0.6, -1.6]  # column x by place: ones, tens, ...
        Y_CARRY, Y_A, Y_B, Y_LINE, Y_R = 3.0, 2.1, 1.0, 0.35, -0.4
        top = VGroup(*[M(str(d), 64, CYAN).move_to([xs[k], Y_A, 0]) for k, d in enumerate(L1)])
        bot = VGroup(*[M(str(d), 64, VIOLET).move_to([xs[k], Y_B, 0]) for k, d in enumerate(L2)])
        plus = M("+", 64, MUTED).move_to([-2.7, Y_B, 0])
        line = Line([-3.1, Y_LINE, 0], [2.9, Y_LINE, 0], color=MUTED, stroke_width=3)
        beam = RoundedRectangle(corner_radius=0.15, width=0.9, height=Y_CARRY - Y_R + 0.9, fill_color=YELLOW,
                                fill_opacity=0.08, stroke_color=YELLOW, stroke_width=2)
        beam.move_to([xs[0], (Y_CARRY + Y_R) / 2, 0])
        start = Arrow([3.6, -1.35, 0], [-2.4, -1.35, 0], buff=0, color=YELLOW, stroke_width=5, tip_length=0.25)
        start_lab = T("start at the ones place", 26, YELLOW).next_to(start, DOWN, buff=0.15)
        mini = LList(L1, CYAN, -3.6, x0=-2.2, step=1.3, size=0.8)
        mini_lab = row_label("l1", CYAN, -3.6).shift(RIGHT * 0.6)
        mini_cap = T("the list already starts there", 24, MUTED).next_to(mini, DOWN, buff=0.3)

        self.seg("Here's the good news. Reverse order is exactly how we add by hand, starting from the ones place.", 6.55)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), rt=0.5)
        self.beat(LaggedStart(*[FadeIn(m, shift=DOWN * 0.2) for m in [*reversed(top), plus, *reversed(bot)]], lag_ratio=0.08),
                  Create(line), rt=1.2)
        self.until(3.4)
        self.beat(GrowArrow(start), FadeIn(start_lab), FadeIn(beam), rt=0.9)
        self.beat(FadeIn(mini_lab), FadeIn(mini, shift=UP * 0.2), rt=0.6)
        self.beat(restyle(mini.nodes[0], lambda x: x.box.set_stroke(YELLOW, width=5)), FadeIn(mini_cap), rt=0.5)
        self.close_seg()

        self.seg("Add each column, write down the last digit, and carry the rest to the next column.", 5.2)
        self.beat(FadeOut(VGroup(start, start_lab, mini, mini_lab, mini_cap)), rt=0.4)
        carries = []
        for s in STEPS:
            k = s["k"]
            anims = [beam.animate.move_to([xs[k], (Y_CARRY + Y_R) / 2, 0])] if k > 0 else []
            digit = M(str(s["digit"]), 64, GREEN).move_to([xs[k], Y_R, 0])
            self.beat(*anims, FadeIn(digit, shift=DOWN * 0.3), rt=0.45)
            if s["cout"]:
                c = M("1", 34, MAGENTA).move_to([xs[k + 1], Y_CARRY, 0])
                self.beat(FadeIn(c, shift=UP * 0.3, scale=0.5), rt=0.3)
                carries.append(c)
            else:
                self.hold(0.3)
        self.beat(FadeOut(Group(*self.mobjects[1:])), rt=0.5)
        self.close_seg()


class Scene5_Walk(Base):
    """Transparent overlay composited on top of the three.js walkthrough (render with -t)."""

    def setup(self):
        pass

    def construct(self):
        hdr = header("WALK BOTH LISTS", YELLOW)
        code = code_panel(ADD_CODE, -3.75)

        def carry_pill(v):
            return pill(f"carry {v}", MAGENTA if v else MUTED, 26).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)

        badge = carry_pill(0)
        bar = line_bar(code, 1, 2, YELLOW)

        def readout(s):
            a = M(str(s["a"] if s["a"] is not None else 0), 52, CYAN if s["a"] is not None else MUTED)
            b = M(str(s["b"] if s["b"] is not None else 0), 52, VIOLET if s["b"] is not None else MUTED)
            parts = VGroup(a, M("+", 52, MUTED), b, M("+", 52, MUTED), M(str(s["cin"]), 52, MAGENTA),
                           M("=", 52, MUTED), M(str(s["total"]), 52, YELLOW))
            return parts.arrange(RIGHT, buff=0.22).move_to([0, -1.05, 0])

        self.seg("So we walk both lists together, one node at a time, keeping a carry.", 4.425)
        self.until(0.3)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(badge), rt=0.5)
        self.until(1.2)
        self.beat(FadeIn(code, shift=UP * 0.3), rt=0.8)
        self.until(2.4)
        self.beat(FadeIn(bar), rt=0.4)
        self.close_seg()

        texts = [
            ("First column. Two plus five is seven, and there's no carry.", 4.0),
            ("Next, four plus six is ten. We write a zero, and carry the one.", 4.45),
            ("Then nine plus four, plus the carry, is fourteen. Write four, carry one.", 4.75),
            ("The first list has run out, so it counts as zero. Nine plus one is ten. Write zero, carry one.", 6.3),
            ("Both lists are finished, but the carry is still one. So we add one final node.", 5.125),
        ]
        ro = None
        for s, (text, dur) in zip(STEPS, texts):
            b = STEP_B[s["k"]]
            self.seg(text, dur)
            self.beat(Transform(bar, line_bar(code, 3, 3, YELLOW)), *([FadeOut(ro)] if ro else []), rt=0.35)
            self.until(b)
            self.beat(Transform(bar, line_bar(code, 4, 5, YELLOW)), rt=0.3)
            self.until(b + 0.9)
            ro = readout(s)
            self.beat(Transform(bar, line_bar(code, 6, 6, YELLOW)), FadeIn(ro, scale=1.2), rt=0.35)
            if s["cout"] != s["cin"]:
                self.until(b + 1.2)
                self.beat(Transform(badge, carry_pill(s["cout"])), rt=0.3)
            self.until(b + 1.7)
            self.beat(Transform(bar, line_bar(code, 7, 8, GREEN)), rt=0.3)
            self.until(b + 2.3)
            self.beat(Transform(bar, line_bar(code, 9, 10, YELLOW)), rt=0.3)
            self.close_seg()

        chain = VGroup()
        for k, d in enumerate(RESULT):
            chain.add(M(str(d), 52, GREEN))
            if k < len(RESULT) - 1:
                chain.add(M("→", 40, MUTED))
        chain.arrange(RIGHT, buff=0.2).move_to([0, -1.05, 0])
        number = VGroup(M("=", 52, MUTED), M("10407", 60, YELLOW)).arrange(RIGHT, buff=0.3).move_to([0, -1.05, 0])
        dur = 6.075

        self.seg("The result reads seven, zero, four, zero, one. That's ten thousand four hundred seven.", dur)
        self.beat(Transform(bar, line_bar(code, 3, 3, YELLOW)), FadeOut(ro), rt=0.35)
        self.until(0.6)
        self.beat(Transform(bar, line_bar(code, 11, 11, GREEN)), rt=0.3)
        self.until(1.2)
        self.beat(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in chain], lag_ratio=0.25), rt=2.3)
        self.until(3.9)
        self.beat(FadeOut(chain, shift=UP * 0.3), FadeIn(number, shift=UP * 0.3), rt=0.5)
        self.until(dur - 0.55)
        self.beat(FadeOut(VGroup(hdr, badge, code, bar, number)), rt=0.5)
        self.close_seg()


class Scene6_Complexity(Base):
    def construct(self):
        hdr = header("COMPLEXITY", GREEN)
        a = LList(L1, CYAN, 3.4, x0=-2.6, step=1.15, size=0.7, null=False)
        b = LList(L2, VIOLET, 2.2, x0=-2.6, step=1.15, size=0.7, null=False)
        la = T("m = 3", 26, CYAN).next_to(a, RIGHT, buff=0.4)
        lb = T("n = 4", 26, VIOLET).next_to(b, RIGHT, buff=0.4)
        runner = Dot(radius=0.11, color=YELLOW).move_to(b.nodes[0].get_bottom() + DOWN * 0.3)
        time_o = MathTex(r"O(\max(m, n))", font_size=80, color=GREEN).move_to([0, 0.3, 0])
        time_l = T("time", 30, MUTED).next_to(time_o, DOWN, buff=0.15)
        tglow = glow(time_o, GREEN, layers=6, max_w=14, max_op=0.3)

        self.seg("Each node is visited once, so the time is linear in the length of the longer list.", 5.175)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(a), FadeIn(b), rt=0.7)
        self.beat(FadeIn(la), FadeIn(lb), FadeIn(runner), rt=0.4)
        self.beat(runner.animate.move_to(b.nodes[-1].get_bottom() + DOWN * 0.3),
                  LaggedStart(*[restyle(n, lambda x: x.box.set_fill(YELLOW, opacity=0.25)) for n in b.nodes], lag_ratio=0.25), rt=1.5)
        self.beat(Write(time_o), FadeIn(tglow), FadeIn(time_l), rt=0.9)
        self.close_seg()

        res = LList(RESULT, GREEN, -1.9, x0=-2.6, step=1.15, size=0.7, null=False)
        space_o = MathTex(r"O(\max(m, n))", font_size=64, color=VIOLET).move_to([0, -3.4, 0])
        space_l = T("extra space", 28, MUTED).next_to(space_o, DOWN, buff=0.15)

        self.seg("And the new list takes the same amount of extra space.", 3.45)
        self.beat(LaggedStart(*[GrowFromCenter(n) for n in res.nodes], lag_ratio=0.12),
                  LaggedStart(*[GrowArrow(x) for x in res.arrows], lag_ratio=0.12), rt=0.9)
        self.beat(FadeIn(space_o, shift=UP * 0.2), FadeIn(space_l), rt=0.6)
        self.hold(1.2)
        self.beat(FadeOut(Group(*self.mobjects[1:])), rt=0.5)
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(ADD_CODE, 1.0)
        cglow = glow(code.background, VIOLET, max_w=22, max_op=0.25)
        bar = line_bar(code, 3, 3, CYAN)

        self.seg("One loop, one carry, and a dummy head to keep the code clean.", 4.1)
        self.beat(FadeIn(code.background), FadeIn(cglow), rt=0.3)
        self.beat(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08),
                  FadeIn(code.line_numbers), rt=0.8)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(1.4)
        self.beat(Transform(bar, line_bar(code, 6, 6, MAGENTA)), rt=0.4)
        self.until(2.3)
        self.beat(Transform(bar, line_bar(code, 1, 1, YELLOW)), rt=0.4)
        self.until(3.3)
        self.beat(Transform(bar, line_bar(code, 0, 11, GREEN)), rt=0.5)
        self.close_seg()

        tag = VGroup(T("Reverse order is", 60), T("grade school", 60), T("addition.", 60)).arrange(DOWN, buff=0.15)
        tag.set_color_by_gradient(CYAN, VIOLET, MAGENTA).move_to([0, 0.8, 0])
        tag_glow = glow(tag, VIOLET, layers=6, max_w=18, max_op=0.22)
        title, tglow, lists = cover()

        self.seg("Reverse order turns linked lists into grade school addition.", 3.975)
        self.beat(FadeOut(VGroup(code, cglow, bar), shift=UP * 0.4), rt=0.4)
        self.beat(Write(tag), FadeIn(tag_glow), rt=1.0)
        self.hold(0.5)
        # Morph into the opening frame so the loop closes seamlessly
        self.beat(ReplacementTransform(tag, title), FadeOut(tag_glow), FadeIn(tglow),
                  FadeIn(lists, shift=UP * 0.3), rt=1.1)
        self.add(tglow, title, lists)
        self.close_seg()
