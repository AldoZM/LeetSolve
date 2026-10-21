WALK = json.load(open('walk.json', encoding='utf-8'))
LIMIT = WALK["limit"]

CODE = """def reverse(x):
    sign = -1 if x < 0 else 1
    x, rev = abs(x), 0
    LIMIT = 2**31 - 1
    while x:
        x, d = divmod(x, 10)
        if rev > (LIMIT - d) // 10:
            return 0
        rev = rev * 10 + d
    return sign * rev"""


def digits(n, color, y, size=0.8, gap=0.12, x=0.0):
    return tile_row(list(str(n)), color, y, size, gap, x)


def cover():
    # Opening frame and closing frame are the same, so the video loops seamlessly
    title, tglow = gradient_title(["Reverse", "Integer"], size=110, y=3.3)
    top = digits(1463, CYAN, 0.2, size=0.9, gap=0.35)
    bot = digits(3641, GREEN, -2.0, size=0.9, gap=0.35)
    arrows = VGroup(*[Arrow(top[k].get_bottom(), bot[3 - k].get_top(), buff=0.1, color=ARROW, stroke_width=3, tip_length=0.15)
                      for k in range(4)])
    return title, tglow, VGroup(arrows, top, bot)


class Scene1_Hook(Base):
    def construct(self):
        title, tglow, art = cover()
        self.add(tglow, title, art)
        arrows, top, bot = art
        rng = random.Random(7)
        bg = VGroup(*[
            M(str(rng.randint(0, 9)), rng.randint(18, 34), rng.choice([CYAN, MAGENTA, VIOLET])).set_opacity(rng.uniform(0.12, 0.28))
            .move_to([rng.uniform(-4.1, 4.1), rng.choice([rng.uniform(-5.6, -4.4), rng.uniform(5.0, 5.7), rng.uniform(1.2, 1.5)]), 0])
            for _ in range(22)
        ])
        tags = tags_block([("LeetCode #7", CYAN), ("Medium", YELLOW), ("Math", VIOLET)], y=-3.6)

        self.seg(0)
        self.beat(LaggedStart(*[FadeIn(d, scale=0.4) for d in bg], lag_ratio=0.04),
                  LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in [*tags[0], *tags[1]]], lag_ratio=0.3), rt=1.0)
        self.beat(LaggedStart(*[ShowPassingFlash(a.copy().set_stroke(YELLOW, width=6), time_width=0.6) for a in arrows], lag_ratio=0.2), rt=1.0)
        self.beat(LaggedStart(*[ring(t.box, GREEN) for t in bot], lag_ratio=0.15), rt=0.9)
        self.finish(FadeOut(VGroup(title, tglow, tags, bg, art)), rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        hdr = header("THE PROBLEM", CYAN)
        a = digits(123, CYAN, 3.2, size=1.0, gap=0.2)
        b = digits(321, GREEN, 1.6, size=1.0, gap=0.2)
        arrow = M("↓", 44, MUTED).move_to([0, 2.4, 0])
        bits = T("signed 32-bit integer", 28, MUTED).move_to([0, 4.4, 0])

        self.seg(1)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(bits), LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in a], lag_ratio=0.15), rt=0.9)
        self.until(DUR[1] * 0.5)
        self.beat(FadeIn(arrow), *[TransformFromCopy(a[k], b[2 - k]) for k in range(3)], rt=1.0)
        self.close_seg()

        line = NumberLine(x_range=[-1, 1, 1], length=7.4, color=MUTED, include_ticks=False).move_to([0, -0.8, 0])
        lo = M("-2147483648", 26, MUTED).next_to(line.get_left(), DOWN, buff=0.25).shift(RIGHT * 0.5)
        hi = M("2147483647", 26, YELLOW).next_to(line.get_right(), DOWN, buff=0.25).shift(LEFT * 0.4)
        band = Rectangle(width=7.4, height=0.3, fill_color=GREEN, fill_opacity=0.25, stroke_width=0).move_to(line)
        big = M("1534236469", 40, CYAN).move_to([0, -2.4, 0])
        flip = M("9646324351", 40, RED).move_to([0, -3.4, 0])
        out = Dot(line.get_right() + RIGHT * 0.6, radius=0.12, color=RED)
        zero = T("return 0", 40, RED).move_to([0, -4.6, 0])

        self.seg(2)
        self.beat(Create(line), FadeIn(band), FadeIn(lo), FadeIn(hi), rt=0.7)
        self.beat(FadeIn(big), rt=0.4)
        self.beat(TransformFromCopy(big, flip), rt=0.6)
        self.beat(GrowFromCenter(out), FadeIn(zero, scale=1.3), rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene3_String(Base):
    def construct(self):
        hdr = header("THE EASY WAY", GREEN)
        code = M('int(str(x)[::-1])', 44, INK).move_to([0, 3.0, 0])
        ok = T("✓  easy to write", 30, GREEN).move_to([0, 2.0, 0])
        warn = VGroup(T("but overflow?", 44, RED), T("no 64-bit integers allowed", 28, MUTED)).arrange(DOWN, buff=0.25).move_to([0, 0.0, 0])
        meter = RoundedRectangle(corner_radius=0.15, width=1.0, height=3.6, stroke_color=MUTED, stroke_width=3).move_to([0, -3.4, 0])
        fill = Rectangle(width=0.8, height=0.1, fill_color=GREEN, fill_opacity=0.8, stroke_width=0).align_to(meter, DOWN).shift(UP * 0.1)
        cap = Line(meter.get_corner(UL) + DOWN * 0.3 + LEFT * 0.3, meter.get_corner(UR) + DOWN * 0.3 + RIGHT * 0.3, color=RED, stroke_width=5)
        cap_l = M("2³¹−1", 26, RED).next_to(cap, RIGHT, buff=0.15)

        self.seg(3)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), Write(code), rt=1.0)
        self.beat(FadeIn(ok), rt=0.4)
        self.until(DUR[3] * 0.4)
        self.beat(FadeIn(warn, shift=UP * 0.2), FadeIn(meter), FadeIn(cap), FadeIn(cap_l), FadeIn(fill), rt=0.7)
        self.beat(fill.animate.stretch_to_fit_height(3.6, about_edge=DOWN).set_fill(RED), rt=1.2)
        self.clear_all()
        self.close_seg()


