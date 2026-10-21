from manim import *
import math
import random

FPS = 30
config.pixel_width, config.pixel_height = 1080, 1440
config.frame_width, config.frame_height = 9, 12
config.frame_rate = FPS

# Palette: deep navy with neon accents
BG = "#0B0E1A"
PANEL = "#141B2F"
PANEL2 = "#1B2340"
CODE_BG = "#11162A"
CYAN = "#22D3EE"
MAGENTA = "#F472B6"
YELLOW = "#FACC15"
GREEN = "#34D399"
RED = "#F87171"
VIOLET = "#A78BFA"
MUTED = "#64748B"
INK = "#E2E8F0"

NUMS = [5, 12, 1, 14, 8, 15]
TARGET = 23
ANS = (4, 5)

TOP_Y = 5.4      # header row
ARR_Y = 3.85     # array row while solving

BRUTE_CODE = """def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]"""

HASH_CODE = """def twoSum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i"""


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


def pill(text, color, size=24):
    label = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.2, width=label.width + 0.5, height=label.height + 0.3,
                           fill_color=color, fill_opacity=0.12, stroke_color=color, stroke_width=2)
    return VGroup(box, label.move_to(box))


def ring(m, color, width=8):
    # Light that travels around a shape's border without touching its fill
    return ShowPassingFlash(m.copy().set_fill(opacity=0).set_stroke(color, width=width), time_width=0.5)


def header(text, color):
    return pill(text, color, 22).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def dot_grid():
    return VGroup(*[Dot([x, y, 0], radius=0.016, color=MUTED, fill_opacity=0.35)
                    for x in np.arange(-4.2, 4.3, 0.6) for y in np.arange(-5.7, 5.8, 0.6)])


class Cell(VGroup):
    def __init__(self, value, index, size=1.0, **kwargs):
        super().__init__(**kwargs)
        self.box = RoundedRectangle(corner_radius=0.15, width=size, height=size, fill_color=PANEL,
                                    fill_opacity=1, stroke_color=CYAN, stroke_width=3)
        self.num = M(str(value), int(40 * size)).move_to(self.box)
        self.idx = T(str(index), int(20 * size), MUTED).next_to(self.box, DOWN, buff=0.12)
        self.add(self.box, self.num, self.idx)


def make_array(y, size=1.0, gap=0.25):
    cells = VGroup(*[Cell(v, i, size) for i, v in enumerate(NUMS)])
    for i, c in enumerate(cells):
        c.move_to([(i - 2.5) * (size + gap), y, 0])
    return cells


def target_badge(scale=1.0):
    label = T("target", 26, MUTED)
    val = M(str(TARGET), 50, YELLOW)
    row = VGroup(label, val).arrange(RIGHT, buff=0.3)
    box = RoundedRectangle(corner_radius=0.25, width=row.width + 0.7, height=row.height + 0.4,
                           fill_color=YELLOW, fill_opacity=0.08, stroke_color=YELLOW, stroke_width=2.5)
    return VGroup(glow(box, YELLOW, max_w=18), box, row.move_to(box)).scale(scale)


def corner_badge():
    return target_badge(0.7).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)


def pointer(color, letter):
    tri = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(0.13)
    lab = T(letter, 22, color).next_to(tri, DOWN, buff=0.06)
    return VGroup(tri, lab)


def ptr_pos(cells, k):
    return cells[k].idx.get_bottom() + DOWN * 0.36


def cover():
    # Opening frame and closing frame are the same, so the video loops seamlessly
    title = T("Two Sum", 110).set_color_by_gradient(CYAN, VIOLET, MAGENTA).move_to([0, 3.4, 0])
    tglow = glow(title, VIOLET, layers=6, max_w=20, max_op=0.25)
    cells = make_array(0.2)
    badge = target_badge().move_to([0, -1.9, 0])
    return title, tglow, cells, badge


def code_panel(src, y):
    code = Code(code_string=src, language="python", formatter_style="monokai", background="rectangle",
                background_config={"fill_color": CODE_BG, "stroke_color": VIOLET, "stroke_width": 2},
                paragraph_config={"font": "Consolas"})
    code.scale_to_fit_width(8.2).move_to([0, y, 0])
    return code


def line_bar(code, k, color=YELLOW):
    lines = code.code_lines
    step = abs(lines[1].get_y() - lines[0].get_y())
    bar = Rectangle(width=code.background.width - 0.12, height=step * 0.95, fill_color=color, fill_opacity=0.16,
                    stroke_color=color, stroke_width=1.5)
    return bar.move_to([code.background.get_x(), lines[k].get_y(), 0])


