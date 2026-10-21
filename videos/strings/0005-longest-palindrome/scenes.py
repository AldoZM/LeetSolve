WALK = json.load(open('walk.json', encoding='utf-8'))
S = WALK["s"]
CENTERS = WALK["centers"]

CODE = """def longestPalindrome(s):
    best = ""
    for c in range(2 * len(s) - 1):
        l, r = c // 2, (c + 1) // 2
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l, r = l - 1, r + 1
        if r - l - 1 > len(best):
            best = s[l + 1:r]
    return best"""


def letters(y, size=0.72, gap=0.1, text=S, color=CYAN):
    return tile_row(list(text), color, y, size, gap)


def arch(row, l, r, color=GREEN, width=4):
    # Arc over the row joining two mirrored letters
    a, b = row[l].get_top() + UP * 0.08, row[r].get_top() + UP * 0.08
    return ArcBetweenPoints(a, b, angle=-PI * 0.75, color=color, stroke_width=width)


def ticks(x, top, bottom, color, length=0.3):
    # Center marks above and below a row, so they never cover the letter
    return VGroup(Line([x, top + 0.06, 0], [x, top + 0.06 + length, 0], color=color, stroke_width=6),
                  Line([x, bottom - 0.06, 0], [x, bottom - 0.06 - length, 0], color=color, stroke_width=6))


def cover():
    # Opening frame and closing frame are the same, so the video loops seamlessly
    title, tglow = gradient_title(["Longest", "Palindromic", "Substring"], size=80, y=3.4)
    row = letters(-1.2)
    arcs = VGroup(*[arch(row, 6 - d, 6 + d, YELLOW if d == 0 else GREEN) for d in (1, 2, 3)])
    center = ticks(row[6].get_x(), row[6].get_top()[1], row[6].get_bottom()[1], YELLOW)
    return title, tglow, VGroup(row, arcs, center)


