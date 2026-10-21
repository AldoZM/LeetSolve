from manim import *
import math
import random

config.pixel_width, config.pixel_height = 1280, 720
config.frame_width, config.frame_height = 16, 9
FPS = 30
config.frame_rate = FPS

# Palette: deep navy with neon accents
BG = "#0B0E1A"
PANEL = "#141B2F"
PANEL2 = "#1B2340"
CYAN = "#22D3EE"
MAGENTA = "#F472B6"
YELLOW = "#FACC15"
GREEN = "#34D399"
RED = "#F87171"
VIOLET = "#A78BFA"
MUTED = "#64748B"
INK = "#E2E8F0"

NUMS = [5, 12, 1, 14, 3, 9]
TARGET = 23


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
    box = RoundedRectangle(corner_radius=0.22, width=label.width + 0.6, height=label.height + 0.32,
                           fill_color=color, fill_opacity=0.12, stroke_color=color, stroke_width=2)
    return VGroup(box, label.move_to(box))


def dot_grid():
    dots = VGroup(*[Dot([x, y, 0], radius=0.018, color=MUTED, fill_opacity=0.35)
                    for x in np.arange(-7.6, 7.7, 0.8) for y in np.arange(-4.2, 4.3, 0.8)])
    return dots


class Cell(VGroup):
    def __init__(self, value, index, size=1.25, **kwargs):
        super().__init__(**kwargs)
        self.box = RoundedRectangle(corner_radius=0.18, width=size, height=size, fill_color=PANEL,
                                    fill_opacity=1, stroke_color=CYAN, stroke_width=3)
        self.num = M(str(value), int(46 * size / 1.25)).move_to(self.box)
        self.idx = T(str(index), int(22 * size / 1.25), MUTED).next_to(self.box, DOWN, buff=0.16)
        self.add(self.box, self.num, self.idx)


def make_array(y=0.3, size=1.25, gap=0.35, x0=0.0):
    cells = VGroup(*[Cell(v, i, size) for i, v in enumerate(NUMS)])
    for i, c in enumerate(cells):
        c.move_to([x0 + (i - 2.5) * (size + gap), y, 0])
    return cells


def target_badge(scale=1.0):
    label = T("target", 26, MUTED)
    val = M(str(TARGET), 50, YELLOW)
    row = VGroup(label, val).arrange(RIGHT, buff=0.3)
    box = RoundedRectangle(corner_radius=0.25, width=row.width + 0.7, height=row.height + 0.4,
                           fill_color=YELLOW, fill_opacity=0.08, stroke_color=YELLOW, stroke_width=2.5)
    g = VGroup(glow(box, YELLOW, max_w=18), box, row.move_to(box))
    return g.scale(scale)


def pointer(color, letter):
    tri = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(0.16)
    lab = T(letter, 26, color).next_to(tri, DOWN, buff=0.08)
    return VGroup(tri, lab)