class Base(Scene):
    scene_budget = 0.0
    scene_used = 0.0

    def setup(self):
        self.camera.background_color = BG
        self.add(dot_grid())

    # Manim renders whole frames; keep animations on frame boundaries so audio stays in sync
    def frames(self, t):
        return math.ceil(t * FPS - 1e-6) / FPS

    def seg(self, text, dur):
        self.add_subcaption(text, duration=dur)
        self.scene_budget += dur

    def beat(self, *anims, rt=1.0, **kwargs):
        rt = self.frames(rt)
        self.play(*anims, run_time=rt, **kwargs)
        self.scene_used += rt

    def hold(self, t):
        t = self.frames(t)
        self.wait(t)
        self.scene_used += t

    def close_seg(self):
        rest = self.scene_budget - self.scene_used
        if rest > 0:
            self.wait(rest)
            self.scene_used += rest


class Scene1_Hook(Base):
    def construct(self):
        title, tglow, cells, badge = cover()
        self.add(tglow, title, cells, badge)

        rng = random.Random(7)
        digits = VGroup(*[
            M(str(rng.randint(0, 99)), rng.randint(16, 34), rng.choice([CYAN, MAGENTA, VIOLET])).set_opacity(rng.uniform(0.12, 0.28))
            .move_to([rng.uniform(-4.1, 4.1), rng.choice([rng.uniform(-5.6, -3.0), rng.uniform(4.6, 5.6), rng.uniform(1.3, 2.2)]), 0])
            for _ in range(26)
        ])
        tags = VGroup(pill("LeetCode #1", CYAN, 26), pill("Easy", GREEN, 26)).arrange(RIGHT, buff=0.3)
        tags2 = pill("Interview classic", MAGENTA, 26)
        tag_block = VGroup(tags, tags2).arrange(DOWN, buff=0.25).move_to([0, -3.9, 0])

        self.seg("Two Sum. Problem number one on LeetCode, and an interview classic.", 4.7)
        self.beat(Indicate(title, color=WHITE, scale_factor=1.06), rt=0.7)
        self.beat(LaggedStart(*[FadeIn(d, scale=0.4) for d in digits], lag_ratio=0.04),
                  LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in [*tags, tags2]], lag_ratio=0.3), rt=1.2)
        self.beat(digits.animate.shift(UP * 0.3),
                  LaggedStart(*[ring(c.box, VIOLET) for c in cells], lag_ratio=0.12), rt=1.1)
        self.beat(FadeOut(VGroup(title, tglow, tag_block, digits)),
                  cells.animate.move_to([0, 2.0, 0]), badge.animate.move_to([0, 4.2, 0]), rt=0.8)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        cells = make_array(2.0)
        badge = target_badge().move_to([0, 4.2, 0])
        self.add(cells, badge)
        hdr = header("THE PROBLEM", CYAN)
        nums_label = M("nums", 26, MUTED).next_to(cells, UP, buff=0.2).align_to(cells, LEFT)

        self.seg("You're given an array of integers and a target number.", 3.475)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(nums_label, shift=RIGHT * 0.2), rt=0.6)
        self.beat(LaggedStart(*[AnimationGroup(ring(c.box, CYAN), c.num.animate(rate_func=there_and_back).scale(1.25).set_color(CYAN))
                                for c in cells], lag_ratio=0.12), rt=1.4)
        self.beat(Indicate(badge, color=YELLOW, scale_factor=1.15), rt=0.7)
        self.close_seg()

        eq = VGroup(M("?", 60, MAGENTA), M("+", 60, MUTED), M("?", 60, MAGENTA), M("=", 60, MUTED), M("23", 60, YELLOW))
        eq.arrange(RIGHT, buff=0.3).move_to([0, -0.3, 0])
        a, b = cells[ANS[0]], cells[ANS[1]]
        arc = ArcBetweenPoints(a.box.get_top() + UP * 0.08, b.box.get_top() + UP * 0.08, angle=-PI * 0.7,
                               color=GREEN, stroke_width=5)
        glows = VGroup(glow(a.box, GREEN), glow(b.box, GREEN))
        solved = VGroup(M("8", 60, GREEN), M("+", 60, MUTED), M("15", 60, GREEN), M("=", 60, MUTED),
                        M("23", 60, YELLOW)).arrange(RIGHT, buff=0.3).move_to(eq)
        ret = pill("return [4, 5]", GREEN, 32).move_to([0, -1.5, 0])
        card_lines = VGroup(
            VGroup(T("Input", 24, MUTED), M("nums = [5,12,1,14,8,15]", 24, INK)).arrange(RIGHT, buff=0.25),
            M("target = 23", 24, YELLOW),
            VGroup(T("Output", 24, MUTED), M("[4, 5]", 24, GREEN)).arrange(RIGHT, buff=0.25),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        card_box = RoundedRectangle(corner_radius=0.2, width=card_lines.width + 0.7, height=card_lines.height + 0.6,
                                    fill_color=CODE_BG, fill_opacity=1, stroke_color=MUTED, stroke_width=1.5)
        card = VGroup(card_box, card_lines.move_to(card_box)).move_to([0, -3.8, 0])
        card_lines[1].align_to(card_lines[0][1], LEFT)

        self.seg("Find the two numbers that add up exactly to the target, and return their indices.", 5.325)
        self.beat(Write(eq), FadeIn(card, shift=UP * 0.3), rt=0.9)
        self.beat(a.box.animate.set_stroke(GREEN, width=4), b.box.animate.set_stroke(GREEN, width=4),
                  FadeIn(glows), Create(arc), Transform(eq, solved), rt=1.4)
        self.beat(a.idx.animate.set_color(YELLOW).scale(1.4), b.idx.animate.set_color(YELLOW).scale(1.4),
                  FadeIn(ret, shift=UP * 0.2), rt=0.9)
        self.hold(1.0)
        self.beat(FadeOut(VGroup(eq, ret, arc, glows, nums_label, card, hdr)),
                  a.box.animate.set_stroke(CYAN, width=3), b.box.animate.set_stroke(CYAN, width=3),
                  a.idx.animate.set_color(MUTED).scale(1 / 1.4), b.idx.animate.set_color(MUTED).scale(1 / 1.4), rt=0.4)
        self.beat(cells.animate.move_to([0, ARR_Y, 0]), Transform(badge, corner_badge()), rt=0.5)
        self.close_seg()


class Scene3_BruteForce(Base):
    def construct(self):
        cells = make_array(ARR_Y)
        badge = corner_badge()
        self.add(cells, badge)

        hdr = header("BRUTE FORCE", RED)
        code = code_panel(BRUTE_CODE, -3.95)
        bar = line_bar(code, 0, RED)

        gs = 0.3
        grid = VGroup()
        grid_cells = {}
        for i in range(6):
            for j in range(6):
                sq = Square(gs, stroke_width=1.5, stroke_color=MUTED, stroke_opacity=0.5,
                            fill_color=PANEL, fill_opacity=1 if j > i else 0.2)
                sq.move_to([j * (gs + 0.05), -i * (gs + 0.05), 0])
                grid.add(sq)
                grid_cells[(i, j)] = sq
        grid_title = T("pairs checked", 20, MUTED).next_to(grid, UP, buff=0.15)
        grid_block = VGroup(grid, grid_title).move_to([2.2, -0.2, 0])

        counter = Integer(0, font_size=80, color=RED)
        counter_label = T("checks", 24, MUTED)
        counter_block = VGroup(counter_label, counter).arrange(DOWN, buff=0.12).move_to([-2.2, -0.2, 0])

        pi_ = pointer(MAGENTA, "i")
        pj = pointer(CYAN, "j")

        def readout(i, j):
            s = NUMS[i] + NUMS[j]
            ok = s == TARGET
            parts = VGroup(M(str(NUMS[i]), 50, MAGENTA), M("+", 50, MUTED), M(str(NUMS[j]), 50, CYAN),
                           M("=", 50, MUTED), M(str(s), 50, GREEN if ok else INK),
                           T("✓" if ok else "≠ 23", 38, GREEN if ok else RED))
            return parts.arrange(RIGHT, buff=0.22).move_to([0, 1.55, 0])

        self.seg("The most direct idea is to try every possible pair.", 3.9)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(code, shift=UP * 0.3), rt=0.7)
        self.beat(FadeIn(bar), rt=0.3)
        pi_.move_to(ptr_pos(cells, 0))
        pj.move_to(ptr_pos(cells, 1))
        self.beat(FadeIn(pi_, shift=UP * 0.3), cells[0].box.animate.set_stroke(MAGENTA, width=4),
                  Transform(bar, line_bar(code, 1, RED)), rt=0.5)
        self.beat(FadeIn(pj, shift=UP * 0.3), cells[1].box.animate.set_stroke(CYAN, width=5),
                  Transform(bar, line_bar(code, 2, RED)), rt=0.5)
        self.ro = readout(0, 1)
        grid_cells[(0, 1)].set_fill(RED, opacity=0.8)
        self.beat(FadeIn(self.ro, shift=UP * 0.2), FadeIn(grid_block), FadeIn(counter_block),
                  Transform(bar, line_bar(code, 3, RED)), rt=0.6)
        self.beat(counter.animate.set_value(1), rt=0.3)
        self.close_seg()

        def check(i, j, prev_j, rt, slow=False):
            new_ro = readout(i, j)
            sq = grid_cells[(i, j)]
            hit = NUMS[i] + NUMS[j] == TARGET
            reset = [cells[prev_j].box.animate.set_stroke(CYAN, width=3)] if prev_j not in (i, j) else []
            move = [pi_.animate.move_to(ptr_pos(cells, i)), pj.animate.move_to(ptr_pos(cells, j)), *reset,
                    cells[i].box.animate.set_stroke(MAGENTA, width=4),
                    cells[j].box.animate.set_stroke(CYAN, width=5)]
            compare = [FadeOut(self.ro), FadeIn(new_ro), sq.animate.set_fill(GREEN if hit else RED, opacity=0.85),
                       counter.animate.set_value(counter.get_value() + 1)]
            if slow:
                # j advances on the inner loop line, then the comparison line runs
                self.beat(*move, Transform(bar, line_bar(code, 2, RED)), rt=rt * 0.4)
                self.beat(*compare, Transform(bar, line_bar(code, 3, RED)), rt=rt * 0.6)
            else:
                self.beat(*move, *compare, Transform(bar, line_bar(code, 3, RED)), rt=rt)
            self.ro = new_ro

        self.seg("Fix one number, and add it to every number after it.", 3.575)
        prev = 1
        for j in range(2, 6):
            check(0, j, prev, 0.75, slow=True)
            prev = j
        self.close_seg()

        self.seg("It works, but with just six numbers, that's already fifteen checks.", 4.175)
        for i in range(1, 5):
            self.beat(cells[i - 1].box.animate.set_stroke(CYAN, width=3), Transform(bar, line_bar(code, 1, RED)), rt=0.2)
            for j in range(i + 1, 6):
                check(i, j, prev, 0.22)
                prev = j
        a, b = cells[ANS[0]], cells[ANS[1]]
        self.beat(Transform(bar, line_bar(code, 4, GREEN)), a.box.animate.set_stroke(GREEN, width=5),
                  b.box.animate.set_stroke(GREEN, width=5), Indicate(counter, color=YELLOW, scale_factor=1.5), rt=0.6)
        self.close_seg()

        self.seg("And it grows quadratically. With a million numbers, that's half a trillion pairs.", 5.1)
        everything = VGroup(cells, badge, pi_, pj, self.ro, grid_block, counter_block, code, bar)
        self.beat(FadeOut(everything, shift=DOWN * 0.3), rt=0.5)
        axes = Axes(x_range=[0, 10, 2], y_range=[0, 100, 20], x_length=6.4, y_length=5.0,
                    axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": False}).move_to([-0.3, 1.6, 0])
        xl = T("n", 28, MUTED).next_to(axes.x_axis, RIGHT, buff=0.12)
        yl = T("pairs", 24, MUTED).next_to(axes.y_axis, UP, buff=0.12)
        curve = axes.plot(lambda x: x ** 2, x_range=[0, 10], color=RED, stroke_width=6)
        cglow = glow(curve, RED, layers=6, max_w=22)
        big_o = MathTex(r"O(n^2)", font_size=64, color=RED).next_to(axes.c2p(10, 100), LEFT, buff=0.35)
        stat1 = VGroup(M("1,000,000", 46, INK), T("numbers", 26, MUTED)).arrange(DOWN, buff=0.1)
        arrow = Arrow(UP * 0.4, DOWN * 0.4, color=MUTED, stroke_width=4)
        stat2 = VGroup(M("~500,000,000,000", 44, RED), T("pairs", 26, MUTED)).arrange(DOWN, buff=0.1)
        stats = VGroup(stat1, arrow, stat2).arrange(DOWN, buff=0.25).move_to([0, -3.6, 0])
        self.beat(Create(axes), FadeIn(xl), FadeIn(yl), rt=0.7)
        self.beat(Create(curve), FadeIn(cglow), rt=1.4)
        self.beat(Write(big_o), FadeIn(stat1, shift=UP * 0.3), rt=0.6)
        self.beat(GrowArrow(arrow), FadeIn(stat2, scale=1.3), rt=0.7)
        self.hold(0.6)
        self.beat(FadeOut(VGroup(axes, xl, yl, curve, cglow, big_o, stats, hdr)), rt=0.5)
        self.close_seg()


class Scene4_Insight(Base):
    def construct(self):
        hdr = header("THE TRICK", YELLOW)
        badge = target_badge(1.2).move_to([0, 3.9, 0])

        card = Cell(15, 0, 1.8)
        card.remove(card.idx)
        card.box.set_stroke(MAGENTA, width=5)
        card.move_to([-2.2, 1.3, 0])
        card_lab = T("holding", 26, MAGENTA).next_to(card, DOWN, buff=0.22)

        qbox = DashedVMobject(RoundedRectangle(corner_radius=0.22, width=1.8, height=1.8, color=MUTED, stroke_width=4),
                              num_dashes=26).move_to([2.2, 1.3, 0])
        qmark = M("?", 72, MUTED).move_to(qbox)
        q_lab = T("need", 26, MUTED).next_to(qbox, DOWN, buff=0.22)

        eq_q = M("?", 60, MUTED)
        eq = VGroup(M("23", 60, YELLOW), M("−", 60, MUTED), M("15", 60, MAGENTA), M("=", 60, MUTED), eq_q)
        eq.arrange(RIGHT, buff=0.3).move_to([0, -1.2, 0])

        eight_box = RoundedRectangle(corner_radius=0.22, width=1.8, height=1.8, fill_color=PANEL, fill_opacity=1,
                                     stroke_color=GREEN, stroke_width=5).move_to(qbox)
        eight = M("8", 72, GREEN).move_to(qbox)
        eight_glow = glow(eight_box, GREEN, max_w=30, max_op=0.4)
        eq_eight = M("8", 60, GREEN).move_to(eq_q)

        self.seg("Here's the trick. If the target is twenty three and I'm holding a fifteen, I know exactly what I need. An eight.", 7.0)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), rt=0.5)
        self.beat(FadeIn(badge, scale=1.4), rt=0.7)
        self.hold(0.9)
        self.beat(GrowFromCenter(card), FadeIn(card_lab, shift=UP * 0.2), rt=0.6)
        self.beat(Create(qbox), FadeIn(qmark), FadeIn(q_lab), rt=0.6)
        self.beat(Write(eq), rt=0.8)
        self.hold(0.9)
        self.beat(FadeOut(qbox), FadeOut(qmark), FadeIn(eight_box), FadeIn(eight_glow), FadeIn(eight, scale=1.6),
                  Transform(eq_q, eq_eight), q_lab.animate.set_color(GREEN), rt=0.8)
        self.beat(Flash(eight_box, color=GREEN, line_length=0.45, num_lines=14, flash_radius=1.35), rt=0.6)
        self.close_seg()

        formula = VGroup(T("complement", 38, GREEN), T("=", 38, MUTED), T("target", 38, YELLOW),
                         T("−", 38, MUTED), M("nums[i]", 38, MAGENTA)).arrange(RIGHT, buff=0.22)
        formula.move_to([0, -3.6, 0])
        frame = SurroundingRectangle(formula, color=VIOLET, buff=0.3, corner_radius=0.2, stroke_width=3)
        fglow = glow(frame, VIOLET, max_w=22)

        self.seg("We call that the complement. The target, minus the current value.", 4.35)
        self.beat(FadeIn(formula, shift=UP * 0.3), rt=1.0)
        self.beat(Create(frame), FadeIn(fglow), rt=0.7)
        self.beat(Indicate(formula[0], color=GREEN, scale_factor=1.15), rt=0.7)
        self.hold(0.9)
        self.beat(FadeOut(Group(*self.mobjects[1:])), rt=0.6)
        self.close_seg()