class Scene4_Math(Base):
    def construct(self):
        hdr = header("THE MATH", YELLOW)
        x_lab = T("x", 34, CYAN).move_to([-3.6, 3.2, 0])
        x = digits(1463, CYAN, 3.2, size=0.9, gap=0.15)
        mod = MathTex(r"d = x \bmod 10 = 3", font_size=48, color=YELLOW).move_to([0, 1.7, 0])
        div = MathTex(r"x = x \,/\!/\, 10 = 146", font_size=48, color=CYAN).move_to([0, 0.8, 0])

        self.seg(4)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(x_lab), FadeIn(x), rt=0.6)
        self.until(DUR[4] * 0.3)
        self.beat(Write(mod), restyle(x[3], lambda m: m.shift(DOWN * 0.5).box.set_stroke(YELLOW, width=4)), rt=0.8)
        self.until(DUR[4] * 0.65)
        self.beat(Write(div), FadeOut(x[3], shift=DOWN * 0.3), rt=0.8)
        self.close_seg()

        rev_lab = T("rev", 34, GREEN).move_to([-3.6, -1.0, 0])
        rev = digits(36, GREEN, -1.0, size=0.9, gap=0.15)
        new = Tile(4, YELLOW, 0.9)
        push = MathTex(r"\text{rev} = \text{rev} \times 10 + d", font_size=48, color=GREEN).move_to([0, -2.6, 0])

        self.seg(5)
        self.beat(FadeOut(VGroup(mod, div)), FadeIn(rev_lab), FadeIn(rev), rt=0.5)
        self.beat(Write(push), rt=0.8)
        self.beat(rev.animate.shift(LEFT * 0.525), rt=0.5)
        new.next_to(rev, RIGHT, buff=0.15)
        self.beat(FadeIn(new, shift=DOWN * 0.4), rt=0.5)
        self.close_seg()

        check = MathTex(r"\text{rev} > (\text{LIMIT} - d) \,/\!/\, 10", font_size=46, color=RED).move_to([0, -3.8, 0])
        then = T("→ return 0", 34, RED).next_to(check, DOWN, buff=0.25)
        shield = Rectangle(width=8.2, height=4.2, stroke_color=RED, stroke_width=3, fill_opacity=0).move_to([0, -2.1, 0])

        self.seg(6)
        self.beat(Write(check), rt=0.9)
        self.beat(FadeIn(then, shift=UP * 0.2), Create(shield), rt=0.7)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        hdr = header("POP AND PUSH", YELLOW)
        code = code_panel(CODE, -3.95, max_h=3.85)

        def readout(x, d, rev, rev_color=GREEN):
            parts = VGroup(pill(f"x {x}", CYAN, 26), pill(f"d {d}", YELLOW, 26), pill(f"rev {rev}", rev_color, 26))
            return parts.arrange(RIGHT, buff=0.25).move_to([0, -1.35, 0])

        st = {"x": WALK["x1"], "d": "-", "rev": 0}
        ro = readout(st["x"], "-", 0)
        bar = line_bar(code, 2, 3)
        ev = []
        for run in ("run1", "run2"):
            for k, op in enumerate(WALK[run]):
                for kind in ("pop", "check", "push", "stop"):
                    if kind in op:
                        ev.append((seg_time(WALK["first"], op[kind]), kind, (run, k)))
        ev.append((seg_time(WALK["first"], WALK["done1"]), "done", ("run1", 0)))
        ev.append((seg_time(WALK["first"], WALK["reset"]), "reset", ("run2", 0)))
        ev.sort(key=lambda e: e[0])

        def intro():
            self.until(0.3)
            self.beat(FadeIn(hdr, shift=RIGHT * 0.3), rt=0.5)
            self.until(0.9)
            self.beat(FadeIn(code, shift=UP * 0.3), rt=0.8)
            self.until(2.0)
            self.beat(FadeIn(bar), FadeIn(ro), rt=0.4)

        def on(kind, key):
            run, k = key
            op = WALK[run][k]
            fast = run == "run2" and not op["overflow"]
            rt = 0.12 if fast else 0.3
            if kind == "pop":
                st["x"], st["d"] = op["x_after"], op["d"]
                self.beat(Transform(bar, line_bar(code, 5)), Transform(ro, readout(st["x"], st["d"], st["rev"])), rt=rt)
            elif kind == "check":
                self.beat(Transform(bar, line_bar(code, 6, 6, RED if op["overflow"] else GREEN)), rt=rt)
            elif kind == "push":
                st["rev"] = op["rev_after"]
                self.beat(Transform(bar, line_bar(code, 8, 8, GREEN)), Transform(ro, readout(st["x"], st["d"], st["rev"])), rt=rt)
            elif kind == "stop":
                self.beat(Transform(bar, line_bar(code, 7, 7, RED)), Transform(ro, readout(st["x"], st["d"], "0", RED)), rt=0.3)
            elif kind == "done":
                self.beat(Transform(bar, line_bar(code, 9, 9, GREEN)), rt=0.3)
            elif kind == "reset":
                st["x"], st["d"], st["rev"] = WALK["x2"], "-", 0
                self.beat(Transform(bar, line_bar(code, 2, 3)), Transform(ro, readout(st["x"], "-", 0)), rt=0.3)

        def outro():
            self.finish(FadeOut(VGroup(hdr, ro, code, bar)), rt=0.5)

        self.run_events(WALK, ev, on, intro, outro)