class Base(Scene):
    scene_budget = 0.0
    scene_used = 0.0

    def setup(self):
        self.camera.background_color = BG
        self.add(dot_grid())

    # Manim rounds every play/wait up to whole frames; track that so audio stays in sync
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
        rng = random.Random(7)
        digits = VGroup(*[
            M(str(rng.randint(0, 99)), rng.randint(18, 40), rng.choice([CYAN, MAGENTA, VIOLET])).set_opacity(rng.uniform(0.12, 0.3))
            .move_to([rng.uniform(-7.4, 7.4), rng.uniform(-4.1, 4.1), 0])
            for _ in range(34)
        ])
        title = T("Two Sum", 130).set_color_by_gradient(CYAN, VIOLET, MAGENTA).shift(UP * 0.35)
        tglow = glow(title, VIOLET, layers=6, max_w=20, max_op=0.25)
        tags = VGroup(pill("LeetCode #1", CYAN, 28), pill("Easy", GREEN, 28), pill("Interview classic", MAGENTA, 28))
        tags.arrange(RIGHT, buff=0.35).next_to(title, DOWN, buff=0.6)

        self.seg("Two Sum. Problem number one on LeetCode, and an interview classic.", 4.7)
        self.beat(LaggedStart(*[FadeIn(d, scale=0.4) for d in digits], lag_ratio=0.04), rt=0.8)
        self.beat(Write(title), FadeIn(tglow), rt=1.3)
        self.beat(LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in tags], lag_ratio=0.3), rt=0.8)
        self.beat(digits.animate.shift(UP * 0.35), rt=1.1)
        self.beat(FadeOut(VGroup(digits, title, tglow, tags)), rt=0.6)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        header = pill("THE PROBLEM", CYAN, 22).to_corner(UL, buff=0.5)
        cells = make_array(y=0.3)
        badge = target_badge().move_to([0, 2.6, 0])
        nums_label = M("nums", 30, MUTED).next_to(cells, LEFT, buff=0.45)

        self.seg("You're given an array of integers and a target number.", 3.475)
        self.beat(FadeIn(header, shift=RIGHT * 0.3), rt=0.4)
        self.beat(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.12), FadeIn(nums_label), rt=1.5)
        self.beat(FadeIn(badge, scale=1.3), rt=0.8)
        self.close_seg()

        q1, q2 = M("?", 64, MAGENTA), M("?", 64, MAGENTA)
        eq = VGroup(q1, M("+", 64, MUTED), q2, M("=", 64, MUTED), M("23", 64, YELLOW)).arrange(RIGHT, buff=0.35)
        eq.move_to([0, -2.0, 0])
        a, b = cells[3], cells[5]
        arc = ArcBetweenPoints(a.box.get_top() + UP * 0.1, b.box.get_top() + UP * 0.1, angle=-PI * 0.7,
                               color=GREEN, stroke_width=5)
        glows = VGroup(glow(a.box, GREEN), glow(b.box, GREEN))
        solved = VGroup(M("14", 64, GREEN), M("+", 64, MUTED), M("9", 64, GREEN), M("=", 64, MUTED),
                        M("23", 64, YELLOW)).arrange(RIGHT, buff=0.35).move_to(eq)
        ret = pill("return [3, 5]", GREEN, 34).next_to(eq, DOWN, buff=0.45)

        self.seg("Find the two numbers that add up exactly to the target, and return their indices.", 5.325)
        self.beat(Write(eq), rt=0.8)
        self.beat(a.box.animate.set_stroke(GREEN, width=4), b.box.animate.set_stroke(GREEN, width=4),
                  FadeIn(glows), Create(arc), Transform(eq, solved), rt=1.4)
        self.beat(a.idx.animate.set_color(YELLOW).scale(1.4), b.idx.animate.set_color(YELLOW).scale(1.4),
                  FadeIn(ret, shift=UP * 0.2), rt=1.0)
        self.hold(1.2)
        self.beat(FadeOut(VGroup(eq, ret, arc, glows, nums_label)),
                  a.box.animate.set_stroke(CYAN, width=3), b.box.animate.set_stroke(CYAN, width=3),
                  a.idx.animate.set_color(MUTED).scale(1 / 1.4), b.idx.animate.set_color(MUTED).scale(1 / 1.4),
                  FadeOut(header), rt=0.6)
        self.close_seg()