class Scene5_HashMap(Base):
    def construct(self):
        hdr = header("ONE PASS + HASH MAP", CYAN)
        badge = corner_badge()
        cells = make_array(ARR_Y)
        code = code_panel(HASH_CODE, -3.85)
        bar = line_bar(code, 1, YELLOW)

        panel = RoundedRectangle(corner_radius=0.25, width=3.6, height=3.75, fill_color=PANEL, fill_opacity=1,
                                 stroke_color=VIOLET, stroke_width=3).move_to([2.55, 0.12, 0])
        pglow = glow(panel, VIOLET, max_w=20, max_op=0.25)
        map_title = VGroup(M("seen", 28, VIOLET), M("{ value : index }", 18, MUTED)).arrange(DOWN, buff=0.06)
        map_title.next_to(panel.get_top(), DOWN, buff=0.15)
        row_ys = [0.92, 0.36, -0.2, -0.76, -1.32]

        def make_row(value, index, y):
            box = RoundedRectangle(corner_radius=0.12, width=3.1, height=0.46, fill_color=PANEL2, fill_opacity=1,
                                   stroke_color=VIOLET, stroke_width=1.5)
            txt = VGroup(M(str(value), 26, INK), M("→", 22, MUTED), M(str(index), 26, YELLOW)).arrange(RIGHT, buff=0.3)
            return VGroup(box, txt.move_to(box)).move_to([panel.get_x(), y, 0])

        ptr = pointer(MAGENTA, "i")
        probe_center = np.array([-2.15, 0.75, 0])

        self.seg("So we walk the array just once, with a hash map that remembers every number and its index.", 5.9)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(badge), rt=0.6)
        self.beat(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.1), rt=1.1)
        self.beat(FadeIn(code, shift=UP * 0.3), rt=0.7)
        self.beat(Create(panel), FadeIn(pglow), Write(map_title), FadeIn(bar), rt=1.0)
        self.close_seg()

        question = VGroup(T("Is my", 30, INK), T("complement", 30, GREEN), T("in the map?", 30, INK))
        question.arrange(DOWN, buff=0.12).move_to(probe_center)
        ptr.move_to(ptr_pos(cells, 0))

        self.seg("At each step, we first ask. Is my complement already in the map?", 4.25)
        self.beat(FadeIn(ptr, shift=UP * 0.3), cells[0].box.animate.set_stroke(MAGENTA, width=5),
                  Transform(bar, line_bar(code, 2, YELLOW)), rt=0.6)
        self.beat(Write(question), Transform(bar, line_bar(code, 4, YELLOW)), rt=1.0)
        self.beat(Indicate(question[1], color=GREEN, scale_factor=1.2), rt=0.8)
        self.hold(0.5)
        self.beat(FadeOut(question, shift=UP * 0.2), rt=0.4)
        self.close_seg()

        rows = []
        self.probe = VGroup()
        scan = RoundedRectangle(corner_radius=0.12, width=3.3, height=0.56, stroke_color=YELLOW, stroke_width=3,
                                fill_color=YELLOW, fill_opacity=0.08)

        def need_text(i):
            x = NUMS[i]
            line1 = VGroup(M(str(x), 46, MAGENTA), T("needs", 30, MUTED), M(str(TARGET - x), 46, GREEN)).arrange(RIGHT, buff=0.22)
            line2 = M(f"{TARGET} − {x} = {TARGET - x}", 24, MUTED)
            return VGroup(line1, line2).arrange(DOWN, buff=0.15).move_to(probe_center)

        def advance(i, s):
            # for-loop line moves the pointer, then the complement line computes need
            anims = [ptr.animate.move_to(ptr_pos(cells, i)), cells[i].box.animate.set_stroke(MAGENTA, width=5),
                     Transform(bar, line_bar(code, 2, YELLOW))]
            if i > 0:
                anims.append(cells[i - 1].box.animate.set_stroke(VIOLET, width=3))
            self.beat(*anims, rt=0.3 * s)
            new_probe = need_text(i)
            self.beat(FadeOut(self.probe), FadeIn(new_probe, shift=UP * 0.2),
                      Transform(bar, line_bar(code, 3, YELLOW)), rt=0.4 * s)
            self.probe = new_probe

        def step(i, s):
            advance(i, s)
            if rows:
                scan.move_to([panel.get_x(), row_ys[0], 0])
                self.beat(FadeIn(scan), Transform(bar, line_bar(code, 4, YELLOW)), rt=0.15 * s)
                self.beat(scan.animate.move_to([panel.get_x(), row_ys[len(rows) - 1], 0]), rt=0.4 * s)
                self.beat(FadeOut(scan), rt=0.1 * s)
            else:
                self.beat(panel.animate(rate_func=there_and_back).set_stroke(YELLOW, width=7),
                          Transform(bar, line_bar(code, 4, YELLOW)), rt=0.5 * s)
            miss = T("✗  not there", 26, RED).next_to(self.probe, DOWN, buff=0.28)
            self.beat(FadeIn(miss, scale=1.3), rt=0.3 * s)
            row = make_row(NUMS[i], i, row_ys[len(rows)])
            flying = cells[i].num.copy()
            self.beat(flying.animate.move_to(row[1][0]).set_color(INK), FadeOut(miss),
                      Transform(bar, line_bar(code, 6, YELLOW)), rt=0.5 * s)
            self.remove(flying)
            self.beat(FadeIn(row, scale=1.15), rt=0.25 * s)
            rows.append(row)

        self.seg("Five needs eighteen. Not there. Store it.", 3.026)
        step(0, 1.2)
        self.close_seg()

        self.seg("Twelve needs eleven. One needs twenty two. Still nothing. Into the map.", 5.075)
        step(1, 0.95)
        step(2, 0.95)
        self.close_seg()

        self.seg("Fourteen needs nine. Eight needs fifteen. Keep storing.", 3.975)
        step(3, 0.72)
        step(4, 0.72)
        self.close_seg()

        self.seg("Now we reach fifteen. It needs eight, and eight is already in the map, at index four!", 5.4)
        advance(5, 1.4)
        scan.move_to([panel.get_x(), row_ys[0], 0])
        self.beat(FadeIn(scan), Transform(bar, line_bar(code, 4, YELLOW)), rt=0.2)
        self.beat(scan.animate.move_to([panel.get_x(), row_ys[4], 0]), rt=0.9)
        hit_row = rows[4]
        hglow = glow(hit_row[0], GREEN, max_w=22, max_op=0.45)
        found = T("✓  found at index 4", 26, GREEN).next_to(self.probe, DOWN, buff=0.28)
        self.beat(hit_row[0].animate.set_stroke(GREEN, width=3).set_fill(GREEN, opacity=0.2), FadeIn(hglow),
                  scan.animate.set_stroke(GREEN), FadeIn(found, scale=1.3),
                  Transform(bar, line_bar(code, 4, GREEN)), rt=0.6)
        self.beat(Flash(hit_row, color=GREEN, line_length=0.3, num_lines=12, flash_radius=1.8), rt=0.5)
        a, b = cells[ANS[0]], cells[ANS[1]]
        arc = ArcBetweenPoints(a.box.get_top() + UP * 0.08, b.box.get_top() + UP * 0.08, angle=-PI * 0.7,
                               color=GREEN, stroke_width=5)
        self.beat(a.box.animate.set_stroke(GREEN, width=5), b.box.animate.set_stroke(GREEN, width=5),
                  Create(arc), FadeIn(glow(a.box, GREEN)), FadeIn(glow(b.box, GREEN)),
                  Transform(bar, line_bar(code, 5, GREEN)), rt=0.8)
        self.close_seg()

        ans = pill("return [4, 5]", GREEN, 36).move_to(probe_center + DOWN * 2.1)
        aglow = glow(ans[0], GREEN, max_w=26, max_op=0.4)

        self.seg("The answer is indices four and five.", 2.675)
        self.beat(FadeIn(aglow), FadeIn(ans, scale=1.4),
                  a.idx.animate.set_color(YELLOW).scale(1.4), b.idx.animate.set_color(YELLOW).scale(1.4), rt=0.7)
        self.hold(1.2)
        self.beat(FadeOut(Group(*self.mobjects[1:])), rt=0.6)
        self.close_seg()


