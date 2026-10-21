S = "abcbdea"
WALK = json.load(open('walk.json', encoding='utf-8'))


def trace():
    # One entry per right index: the map lookup, the left edge before and after, and the best so far
    last, left, best, out = {}, 0, 0, []
    for r, ch in enumerate(S):
        prev = last.get(ch, -1)
        jump = prev >= left
        new_left = prev + 1 if jump else left
        best = max(best, r - new_left + 1)
        out.append({"r": r, "ch": ch, "prev": prev, "jump": jump, "left0": left, "left": new_left, "best": best})
        last[ch] = r
        left = new_left
    return out


STEPS = trace()

CODE = """def lengthOfLongestSubstring(s):
    last = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best"""


def letters(y, size=0.85, gap=0.14, color=CYAN):
    return tile_row(list(S), color, y, size, gap)


def window(row, a, b, color=YELLOW, pad=0.1, op=0.12):
    tiles = VGroup(*row[a:b + 1])
    return RoundedRectangle(corner_radius=0.16, width=tiles.width + 2 * pad, height=tiles.height + 2 * pad,
                            fill_color=color, fill_opacity=op, stroke_color=color, stroke_width=3).move_to(tiles)


def cover():
    # Opening frame and closing frame are the same, so the video loops seamlessly
    title, tglow = gradient_title(["Longest Substring", "Without Repeating", "Characters"], size=64, y=3.2)
    row = letters(-0.6)
    win = window(row, 2, 6)
    return title, tglow, VGroup(win, row)