class Scene3_BruteForce(Base):
    def construct(self):
        cells = make_array(y=0.3)
        badge = target_badge().move_to([0, 2.6, 0])
        self.add(cells, badge)

        header = pill("BRUTE FORCE", RED, 22).to_corner(UL, buff=0.5)
        # Pair grid: cell (i, j) lights up once the pair is checked
        gs = 0.36
        grid = VGroup()
        grid_cells = {}
        for i in range(6):
            for j in range(6):
                sq = Square(gs, stroke_width=1.5, stroke_color=MUTED, stroke_opacity=0.5,
                            fill_color=PANEL, fill_opacity=1 if j > i else 0.2)
                sq.move_to([j * (gs + 0.06), -i * (gs + 0.06), 0])
                grid.add(sq)
                grid_cells[(i, j)] = sq
        grid_title = T("pairs checked", 22, MUTED)
        grid_block = VGroup(grid, grid_title)
        grid_title.next_to(grid, UP, buff=0.2)
        grid_block.move_to([5.4, -2.2, 0])

        counter = Integer(0, font_size=72, color=RED)
        counter_label = T("checks", 24, MUTED)
        counter_block = VGroup(counter_label, counter).arrange(DOWN, buff=0.15).move_to([-5.6, -2.2, 0])

        pi_ = pointer(MAGENTA, "i")
        pj = pointer(CYAN, "j")

        def ptr_pos(k):
            return cells[k].idx.get_bottom() + DOWN * 0.42

        def readout(i, j):
            s = NUMS[i] + NUMS[j]
            ok = s == TARGET
            parts = VGroup(M(str(NUMS[i]), 54, MAGENTA), M("+", 54, MUTED), M(str(NUMS[j]), 54, CYAN),
                           M("=", 54, MUTED), M(str(s), 54, GREEN if ok else INK),
                           T("✓" if ok else "≠ 23", 40, GREEN if ok else RED))
            return parts.arrange(RIGHT, buff=0.28).move_to([0, -2.6, 0])

        self.seg("The most direct idea is to try every possible pair.", 3.9)
        self.beat(FadeIn(header, shift=RIGHT * 0.3), cells.animate.shift(UP * 0.7), rt=0.8)
        pi_.move_to(ptr_pos(0))
        pj.move_to(ptr_pos(1))
        cells[0].box.set_stroke(MAGENTA)
        self.beat(FadeIn(pi_, shift=UP * 0.3), FadeIn(pj, shift=UP * 0.3),
                  cells[1].box.animate.set_stroke(CYAN, width=5), rt=0.6)
        ro = readout(0, 1)
        grid_cells[(0, 1)].set_fill(RED, opacity=0.7)
        self.beat(FadeIn(ro, shift=UP * 0.2), FadeIn(grid_block), FadeIn(counter_block), rt=0.7)
        self.beat(counter.animate.set_value(1), rt=0.3)
        self.close_seg()

        def check(i, j, rt, prev_j):
            new_ro = readout(i, j)
            sq = grid_cells[(i, j)]
            hit = NUMS[i] + NUMS[j] == TARGET
            reset = [cells[prev_j].box.animate.set_stroke(CYAN, width=3)] if prev_j not in (i, j) else []
            self.beat(pi_.animate.move_to(ptr_pos(i)), pj.animate.move_to(ptr_pos(j)), *reset,
                      cells[i].box.animate.set_stroke(MAGENTA, width=4),
                      cells[j].box.animate.set_stroke(CYAN, width=5),
                      FadeOut(self.ro), FadeIn(new_ro),
                      sq.animate.set_fill(GREEN if hit else RED, opacity=0.85),
                      counter.animate.set_value(counter.get_value() + 1), rt=rt)
            self.ro = new_ro

        self.ro = ro
        self.seg("Fix one number, and add it to every number after it.", 3.575)
        prev = 1
        for j in range(2, 6):
            check(0, j, 0.7, prev)
            prev = j
        self.close_seg()

        self.seg("It works, but with just six numbers, that's already fifteen checks.", 4.175)
        for i in range(1, 5):
            self.beat(cells[i - 1].box.animate.set_stroke(CYAN, width=3), rt=0.05)
            for j in range(i + 1, 6):
                check(i, j, 0.24, prev)
                prev = j
        self.beat(Indicate(counter, color=YELLOW, scale_factor=1.5), rt=0.6)
        self.close_seg()

        self.seg("And it grows quadratically. With a million numbers, that's half a trillion pairs.", 5.1)
        everything = VGroup(cells, badge, pi_, pj, self.ro, grid_block, counter_block)
        self.beat(FadeOut(everything, shift=DOWN * 0.3), rt=0.5)
        axes = Axes(x_range=[0, 10, 2], y_range=[0, 100, 20], x_length=6.2, y_length=4.4,
                    axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": False}).move_to([-3.2, -0.4, 0])
        xl = T("n", 28, MUTED).next_to(axes.x_axis, RIGHT, buff=0.15)
        yl = T("pairs", 24, MUTED).next_to(axes.y_axis, UP, buff=0.15)
        curve = axes.plot(lambda x: x ** 2, x_range=[0, 10], color=RED, stroke_width=6)
        cglow = glow(curve, RED, layers=6, max_w=22)
        big_o = MathTex(r"O(n^2)", font_size=64, color=RED).next_to(axes.c2p(10, 100), RIGHT, buff=0.2).shift(DOWN * 0.3)
        stat1 = VGroup(M("1,000,000", 46, INK), T("numbers", 26, MUTED)).arrange(DOWN, buff=0.1)
        arrow = Arrow(UP * 0.4, DOWN * 0.4, color=MUTED, stroke_width=4)
        stat2 = VGroup(M("~500,000,000,000", 46, RED), T("pairs", 26, MUTED)).arrange(DOWN, buff=0.1)
        stats = VGroup(stat1, arrow, stat2).arrange(DOWN, buff=0.3).move_to([4.4, -0.3, 0])
        self.beat(Create(axes), FadeIn(xl), FadeIn(yl), rt=0.7)
        self.beat(Create(curve), FadeIn(cglow), rt=1.4)
        self.beat(Write(big_o), FadeIn(stat1, shift=LEFT * 0.3), rt=0.6)
        self.beat(GrowArrow(arrow), FadeIn(stat2, scale=1.3), rt=0.7)
        self.hold(0.6)
        self.beat(FadeOut(VGroup(axes, xl, yl, curve, cglow, big_o, stats, header)), rt=0.5)
        self.close_seg()


class Scene4_Insight(Base):
    def construct(self):
        header = pill("THE TRICK", YELLOW, 22).to_corner(UL, buff=0.5)
        badge = target_badge(1.2).move_to([0, 2.5, 0])

        card = Cell(14, 0, 2.0)
        card.remove(card.idx)
        card.box.set_stroke(MAGENTA, width=5)
        card.move_to([-3.6, -0.1, 0])
        card_lab = T("holding", 26, MAGENTA).next_to(card, DOWN, buff=0.25)

        qbox = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=2.0, height=2.0, color=MUTED, stroke_width=4),
                              num_dashes=28).move_to([3.6, -0.1, 0])
        qmark = M("?", 80, MUTED).move_to(qbox)
        q_lab = T("need", 26, MUTED).next_to(qbox, DOWN, buff=0.25)

        eq_q = M("?", 56, MUTED)
        eq = VGroup(M("23", 56, YELLOW), M("−", 56, MUTED), M("14", 56, MAGENTA), M("=", 56, MUTED), eq_q)
        eq.arrange(RIGHT, buff=0.3).move_to([0, -0.1, 0])

        nine_box = RoundedRectangle(corner_radius=0.25, width=2.0, height=2.0, fill_color=PANEL, fill_opacity=1,
                                    stroke_color=GREEN, stroke_width=5).move_to(qbox)
        nine = M("9", 80, GREEN).move_to(qbox)
        nine_glow = glow(nine_box, GREEN, max_w=30, max_op=0.4)
        eq_nine = M("9", 56, GREEN).move_to(eq_q)

        self.seg("Here's the trick. If the target is twenty three and I'm holding a fourteen, I know exactly what I need. A nine.", 7.125)
        self.beat(FadeIn(header, shift=RIGHT * 0.3), rt=0.5)
        self.beat(FadeIn(badge, scale=1.4), rt=0.7)
        self.hold(0.9)
        self.beat(GrowFromCenter(card), FadeIn(card_lab, shift=UP * 0.2), rt=0.6)
        self.beat(Create(qbox), FadeIn(qmark), FadeIn(q_lab), rt=0.6)
        self.beat(Write(eq), rt=0.8)
        self.hold(1.0)
        self.beat(FadeOut(qbox), FadeOut(qmark), FadeIn(nine_box), FadeIn(nine_glow), FadeIn(nine, scale=1.6),
                  Transform(eq_q, eq_nine), q_lab.animate.set_color(GREEN), rt=0.8)
        self.beat(Flash(nine_box, color=GREEN, line_length=0.5, num_lines=14, flash_radius=1.5), rt=0.6)
        self.close_seg()

        formula = VGroup(T("complement", 44, GREEN), T("=", 44, MUTED), T("target", 44, YELLOW),
                         T("−", 44, MUTED), M("nums[i]", 44, MAGENTA)).arrange(RIGHT, buff=0.3)
        formula.move_to([0, -2.9, 0])
        frame = SurroundingRectangle(formula, color=VIOLET, buff=0.3, corner_radius=0.2, stroke_width=3)
        fglow = glow(frame, VIOLET, max_w=22)

        self.seg("We call that the complement. The target, minus the current value.", 4.35)
        self.beat(FadeIn(formula, shift=UP * 0.3), rt=1.0)
        self.beat(Create(frame), FadeIn(fglow), rt=0.7)
        self.beat(Indicate(formula[0], color=GREEN, scale_factor=1.15), rt=0.7)
        self.hold(0.9)
        self.beat(FadeOut(Group(*[m for m in self.mobjects[1:]])), rt=0.6)
        self.close_seg()