class Scene6_Complexity(Base):
    def construct(self):
        hdr = header("COMPLEXITY", GREEN)
        x = digits(1534236469, CYAN, 3.4, size=0.62, gap=0.1)
        brace = Brace(x, DOWN, color=YELLOW, buff=0.15)
        blab = MathTex(r"\approx \log_{10} x\ \text{digits}", font_size=44, color=YELLOW).next_to(brace, DOWN, buff=0.15)
        o, o_lab, o_glow = big_o(r"O(\log x)", GREEN, 0.0, "time")

        self.seg(13)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in x], lag_ratio=0.06), rt=0.8)
        self.beat(GrowFromCenter(brace), FadeIn(blab), rt=0.7)
        self.until(DUR[13] * 0.55)
        self.beat(Write(o), FadeIn(o_glow), FadeIn(o_lab), rt=0.8)
        self.close_seg()

        vars_ = VGroup(*[pill(s, c, 28) for s, c in [("x", CYAN), ("d", YELLOW), ("rev", GREEN)]]).arrange(RIGHT, buff=0.3).move_to([0, -2.0, 0])
        so, so_lab, so_glow = big_o(r"O(1)", VIOLET, -3.7, "extra space", size=72)

        self.seg(14)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in vars_], lag_ratio=0.15), rt=0.7)
        self.beat(Write(so), FadeIn(so_glow), FadeIn(so_lab), rt=0.8)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.0)
        cglow = glow(code.background, VIOLET, max_w=22, max_op=0.25)
        bar = line_bar(code, 5, 5, YELLOW)
        d = DUR[15]

        self.seg(15)
        self.beat(FadeIn(code.background), FadeIn(cglow), rt=0.3)
        self.beat(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08),
                  FadeIn(code.line_numbers), rt=0.8)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(d * 0.35)
        self.beat(Transform(bar, line_bar(code, 8, 8, GREEN)), rt=0.4)
        self.until(d * 0.65)
        self.beat(Transform(bar, line_bar(code, 6, 7, RED)), rt=0.4)
        self.close_seg()

        tag = VGroup(T("Never trust", 66), T("the overflow.", 66)).arrange(DOWN, buff=0.15)
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