class Scene1_Hook(Base):
    def construct(self):
        title, tglow, art = cover()
        self.add(tglow, title, art)
        win, row = art

        rng = random.Random(3)
        bg = VGroup(*[
            M(rng.choice("abcdefghijklmnopqrstuvwxyz"), rng.randint(18, 36), rng.choice([CYAN, MAGENTA, VIOLET]))
            .set_opacity(rng.uniform(0.12, 0.28))
            .move_to([rng.uniform(-4.1, 4.1), rng.choice([rng.uniform(-5.6, -3.0), rng.uniform(5.0, 5.7), rng.uniform(0.7, 1.1)]), 0])
            for _ in range(26)
        ])
        tags = tags_block([("LeetCode #3", CYAN), ("Medium", YELLOW), ("Sliding window", VIOLET)], y=-3.3)

        self.seg(0)
        self.beat(Indicate(title, color=WHITE, scale_factor=1.04), rt=0.7)
        self.beat(LaggedStart(*[FadeIn(d, scale=0.4) for d in bg], lag_ratio=0.04),
                  LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in [*tags[0], *tags[1]]], lag_ratio=0.3), rt=1.2)
        self.beat(LaggedStart(*[ring(t.box, YELLOW) for t in row[2:]], lag_ratio=0.12), rt=1.2)
        self.until(DUR[0] - 1.1)
        self.beat(FadeOut(VGroup(title, tglow, tags, bg, win)), rt=0.45)
        self.beat(row.animate.move_to([0, 2.8, 0]), rt=0.55)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        row = letters(2.8)
        self.add(row)
        hdr = header("THE PROBLEM", CYAN)
        s_lab = M('s = "abcbdea"', 34, INK).move_to([0, 4.2, 0])
        s_lab[3:].set_color(CYAN)
        idx = index_labels(row)

        good = Brace(VGroup(*row[0:3]), DOWN, color=GREEN, buff=0.45)
        good_t = T("abc  no repeats", 26, GREEN).next_to(good, DOWN, buff=0.12)
        bad = Brace(VGroup(*row[0:4]), DOWN, color=RED, buff=0.45)
        bad_t = T("abcb  b repeats", 26, RED).next_to(bad, DOWN, buff=0.12)

        self.seg(1)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(s_lab, shift=DOWN * 0.2), rt=0.6)
        self.beat(LaggedStart(*[FadeIn(i, shift=UP * 0.1) for i in idx], lag_ratio=0.08), rt=0.6)
        self.beat(GrowFromCenter(good), FadeIn(good_t), *[restyle(t, lambda x: x.box.set_stroke(GREEN, width=4)) for t in row[0:3]], rt=0.7)
        self.until(DUR[1] * 0.55)
        self.beat(ReplacementTransform(good, bad), FadeOut(good_t), FadeIn(bad_t),
                  *[restyle(t, lambda x: x.box.set_stroke(CYAN, width=3)) for t in row[0:3]],
                  *[restyle(row[k], lambda x: x.box.set_stroke(RED, width=4).set_fill(RED, opacity=0.25)) for k in (1, 3)], rt=0.7)
        self.close_seg()

        win = window(row, 2, 6)
        ans = VGroup(T("longest", 30, MUTED), M("5", 120, YELLOW)).arrange(DOWN, buff=0.1).move_to([0, -1.4, 0])
        aglow = glow(ans[1], YELLOW, layers=6, max_w=16, max_op=0.3)
        run = M('"cbdea"', 44, YELLOW).move_to([0, 0.75, 0])

        self.seg(2)
        self.beat(FadeOut(VGroup(bad, bad_t)), *[restyle(row[k], lambda x: x.box.set_stroke(CYAN, width=3).set_fill(PANEL, opacity=1)) for k in (1, 3)], rt=0.4)
        self.beat(FadeIn(win, scale=1.1), rt=0.6)
        self.beat(FadeIn(ans, shift=UP * 0.3), FadeIn(aglow), rt=0.6)
        self.until(DUR[2] * 0.5)
        self.beat(LaggedStart(*[ring(t.box, YELLOW) for t in row[2:]], lag_ratio=0.15), FadeIn(run, shift=UP * 0.2), rt=1.3)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        hdr = header("BRUTE FORCE", RED)
        row = letters(3.6)
        n = len(S)

        def has_rep(a, b):
            return len(set(S[a:b + 1])) < b - a + 1

        frame = window(row, 0, 0, GREEN)
        count = VGroup(T("substrings checked", 26, MUTED), M("1", 40, INK)).arrange(RIGHT, buff=0.3).move_to([0, 2.2, 0])

        self.seg(3)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(row, shift=DOWN * 0.2), rt=0.6)
        self.beat(FadeIn(frame), FadeIn(count), rt=0.3)
        pairs = [(a, b) for a in range(n) for b in range(a, n)]
        shown = pairs[1:16]
        per = (DUR[3] - 1.4) / len(shown)
        for k, (a, b) in enumerate(shown):
            c = RED if has_rep(a, b) else GREEN
            num = M(str(k + 2), 40, INK).move_to(count[1])
            self.beat(Transform(frame, window(row, a, b, c)), Transform(count[1], num), rt=per)
        self.close_seg()

        # Upper triangle: one cell per (start, end) pair, green when the substring has no repeats
        bars = VGroup()
        for a in range(n):
            for b in range(a, n):
                c = RED if has_rep(a, b) else GREEN
                cell = RoundedRectangle(corner_radius=0.06, width=0.5, height=0.4, fill_color=c, fill_opacity=0.5,
                                        stroke_color=c, stroke_width=1.5)
                bars.add(cell.move_to([-1.86 + b * 0.62, 1.25 - a * 0.5, 0]))
        axis_end = T("end", 22, MUTED).next_to(bars, UP, buff=0.15)
        axis_start = T("start", 22, MUTED).rotate(PI / 2).next_to(bars, LEFT, buff=0.2)
        bars = VGroup(bars, axis_end, axis_start)
        lab = MathTex(r"\approx \tfrac{n^2}{2}\ \text{substrings}", font_size=48, color=INK).move_to([0, -2.45, 0])
        times = MathTex(r"\times\ n\ \text{per check}", font_size=48, color=MUTED).move_to([0, -3.25, 0])
        o, o_lab, o_glow = big_o(r"O(n^3)", RED, -4.6, "time")

        self.seg(4)
        self.beat(FadeOut(VGroup(frame, count)), rt=0.3)
        self.beat(LaggedStart(*[FadeIn(b, scale=0.5) for b in bars[0]], lag_ratio=0.03), FadeIn(bars[1:]), rt=1.4)
        self.beat(Write(lab), rt=0.7)
        self.until(DUR[4] * 0.55)
        self.beat(FadeIn(times, shift=UP * 0.2), rt=0.5)
        self.beat(Write(o), FadeIn(o_glow), FadeIn(o_lab), rt=0.8)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        hdr = header("THE IDEA", YELLOW)
        row = letters(3.4)
        idx = index_labels(row)
        win = window(row, 0, 2)
        r_arrow = Arrow(UP * 0.35, DOWN * 0.35, buff=0, color=CYAN, stroke_width=6, tip_length=0.2)
        l_arrow = Arrow(UP * 0.35, DOWN * 0.35, buff=0, color=MAGENTA, stroke_width=6, tip_length=0.2)

        def edge_arrows(a, b):
            return (r_arrow.copy().next_to(row[b], UP, buff=0.25), l_arrow.copy().next_to(row[a], UP, buff=0.25))

        ra, la = edge_arrows(0, 2)
        r_txt = T("right: always +1", 26, CYAN).move_to([0, 1.7, 0]).align_to(row, LEFT)
        l_txt = T("left: jumps on a repeat", 26, MAGENTA).move_to([0, 1.15, 0]).align_to(row, LEFT)

        self.seg(5)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(row), FadeIn(idx), rt=0.6)
        self.beat(FadeIn(win), FadeIn(ra), FadeIn(la), rt=0.5)
        self.until(DUR[5] * 0.3)
        self.beat(FadeIn(r_txt, shift=RIGHT * 0.2), rt=0.4)
        win3 = window(row, 0, 3, RED)
        ra3, _ = edge_arrows(0, 3)
        self.beat(Transform(win, win3), Transform(ra, ra3), restyle(row[3], lambda x: x.box.set_stroke(RED, width=4)),
                  restyle(row[1], lambda x: x.box.set_stroke(RED, width=4)), rt=0.6)
        self.until(DUR[5] * 0.68)
        _, la2 = edge_arrows(2, 3)
        self.beat(Transform(win, window(row, 2, 3)), Transform(la, la2), FadeIn(l_txt, shift=RIGHT * 0.2),
                  restyle(row[1], lambda x: x.box.set_stroke(CYAN, width=3).set_opacity(0.45)),
                  restyle(row[0], lambda x: x.set_opacity(0.45)),
                  restyle(row[3], lambda x: x.box.set_stroke(CYAN, width=3)), rt=0.7)
        self.close_seg()

        # The last-seen map
        entries = [("a", 0), ("b", 1), ("c", 2)]
        panel = RoundedRectangle(corner_radius=0.2, width=4.4, height=3.3, fill_color=PANEL, fill_opacity=1,
                                 stroke_color=VIOLET, stroke_width=2).move_to([0, -2.4, 0])
        ptitle = T("last seen", 26, VIOLET).next_to(panel, UP, buff=0.15)
        rows = VGroup(*[VGroup(M(c, 40, CYAN), M("→", 36, MUTED), M(str(i), 40, INK)).arrange(RIGHT, buff=0.45)
                        for c, i in entries]).arrange(DOWN, buff=0.3).move_to(panel)
        hit = SurroundingRectangle(rows[1], color=MAGENTA, buff=0.12, corner_radius=0.1)
        link = CurvedArrow(row[3].get_bottom() + DOWN * 0.45, rows[1].get_right() + RIGHT * 0.3, angle=-1.2, color=MAGENTA,
                           stroke_width=4, tip_length=0.2)
        calc = MathTex(r"\text{left} = 1 + 1 = 2", font_size=44, color=MAGENTA).move_to([0, -4.65, 0])
        new_b = M("3", 40, YELLOW).move_to(rows[1][2])

        self.seg(6)
        self.beat(FadeIn(panel), FadeIn(ptitle), rt=0.4)
        self.beat(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rows], lag_ratio=0.2), rt=0.8)
        self.beat(Create(link), Create(hit), rt=0.7)
        self.beat(Write(calc), rt=0.6)
        self.until(DUR[6] * 0.72)
        self.beat(Transform(rows[1][2], new_b), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        hdr = header("SLIDING WINDOW", YELLOW)
        code = code_panel(CODE, -3.85)

        def readout(left, right, best):
            parts = VGroup(pill(f"left {left}", MAGENTA, 28), pill(f"right {right}", CYAN, 28), pill(f"best {best}", GREEN, 28))
            return parts.arrange(RIGHT, buff=0.3).move_to([0, -1.35, 0])

        st = {"left": 0, "right": "-", "best": 0}
        ro = readout(0, "-", 0)
        bar = line_bar(code, 1, 2)
        events = walk_events(WALK, ["start", "check", "jump", "card", "best"])

        def intro():
            self.until(0.3)
            self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(ro), rt=0.5)
            self.until(1.2)
            self.beat(FadeIn(code, shift=UP * 0.3), rt=0.8)
            self.until(2.2)
            self.beat(FadeIn(bar), rt=0.4)

        def on(kind, k):
            s = STEPS[k]
            if kind == "start":
                st["right"] = s["r"]
                self.beat(Transform(bar, line_bar(code, 3)), Transform(ro, readout(st["left"], st["right"], st["best"])), rt=0.3)
            elif kind == "check":
                self.beat(Transform(bar, line_bar(code, 4, 4, MAGENTA if s["jump"] else MUTED)), rt=0.3)
            elif kind == "jump":
                st["left"] = s["left"]
                self.beat(Transform(bar, line_bar(code, 5, 5, MAGENTA)), Transform(ro, readout(st["left"], st["right"], st["best"])), rt=0.3)
            elif kind == "card":
                self.beat(Transform(bar, line_bar(code, 6, 6, VIOLET)), rt=0.3)
            elif kind == "best":
                st["best"] = s["best"]
                self.beat(Transform(bar, line_bar(code, 7, 7, GREEN)), Transform(ro, readout(st["left"], st["right"], st["best"])), rt=0.3)

        def outro():
            d = DUR[WALK["last"]]
            self.until(d * 0.55)
            self.beat(Transform(bar, line_bar(code, 8, 8, GREEN)), rt=0.3)
            self.until(d - 0.55)
            self.beat(FadeOut(VGroup(hdr, ro, code, bar)), rt=0.5)

        self.run_events(WALK, events, on, intro, outro)