class Scene5_HashMap(Base):
    def construct(self):
        header = pill("ONE PASS + HASH MAP", CYAN, 22).to_corner(UL, buff=0.5)
        badge = target_badge(0.75).to_corner(UR, buff=0.5)
        cells = make_array(y=2.0, size=1.05, gap=0.3, x0=-1.9)

        panel = RoundedRectangle(corner_radius=0.3, width=3.5, height=4.7, fill_color=PANEL, fill_opacity=1,
                                 stroke_color=VIOLET, stroke_width=3).move_to([5.45, -0.75, 0])
        pglow = glow(panel, VIOLET, max_w=20, max_op=0.25)
        map_title = VGroup(M("seen", 30, VIOLET), M("{ value : index }", 20, MUTED)).arrange(DOWN, buff=0.08)
        map_title.next_to(panel.get_top(), DOWN, buff=0.22)
        row_ys = [0.55, -0.17, -0.89, -1.61, -2.33]

        def make_row(value, index, y):
            box = RoundedRectangle(corner_radius=0.15, width=2.9, height=0.56, fill_color=PANEL2, fill_opacity=1,
                                   stroke_color=VIOLET, stroke_width=1.5)
            txt = VGroup(M(str(value), 30, INK), M("→", 26, MUTED), M(str(index), 30, YELLOW)).arrange(RIGHT, buff=0.35)
            return VGroup(box, txt.move_to(box)).move_to([panel.get_x(), y, 0])

        ptr = pointer(MAGENTA, "i")

        def ptr_pos(k):
            return cells[k].idx.get_bottom() + DOWN * 0.38

        probe_center = np.array([-1.9, -1.15, 0])

        self.seg("So we walk the array just once, with a hash map that remembers every number and its index.", 5.9)
        self.beat(FadeIn(header, shift=RIGHT * 0.3), FadeIn(badge), rt=0.6)
        self.beat(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.1), rt=1.2)
        self.beat(Create(panel), FadeIn(pglow), Write(map_title), rt=1.1)
        self.close_seg()

        question = VGroup(T("Is my", 40, INK), T("complement", 40, GREEN), T("already in the map?", 40, INK))
        question.arrange(RIGHT, buff=0.22).move_to(probe_center)
        ptr.move_to(ptr_pos(0))

        self.seg("At each step, we first ask. Is my complement already in the map?", 4.25)
        self.beat(FadeIn(ptr, shift=UP * 0.3), cells[0].box.animate.set_stroke(MAGENTA, width=5), rt=0.5)
        self.beat(Write(question), rt=1.0)
        self.beat(Indicate(question[1], color=GREEN, scale_factor=1.2), rt=0.8)
        self.hold(0.6)
        self.beat(FadeOut(question, shift=UP * 0.2), rt=0.4)
        self.close_seg()

        rows = []
        self.probe = VGroup()
        scan = RoundedRectangle(corner_radius=0.15, width=3.1, height=0.66, stroke_color=YELLOW, stroke_width=3,
                                fill_color=YELLOW, fill_opacity=0.08)

        def need_text(i):
            x = NUMS[i]
            line1 = VGroup(M(str(x), 50, MAGENTA), T("needs", 34, MUTED), M(str(TARGET - x), 50, GREEN)).arrange(RIGHT, buff=0.3)
            line2 = M(f"{TARGET} − {x} = {TARGET - x}", 26, MUTED)
            return VGroup(line1, line2).arrange(DOWN, buff=0.18).move_to(probe_center)

        def step(i, s):
            # Move pointer, show complement, scan map, miss, store value
            new_probe = need_text(i)
            anims = [ptr.animate.move_to(ptr_pos(i)), cells[i].box.animate.set_stroke(MAGENTA, width=5),
                     FadeOut(self.probe), FadeIn(new_probe, shift=UP * 0.2)]
            if i > 0:
                anims.append(cells[i - 1].box.animate.set_stroke(VIOLET, width=3))
            self.beat(*anims, rt=0.55 * s)
            self.probe = new_probe
            if rows:
                scan.move_to([panel.get_x(), row_ys[0], 0])
                self.beat(FadeIn(scan), rt=0.15 * s)
                self.beat(scan.animate.move_to([panel.get_x(), row_ys[len(rows) - 1], 0]), rt=0.4 * s)
                self.beat(FadeOut(scan), rt=0.1 * s)
            else:
                self.beat(Indicate(panel, color=YELLOW, scale_factor=1.03), rt=0.5 * s)
            miss = T("✗  not there", 28, RED).next_to(new_probe, DOWN, buff=0.3)
            self.beat(FadeIn(miss, scale=1.3), rt=0.3 * s)
            row = make_row(NUMS[i], i, row_ys[len(rows)])
            flying = cells[i].num.copy()
            self.beat(flying.animate.move_to(row[1][0]).set_color(INK), FadeOut(miss), rt=0.5 * s)
            self.remove(flying)
            self.beat(FadeIn(row, scale=1.15), rt=0.25 * s)
            rows.append(row)

        self.seg("Five needs eighteen. Not there. Store it.", 3.026)
        step(0, 1.2)
        self.close_seg()

        self.seg("Twelve needs eleven. One needs twenty two. Still nothing. Into the map.", 5.075)
        step(1, 1.0)
        step(2, 1.0)
        self.close_seg()

        self.seg("Fourteen needs nine. Three needs twenty. Keep storing.", 3.825)
        step(3, 0.8)
        step(4, 0.8)
        self.close_seg()

        self.seg("Now we reach nine. It needs fourteen, and fourteen is already in the map, at index three!", 5.825)
        new_probe = need_text(5)
        self.beat(ptr.animate.move_to(ptr_pos(5)), cells[5].box.animate.set_stroke(MAGENTA, width=5),
                  cells[4].box.animate.set_stroke(VIOLET, width=3), FadeOut(self.probe),
                  FadeIn(new_probe, shift=UP * 0.2), rt=0.6)
        self.probe = new_probe
        self.hold(0.5)
        scan.move_to([panel.get_x(), row_ys[0], 0])
        self.beat(FadeIn(scan), rt=0.2)
        self.beat(scan.animate.move_to([panel.get_x(), row_ys[3], 0]), rt=0.9)
        hit_row = rows[3]
        hglow = glow(hit_row[0], GREEN, max_w=22, max_op=0.45)
        found = T("✓  found at index 3", 28, GREEN).next_to(new_probe, DOWN, buff=0.3)
        self.beat(hit_row[0].animate.set_stroke(GREEN, width=3).set_fill(GREEN, opacity=0.2), FadeIn(hglow),
                  scan.animate.set_stroke(GREEN), FadeIn(found, scale=1.3), rt=0.6)
        self.beat(Flash(hit_row, color=GREEN, line_length=0.3, num_lines=12, flash_radius=1.7), rt=0.5)
        a, b = cells[3], cells[5]
        arc = ArcBetweenPoints(a.box.get_top() + UP * 0.08, b.box.get_top() + UP * 0.08, angle=-PI * 0.7,
                               color=GREEN, stroke_width=5)
        self.beat(a.box.animate.set_stroke(GREEN, width=5), b.box.animate.set_stroke(GREEN, width=5),
                  Create(arc), FadeIn(glow(a.box, GREEN)), FadeIn(glow(b.box, GREEN)), rt=0.8)
        self.close_seg()

        ans = pill("return [3, 5]", GREEN, 46)
        ans.move_to(probe_center + DOWN * 1.9)
        aglow = glow(ans[0], GREEN, max_w=26, max_op=0.4)

        self.seg("The answer is indices three and five.", 2.7)
        self.beat(FadeIn(aglow), FadeIn(ans, scale=1.4),
                  a.idx.animate.set_color(YELLOW).scale(1.4), b.idx.animate.set_color(YELLOW).scale(1.4), rt=0.7)
        self.hold(1.2)
        self.beat(FadeOut(Group(*[m for m in self.mobjects[1:]])), rt=0.6)
        self.close_seg()