class Scene1_Hook(Base):
    def construct(self):
        title, tglow, art = cover()
        self.add(tglow, title, art)
        row, arcs, center = art
        rng = random.Random(5)
        bg = VGroup(*[
            M(rng.choice("abcdefghijklmnopqrstuvwxyz"), rng.randint(18, 34), rng.choice([CYAN, MAGENTA, VIOLET]))
            .set_opacity(rng.uniform(0.12, 0.28))
            .move_to([rng.uniform(-4.1, 4.1), rng.choice([rng.uniform(-5.6, -3.9), rng.uniform(5.0, 5.7)]), 0])
            for _ in range(22)
        ])
        tags = tags_block([("LeetCode #5", CYAN), ("Medium", YELLOW), ("Expand around center", VIOLET)], y=-3.6)

        self.seg(0)
        self.beat(LaggedStart(*[FadeIn(d, scale=0.4) for d in bg], lag_ratio=0.04),
                  LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in [*tags[0], *tags[1]]], lag_ratio=0.3), rt=1.0)
        self.beat(LaggedStart(*[ShowPassingFlash(a.copy().set_stroke(WHITE, width=8), time_width=0.6) for a in arcs], lag_ratio=0.25), rt=1.0)
        self.until(DUR[0] - 1.05)
        self.beat(FadeOut(VGroup(title, tglow, tags, bg, arcs, center)), rt=0.45)
        self.beat(row.animate.move_to([0, 3.0, 0]), rt=0.55)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        row = letters(3.0)
        self.add(row)
        hdr = header("THE PROBLEM", CYAN)
        idx = index_labels(row)

        def mirror_check(text, y, ok):
            fwd = M(text, 44, CYAN)
            back = M(text[::-1], 44, CYAN)
            mark = T("✓" if ok else "✗", 40, GREEN if ok else RED)
            arrow = M("→", 40, MUTED)
            return VGroup(fwd, arrow, back, mark).arrange(RIGHT, buff=0.35).move_to([0, y, 0])

        good = mirror_check("aba", 1.2, True)
        bad = mirror_check("bar", 0.1, False)

        self.seg(1)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(idx), rt=0.5)
        self.beat(*[restyle(t, lambda x: x.box.set_stroke(GREEN, width=4)) for t in row[0:3]], FadeIn(good, shift=UP * 0.2), rt=0.7)
        self.until(DUR[1] * 0.5)
        self.beat(*[restyle(t, lambda x: x.box.set_stroke(CYAN, width=3)) for t in row[0:3]],
                  *[restyle(t, lambda x: x.box.set_stroke(RED, width=4)) for t in row[1:4]], FadeIn(bad, shift=UP * 0.2), rt=0.7)
        self.close_seg()

        arcs = VGroup(*[arch(row, 6 - d, 6 + d) for d in (1, 2, 3)])
        ans = VGroup(T("answer", 30, MUTED), M('"racecar"', 64, YELLOW)).arrange(DOWN, buff=0.15).move_to([0, -1.5, 0])
        aglow = glow(ans[1], YELLOW, layers=6, max_w=14, max_op=0.28)

        self.seg(2)
        self.beat(FadeOut(VGroup(good, bad)), *[restyle(t, lambda x: x.box.set_stroke(CYAN, width=3)) for t in row[1:4]], rt=0.4)
        self.beat(*[restyle(t, lambda x: x.box.set_stroke(YELLOW, width=4).set_fill(YELLOW, opacity=0.15)) for t in row[3:]],
                  LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.3), rt=1.0)
        self.beat(FadeIn(ans, shift=UP * 0.2), FadeIn(aglow), rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        hdr = header("BRUTE FORCE", RED)
        row = letters(3.4)
        n = len(S)
        frame = SurroundingRectangle(VGroup(*row[0:2]), color=MUTED, buff=0.06, corner_radius=0.1)
        lab = MathTex(r"\tfrac{n^2}{2}\ \text{substrings}", font_size=50, color=INK).move_to([0, 1.2, 0])
        lab2 = MathTex(r"\times\ n\ \text{to check each}", font_size=50, color=MUTED).move_to([0, 0.2, 0])
        o, o_lab, o_glow = big_o(r"O(n^3)", RED, -2.0, "time")
        pairs = [(0, 4), (1, 5), (2, 8), (3, 6), (4, 9), (0, 9)]

        self.seg(3)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(row), FadeIn(frame), rt=0.5)
        for a, b in pairs:
            ok = S[a:b + 1] == S[a:b + 1][::-1]
            self.beat(Transform(frame, SurroundingRectangle(VGroup(*row[a:b + 1]), color=GREEN if ok else RED, buff=0.06,
                                                            corner_radius=0.1)), rt=0.35)
        self.beat(Write(lab), rt=0.6)
        self.beat(FadeIn(lab2, shift=UP * 0.2), rt=0.5)
        self.beat(Write(o), FadeIn(o_glow), FadeIn(o_lab), rt=0.8)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        hdr = header("THE IDEA", YELLOW)
        word = letters(2.2, size=0.95, gap=0.14, text="racecar")
        mirror = DashedLine(word[3].get_top() + UP * 0.9, word[3].get_bottom() + DOWN * 0.9, color=YELLOW, stroke_width=4)
        mlab = T("center", 26, YELLOW).next_to(mirror, UP, buff=0.1)

        self.seg(4)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in word], lag_ratio=0.08), rt=0.8)
        self.until(DUR[4] * 0.45)
        self.beat(Create(mirror), FadeIn(mlab), rt=0.6)
        self.beat(*[ring(word[3 - d].box, YELLOW) for d in (1, 2, 3)], *[ring(word[3 + d].box, YELLOW) for d in (1, 2, 3)], rt=0.8)
        self.close_seg()

        arcs = [arch(word, 3 - d, 3 + d, GREEN, 5) for d in (1, 2, 3)]
        l_ptr = Arrow(DOWN * 0.3, UP * 0.3, buff=0, color=MAGENTA, stroke_width=6, tip_length=0.18).next_to(word[3], DOWN, buff=0.15)
        r_ptr = Arrow(DOWN * 0.3, UP * 0.3, buff=0, color=CYAN, stroke_width=6, tip_length=0.18).next_to(word[3], DOWN, buff=0.15)

        self.seg(5)
        self.beat(FadeIn(l_ptr), FadeIn(r_ptr), rt=0.3)
        for d in (1, 2, 3):
            self.beat(l_ptr.animate.next_to(word[3 - d], DOWN, buff=0.15), r_ptr.animate.next_to(word[3 + d], DOWN, buff=0.15),
                      Create(arcs[d - 1]), rt=0.7)
        self.close_seg()

        odd = letters(-1.0, size=0.8, text="aba")
        even = letters(-3.4, size=0.8, text="abba")
        odd_c = ticks(odd[1].get_x(), odd.get_top()[1], odd.get_bottom()[1], YELLOW)
        gap_x = (even[1].get_right()[0] + even[2].get_left()[0]) / 2
        even_c = ticks(gap_x, even.get_top()[1], even.get_bottom()[1], MAGENTA)
        odd_l = T("letter center: odd length", 26, YELLOW).next_to(odd, DOWN, buff=0.4)
        even_l = T("gap center: even length", 26, MAGENTA).next_to(even, DOWN, buff=0.4)

        self.seg(6)
        self.beat(VGroup(word, mirror, mlab, l_ptr, r_ptr, *arcs).animate.scale(0.8).shift(UP * 0.9), rt=0.5)
        self.beat(FadeIn(odd), Create(odd_c), FadeIn(odd_l), rt=0.7)
        self.until(DUR[6] * 0.5)
        self.beat(FadeIn(even), Create(even_c), FadeIn(even_l), rt=0.7)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        hdr = header("EXPAND AROUND CENTER", YELLOW)
        code = code_panel(CODE, -3.85)

        def readout(c, best):
            where = S[c // 2] if c % 2 == 0 else f"{S[c // 2]}|{S[c // 2 + 1]}"
            parts = VGroup(pill(f"center {where}", YELLOW if c % 2 == 0 else MAGENTA, 28), pill(f"best {best}", GREEN, 28))
            return parts.arrange(RIGHT, buff=0.35).move_to([0, -1.35, 0])

        st = {"c": 0, "best": '""'}
        ro = readout(0, '""')
        bar = line_bar(code, 1)

        # Events: every center start, the comparisons of the two slow centers, and each new best
        events = []
        for k, e in enumerate(CENTERS):
            events.append((seg_time(WALK["first"], e["start"]), "center", (k, 0)))
            if not e["fast"]:
                for j, tm in enumerate(e["times"]):
                    events.append((seg_time(WALK["first"], tm), "cmp", (k, j)))
            if "best" in e:
                events.append((seg_time(WALK["first"], e["best"]), "best", (k, 0)))
        events.sort(key=lambda x: x[0])

        def intro():
            self.until(0.3)
            self.beat(FadeIn(hdr, shift=RIGHT * 0.3), rt=0.5)
            self.until(1.0)
            self.beat(FadeIn(code, shift=UP * 0.3), rt=0.8)
            self.until(2.2)
            self.beat(FadeIn(bar), FadeIn(ro), rt=0.4)

        def on(kind, key):
            k, j = key
            e = CENTERS[k]
            if kind == "center":
                st["c"] = e["c"]
                rt = 0.2 if e["fast"] else 0.3
                self.beat(Transform(bar, line_bar(code, 2, 3)), Transform(ro, readout(st["c"], st["best"])), rt=rt)
            elif kind == "cmp":
                kind_ = e["cmps"][j][2]
                if kind_ == "match":
                    self.beat(Transform(bar, line_bar(code, 4, 5, GREEN)), rt=0.3)
                else:
                    self.beat(Transform(bar, line_bar(code, 4, 4, RED)), rt=0.3)
            elif kind == "best":
                l, r, _ = e["cmps"][-1]
                st["best"] = f'"{S[l + 1:r]}"'
                self.beat(Transform(bar, line_bar(code, 6, 7, GREEN)), Transform(ro, readout(st["c"], st["best"])), rt=0.25)

        def outro():
            d = DUR[WALK["last"]]
            self.until(d - 0.9)
            self.beat(Transform(bar, line_bar(code, 8, 8, GREEN)), rt=0.3)
            self.finish(FadeOut(VGroup(hdr, ro, code, bar)), rt=0.5)

        self.run_events(WALK, events, on, intro, outro)


class Scene6_Complexity(Base):
    def construct(self):
        hdr = header("COMPLEXITY", GREEN)
        row = letters(3.6, size=0.62, gap=0.1)
        marks = VGroup()
        for c in range(2 * len(S) - 1):
            if c % 2 == 0:
                x = row[c // 2].get_x()
                marks.add(Dot([x, 2.85, 0], radius=0.07, color=YELLOW))
            else:
                x = (row[c // 2].get_right()[0] + row[c // 2 + 1].get_left()[0]) / 2
                marks.add(Dot([x, 2.85, 0], radius=0.07, color=MAGENTA))
        cl = MathTex(r"2n - 1\ \text{centers}", font_size=46, color=INK).move_to([0, 2.05, 0])
        o, o_lab, o_glow = big_o(r"O(n^2)", GREEN, 0.4, "time")

        self.seg(13)
        self.beat(FadeIn(hdr, shift=RIGHT * 0.3), FadeIn(row), rt=0.5)
        self.beat(LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.06), FadeIn(cl), rt=1.2)
        self.until(DUR[13] * 0.55)
        self.beat(Write(o), FadeIn(o_glow), FadeIn(o_lab), rt=0.8)
        self.close_seg()

        ptrs = VGroup(*[pill(s, c, 28) for s, c in [("l", MAGENTA), ("r", CYAN), ("best range", GREEN)]]).arrange(RIGHT, buff=0.3)
        ptrs.move_to([0, -1.7, 0])
        so, so_lab, so_glow = big_o(r"O(1)", VIOLET, -3.5, "extra space", size=72)

        self.seg(14)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in ptrs], lag_ratio=0.15), rt=0.8)
        self.beat(Write(so), FadeIn(so_glow), FadeIn(so_lab), rt=0.8)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.0)
        cglow = glow(code.background, VIOLET, max_w=22, max_op=0.25)
        bar = line_bar(code, 2, 3, YELLOW)
        d = DUR[15]

        self.seg(15)
        self.beat(FadeIn(code.background), FadeIn(cglow), rt=0.3)
        self.beat(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08),
                  FadeIn(code.line_numbers), rt=0.8)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(d * 0.55)
        self.beat(Transform(bar, line_bar(code, 4, 5, GREEN)), rt=0.4)
        self.close_seg()

        tag = VGroup(T("Every palindrome", 60), T("has a middle.", 60)).arrange(DOWN, buff=0.15)
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