class Scene6_Complexity(Base):
    def construct(self):
        hdr = header("COMPLEXITY", GREEN)

        lookup = VGroup(T("each lookup", 34, MUTED), MathTex(r"O(1)", font_size=72, color=YELLOW)).arrange(RIGHT, buff=0.35)
        lookup.move_to([0, 3.4, 0])
        boxes = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.68, height=0.68, fill_color=PANEL, fill_opacity=1,
                                          stroke_color=CYAN, stroke_width=2.5) for _ in range(8)]).arrange(RIGHT, buff=0.14)
        boxes.move_to([0, 1.3, 0])
        runner = Dot(radius=0.12, color=MAGENTA).move_to(boxes[0])
        total = MathTex(r"n \times O(1) = ", r"O(n)", font_size=76)
        total[1].set_color(GREEN)
        total.move_to([0, -1.0, 0])
        tglow = glow(total[1], GREEN, layers=6, max_w=16, max_op=0.35)

        self.seg("Each map lookup takes constant time, so the whole algorithm is linear.", 4.8)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(lookup, shift=DOWN * 0.2), rt=0.7)
        self.beat(LaggedStart(*[GrowFromCenter(bx) for bx in boxes], lag_ratio=0.08), FadeIn(runner), rt=0.7)
        self.beat(runner.animate.move_to(boxes[-1]),
                  LaggedStart(*[bx.animate.set_fill(GREEN, opacity=0.35) for bx in boxes], lag_ratio=0.12), rt=1.3)
        self.beat(Write(total), FadeIn(tglow), rt=0.9)
        self.close_seg()

        axes = Axes(x_range=[0, 10, 2], y_range=[0, 100, 20], x_length=6.4, y_length=5.4,
                    axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": False}).move_to([-0.3, 1.2, 0])
        xl = T("n", 28, MUTED).next_to(axes.x_axis, RIGHT, buff=0.12)
        yl = T("work", 24, MUTED).next_to(axes.y_axis, UP, buff=0.12)
        quad = axes.plot(lambda x: x ** 2, x_range=[0, 10], color=RED, stroke_width=6)
        lin = axes.plot(lambda x: x, x_range=[0, 10], color=GREEN, stroke_width=6)
        lglow = glow(lin, GREEN, layers=6, max_w=22)
        lq = MathTex(r"O(n^2)", font_size=60, color=RED).next_to(axes.c2p(10, 100), LEFT, buff=0.35)
        ll = MathTex(r"O(n)", font_size=60, color=GREEN).next_to(axes.c2p(10, 10), UP, buff=0.25).shift(LEFT * 0.3)
        mem = pill("+ O(n) extra memory", VIOLET, 30).move_to([0, -3.5, 0])

        self.seg("We went from n squared down to n, in exchange for a little extra memory.", 4.925)
        self.beat(FadeOut(VGroup(lookup, boxes, runner, total, tglow)), Create(axes), FadeIn(xl), FadeIn(yl), rt=0.8)
        self.beat(Create(quad), Create(lin), FadeIn(lglow), rt=1.4)
        self.beat(FadeIn(lq), FadeIn(ll), rt=0.5)
        self.beat(FadeIn(mem, shift=UP * 0.3), rt=0.6)
        self.hold(0.9)
        self.beat(FadeOut(VGroup(axes, xl, yl, quad, lin, lglow, lq, ll, mem, hdr)), rt=0.5)
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(HASH_CODE, 1.2)
        cglow = glow(code.background, VIOLET, max_w=22, max_op=0.25)
        bar = line_bar(code, 2, CYAN)

        self.seg("One loop, one map, and just a few lines of code.", 3.5)
        self.beat(FadeIn(code.background), FadeIn(cglow), rt=0.4)
        self.beat(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.12),
                  FadeIn(code.line_numbers), rt=1.0)
        self.beat(FadeIn(bar), rt=0.3)
        self.beat(Transform(bar, line_bar(code, 1, VIOLET)), rt=0.5)
        self.beat(Transform(bar, VGroup(*[line_bar(code, k, GREEN) for k in range(7)])), rt=0.6)
        self.close_seg()

        tag = VGroup(T("Trade memory", 68), T("for speed.", 68)).arrange(DOWN, buff=0.2)
        tag.set_color_by_gradient(CYAN, VIOLET, MAGENTA).move_to([0, 0.6, 0])
        tag_glow = glow(tag, VIOLET, layers=6, max_w=18, max_op=0.22)
        title, tglow, cells, badge = cover()

        self.seg("Trade memory for speed. That's the big lesson of Two Sum.", 3.975)
        self.beat(FadeOut(VGroup(code, cglow, bar), shift=UP * 0.4), rt=0.5)
        self.beat(Write(tag), FadeIn(tag_glow), rt=1.0)
        self.hold(0.6)
        # Morph into the opening frame so the loop closes seamlessly
        self.beat(ReplacementTransform(tag, VGroup(title)), FadeOut(tag_glow), FadeIn(tglow),
                  LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.08),
                  FadeIn(badge, shift=UP * 0.3), rt=1.1)
        self.add(tglow, title, cells, badge)
        self.close_seg()