class Scene6_Complexity(Base):
    def construct(self):
        header = pill("COMPLEXITY", GREEN, 22).to_corner(UL, buff=0.5)

        lookup = VGroup(T("each lookup", 34, MUTED), MathTex(r"O(1)", font_size=72, color=YELLOW)).arrange(RIGHT, buff=0.4)
        lookup.move_to([0, 2.0, 0])
        boxes = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.8, height=0.8, fill_color=PANEL, fill_opacity=1,
                                          stroke_color=CYAN, stroke_width=2.5) for _ in range(8)]).arrange(RIGHT, buff=0.18)
        boxes.move_to([0, 0.2, 0])
        runner = Dot(radius=0.14, color=MAGENTA).move_to(boxes[0])
        total = MathTex(r"n \times O(1) = ", r"O(n)", font_size=72)
        total[1].set_color(GREEN)
        total.move_to([0, -1.8, 0])
        tglow = glow(total[1], GREEN, layers=6, max_w=16, max_op=0.35)

        self.seg("Each map lookup takes constant time, so the whole algorithm is linear.", 4.8)
        self.beat(FadeIn(header, shift=RIGHT * 0.3), FadeIn(lookup, shift=DOWN * 0.2), rt=0.7)
        self.beat(LaggedStart(*[GrowFromCenter(bx) for bx in boxes], lag_ratio=0.08), FadeIn(runner), rt=0.7)
        self.beat(runner.animate.move_to(boxes[-1]),
                  LaggedStart(*[bx.animate.set_fill(GREEN, opacity=0.35) for bx in boxes], lag_ratio=0.12), rt=1.3)
        self.beat(Write(total), FadeIn(tglow), rt=0.9)
        self.close_seg()

        axes = Axes(x_range=[0, 10, 2], y_range=[0, 100, 20], x_length=7.0, y_length=4.6,
                    axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": False}).move_to([-1.6, -0.4, 0])
        xl = T("n", 28, MUTED).next_to(axes.x_axis, RIGHT, buff=0.15)
        yl = T("work", 24, MUTED).next_to(axes.y_axis, UP, buff=0.15)
        quad = axes.plot(lambda x: x ** 2, x_range=[0, 10], color=RED, stroke_width=6)
        lin = axes.plot(lambda x: x, x_range=[0, 10], color=GREEN, stroke_width=6)
        lglow = glow(lin, GREEN, layers=6, max_w=22)
        lq = MathTex(r"O(n^2)", font_size=56, color=RED).next_to(axes.c2p(10, 100), RIGHT, buff=0.2).shift(DOWN * 0.3)
        ll = MathTex(r"O(n)", font_size=56, color=GREEN).next_to(axes.c2p(10, 10), RIGHT, buff=0.25)
        mem = pill("+ O(n) extra memory", VIOLET, 28).move_to([4.6, 1.2, 0])

        self.seg("We went from n squared down to n, in exchange for a little extra memory.", 4.925)
        self.beat(FadeOut(VGroup(lookup, boxes, runner, total, tglow)), Create(axes), FadeIn(xl), FadeIn(yl), rt=0.8)
        self.beat(Create(quad), Create(lin), FadeIn(lglow), rt=1.4)
        self.beat(FadeIn(lq), FadeIn(ll), rt=0.5)
        self.beat(FadeIn(mem, shift=LEFT * 0.3), rt=0.6)
        self.hold(0.9)
        self.beat(FadeOut(VGroup(axes, xl, yl, quad, lin, lglow, lq, ll, mem, header)), rt=0.5)
        self.close_seg()


CODE = """def twoSum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i"""


class Scene7_Code(Base):
    def construct(self):
        code = Code(code_string=CODE, language="python", formatter_style="monokai", background="window",
                    paragraph_config={"font": "Consolas"}).scale(1.25).move_to([0, 0.1, 0])
        cglow = glow(code.background, VIOLET, max_w=22, max_op=0.25)
        lines = code.code_lines
        hl = VGroup(*[SurroundingRectangle(lines[k], color=GREEN, buff=0.06, corner_radius=0.08, stroke_width=2,
                                           fill_color=GREEN, fill_opacity=0.12) for k in (3, 4)])

        self.seg("And the code fits in just a few lines.", 2.65)
        self.beat(FadeIn(code.background), FadeIn(cglow), rt=0.4)
        self.beat(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in lines], lag_ratio=0.15),
                  FadeIn(code.line_numbers), rt=1.2)
        self.beat(FadeIn(hl), rt=0.5)
        self.close_seg()

        tag = T("Trade memory for speed.", 72).set_color_by_gradient(CYAN, VIOLET, MAGENTA)
        tag_glow = glow(tag, VIOLET, layers=6, max_w=18, max_op=0.22)
        done = VGroup(T("Two Sum", 36, INK), T("✓", 36, GREEN)).arrange(RIGHT, buff=0.2).next_to(tag, DOWN, buff=0.5)

        self.seg("Trade memory for speed. That's the big lesson of Two Sum.", 3.975)
        self.beat(FadeOut(VGroup(code, cglow, hl), shift=UP * 0.4), rt=0.6)
        self.beat(Write(tag), FadeIn(tag_glow), rt=1.2)
        self.beat(FadeIn(done, shift=UP * 0.2), rt=0.5)
        self.hold(0.9)
        self.beat(FadeOut(VGroup(tag, tag_glow, done)), rt=0.6)
        self.close_seg()