class Scene6_Complexity(Base):
    def construct(self):
        hdr = header("COMPLEXITY", GREEN)
        row = letters(3.6, size=0.75)
        rdot = Triangle(color=CYAN, fill_opacity=1).scale(0.14).rotate(PI).next_to(row[0], UP, buff=0.15)
        ldot = Triangle(color=MAGENTA, fill_opacity=1).scale(0.14).next_to(row[0], DOWN, buff=0.15)
        r_lab = T("right", 22, CYAN).next_to(row, LEFT, buff=0.25).shift(UP * 0.55)
        l_lab = T("left", 22, MAGENTA).next_to(row, LEFT, buff=0.25).shift(DOWN * 0.55)
        o, o_lab, o_glow = big_o(r"O(n)", GREEN, 0.9, "time")
        note = T("each edge moves at most n times", 26, MUTED).move_to([0, 2.1, 0])

        self.seg(13)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(row), FadeIn(rdot), FadeIn(ldot), FadeIn(r_lab), FadeIn(l_lab), rt=0.6)
        self.beat(rdot.animate.next_to(row[3], UP, buff=0.15), rt=0.6)
        self.beat(ldot.animate.next_to(row[2], DOWN, buff=0.15), rt=0.4)
        self.beat(rdot.animate.next_to(row[6], UP, buff=0.15), FadeIn(note), rt=0.8)
        self.until(DUR[13] * 0.6)
        self.beat(Write(o), FadeIn(o_glow), FadeIn(o_lab), rt=0.8)
        self.close_seg()

        cards = VGroup(*[VGroup(M(c, 34, CYAN), M("→", 30, MUTED), M(str(i), 34, INK)).arrange(RIGHT, buff=0.3)
                         for c, i in [("a", 6), ("b", 3), ("c", 2), ("d", 4), ("e", 5)]]).arrange(RIGHT, buff=0.45)
        cards.scale_to_fit_width(8.0).move_to([0, -1.6, 0])
        so, so_lab, so_glow = big_o(r"O(\min(n, |\Sigma|))", VIOLET, -3.4, "extra space", size=64)

        self.seg(14)
        self.beat(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.15), rt=1.0)
        self.beat(Write(so), FadeIn(so_glow), FadeIn(so_lab), rt=0.9)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.0)
        cglow = glow(code.background, VIOLET, max_w=22, max_op=0.25)
        bar = line_bar(code, 3, 3, CYAN)
        d = DUR[15]

        self.seg(15)
        self.beat(FadeIn(code.background), FadeIn(cglow), rt=0.3)
        self.beat(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08),
                  FadeIn(code.line_numbers), rt=0.8)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(d * 0.35)
        self.beat(Transform(bar, line_bar(code, 6, 6, VIOLET)), rt=0.4)
        self.until(d * 0.6)
        self.beat(Transform(bar, line_bar(code, 4, 5, MAGENTA)), rt=0.4)
        self.until(d - 0.6)
        self.beat(Transform(bar, line_bar(code, 0, 8, GREEN)), rt=0.5)
        self.close_seg()

        tag = VGroup(T("One pass.", 64), T("One map.", 64), T("Zero repeats.", 64)).arrange(DOWN, buff=0.15)
        tag.set_color_by_gradient(CYAN, VIOLET, MAGENTA).move_to([0, 0.8, 0])
        tag_glow = glow(tag, VIOLET, layers=6, max_w=18, max_op=0.22)
        title, tglow, art = cover()

        self.seg(16)
        self.beat(FadeOut(VGroup(code, cglow, bar), shift=UP * 0.4), rt=0.4)
        self.beat(Write(tag), FadeIn(tag_glow), rt=1.0)
        self.until(DUR[16] - 1.2)
        # Morph into the opening frame so the loop closes seamlessly
        self.beat(ReplacementTransform(tag, title), FadeOut(tag_glow), FadeIn(tglow), FadeIn(art, shift=UP * 0.3), rt=1.1)
        self.add(tglow, title, art)
        self.close_seg()
