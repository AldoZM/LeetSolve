WALK = json.load(open('walk.json', encoding='utf-8'))
H, ORES = WALK["heights"], WALK["ores"]
WATER = "#3F76E4"

BRUTE_CODE = """def maxArea(height):
    best = 0
    for i in range(len(height)):
        for j in range(i + 1, len(height)):
            best = max(best, min(height[i], height[j]) * (j - i))
    return best"""

CODE = """def maxArea(height):
    l, r = 0, len(height) - 1
    best = 0
    while l < r:
        h = min(height[l], height[r])
        best = max(best, h * (r - l))
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return best"""


class Pillars(VGroup):
    """The heights as pillars of ore blocks on a base line; the top block shows the height. cols[i] is pillar i."""

    def __init__(self, base, size=0.5, gap=0.22, **kwargs):
        super().__init__(**kwargs)
        self.size, self.base = size, base
        self.cols = VGroup()
        for i, h in enumerate(H):
            col = VGroup()
            for k in range(h):
                if k == h - 1:
                    b = Block(h, f"{ORES[i]}_ore", size)
                else:
                    b = VGroup(pixel_art(f"{ORES[i]}_ore", size),
                               Square(size, stroke_color="#000000", stroke_width=2, stroke_opacity=0.5, fill_opacity=0))
                b.move_to([0, base + size * (k + 0.5), 0])
                col.add(b)
            self.cols.add(col)
        self.cols.arrange(RIGHT, buff=gap, aligned_edge=DOWN)
        self.cols.move_to([0, base + self.cols.height / 2, 0])
        self.idx = VGroup(*[MT(str(i), 28, MC_GRAY).next_to(c, DOWN, buff=0.12) for i, c in enumerate(self.cols)])
        self.add(self.cols, self.idx)

    def water(self, l, r, color=WATER, opacity=0.6):
        # Water between walls l and r, up to the shorter one
        h = min(H[l], H[r]) * self.size
        x0, x1 = self.cols[l].get_right()[0], self.cols[r].get_left()[0]
        w = Rectangle(width=x1 - x0, height=h, stroke_width=0, fill_color=color, fill_opacity=opacity)
        w.move_to([(x0 + x1) / 2, self.base + h / 2, 0])
        return w


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def eq_line(parts, size=34, font=PIXEL, buff=0.3):
    return VGroup(*[MT(s, size, c, font) for s, c in parts]).arrange(RIGHT, buff=buff)


def pulse(m, k=1.15):
    # Emphasis that keeps the pixel art's colors (Indicate would paint it one flat color)
    return m.animate(rate_func=there_and_back).scale(k)


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("CONTAINER WITH", width=8.0).move_to([0, 4.85, 0])
    t2 = stone_title("MOST WATER", width=6.4).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.45, 2.75, 0])
    p = Pillars(-1.2, 0.5)
    water = p.water(1, 5)
    area = MT("16", 44, MC_WHITE, PIXEL).move_to(water)
    tags = VGroup(chat("LeetCode #11", MC_AQUA, 46), chat("Medium", MC_GOLD, 46), chat("Two Pointers", MC_GREEN, 46))
    tags.arrange(RIGHT, buff=0.22).move_to([0, -3.05, 0])
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    # Water goes behind the pillars
    return VGroup(ground, t1, t2, spl, water, p, area, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, water, p, area, tags = art
        self.add(art)

        self.seg(0)
        self.beat(pulse(spl), rt=0.8)
        self.sfx("stone_dig1", 0.35, delay=0.35)
        self.beat(LaggedStart(*[c.animate(rate_func=there_and_back).shift(UP * 0.3) for c in p.cols], lag_ratio=0.18), rt=1.6)
        self.sfx("orb", 0.3, delay=0.3)
        self.beat(pulse(area, 1.3), *[ShowPassingFlash(outline(p.cols[k], MC_GOLD, 10), time_width=0.6) for k in (1, 5)], rt=0.9)
        self.beat(pulse(spl), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        p = Pillars(-0.2, 0.62)
        lab = MT("height", 40, MC_WHITE).next_to(p, UP, buff=0.25).align_to(p, LEFT)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        # Pillars grow block by block
        for k, c in enumerate(p.cols):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.28, delay=0.1 + 0.15 * k)
        self.beat(LaggedStart(*[LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in c], lag_ratio=0.25) for c in p.cols],
                              lag_ratio=0.15), FadeIn(p.idx), rt=1.8)
        self.beat(FadeIn(lab), rt=0.3)
        walls = VGroup(outline(p.cols[1], MC_YELLOW, 8), outline(p.cols[5], MC_YELLOW, 8))
        self.until(min(3.4, DUR[1] - 1.0))
        self.beat(Create(walls), rt=0.5)
        self.close_seg()

        self.seg(2)
        water = p.water(1, 5)
        self.add(water)
        self.bring_to_back(water)
        water.stretch(0.01, 1, about_edge=DOWN)
        self.until(0.5)
        self.sfx("pop", 0.3)
        self.beat(water.animate.stretch(100, 1, about_edge=DOWN), rt=1.0)
        lim = MT("shorter wall", 36, MC_AQUA).next_to(p.cols[1], LEFT, buff=0.2).shift(UP * 0.6)
        self.beat(FadeIn(lim), rt=0.3)
        area = eq_line([("4", MC_AQUA), ("x", MC_GRAY), ("4", MC_WHITE), ("=", MC_GRAY), ("16", MC_GOLD)], 40).move_to([0, -2.4, 0])
        self.until(min(3.6, DUR[2] - 0.9))
        self.sfx("orb", 0.3)
        self.beat(FadeIn(area, shift=UP * 0.2), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("EVERY PAIR", MC_RED)
        p = Pillars(0.9, 0.42)
        code = code_panel(BRUTE_CODE, -3.7, max_h=2.9)
        pick = pickaxe(1.0).move_to([-2.9, -0.5, 0])
        dbg = Rectangle(width=1.2, height=0.16, fill_color="#000000", fill_opacity=1, stroke_width=0)
        dbg.next_to(pick, DOWN, buff=0.15)
        pairs = [(i, j) for i in range(len(H)) for j in range(i + 1, len(H))]

        def dfill(frac):
            r = Rectangle(width=max(1.16 * frac, 0.02), height=0.1, stroke_width=0, fill_opacity=1,
                          fill_color=interpolate_color(ManimColor(MC_RED), ManimColor(MC_GREEN), frac))
            r.move_to(dbg.get_left() + RIGHT * (0.02 + max(1.16 * frac, 0.02) / 2))
            return r

        def counter(k):
            c = MT(f"pairs {k}", 32, MC_WHITE, PIXEL)
            c.move_to([1.2, -0.5, 0])
            return c

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(p, shift=DOWN * 0.3), rt=0.8)
        self.until(1.4)
        self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
        self.close_seg()

        fill, cnt = dfill(1.0), counter(0)
        water = p.water(0, 1)
        bar = line_bar(code, 4, 4, MC_YELLOW)
        self.seg(4)
        self.add(water)
        self.bring_to_back(water)
        self.beat(FadeIn(pick, scale=0.6), FadeIn(dbg), FadeIn(fill), FadeIn(cnt), FadeIn(bar), FadeIn(water), rt=0.5)

        def check(k, rt):
            i, j = pairs[k]
            self.sfx(f"stone_dig{k % 4 + 1}", 0.2, delay=rt * 0.5)
            self.beat(Transform(water, p.water(i, j)), Transform(fill, dfill(1 - (k + 1) / 22)), Transform(cnt, counter(k + 1)),
                      Rotate(pick, angle=-25 * DEGREES, rate_func=there_and_back), rt=rt)

        n4 = 7
        for k in range(n4):
            check(k, min(0.45, (DUR[4] - 0.8) / n4))
        self.close_seg()

        self.seg(5)
        for k in range(n4, len(pairs)):
            check(k, min(0.24, (DUR[5] - 1.6) / (len(pairs) - n4)))
        broken = MT("almost broken!", 32, MC_RED).next_to(dbg, DOWN, buff=0.12)
        self.sfx("break", 0.45)
        self.beat(Wiggle(pick), FadeIn(broken, shift=UP * 0.1), rt=0.7)
        self.close_seg()

        self.seg(6)
        self.beat(FadeOut(VGroup(p, water, code, bar, pick, dbg, fill, cnt, broken)), rt=0.5)
        n = eq_line([("n =", MC_GRAY), ("1,000,000", MC_WHITE)], 32)
        n.move_to([0, 2.6, 0])
        self.beat(FadeIn(n, shift=UP * 0.2), rt=0.4)
        big = MT("500,000,000,000", 40, MC_RED, PIXEL).move_to([0, 1.0, 0])
        pl = MT("pairs", 52, MC_GRAY).next_to(big, DOWN, buff=0.25)
        self.until(min(2.2, DUR[6] - 2.0))
        self.beat(FadeIn(big, scale=1.4), FadeIn(pl), rt=0.5)
        o = big_o_pow("n", 2, 72, MC_RED).move_to([0, -1.9, 0])
        self.until(DUR[6] - 1.1)
        self.beat(FadeIn(o, scale=0.5), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        p = Pillars(0.3, 0.55)
        L = MT("L", 40, MC_AQUA, PIXEL)
        R = MT("R", 40, MC_GOLD, PIXEL)

        def place(m, i):
            return m.copy().next_to(p.idx[i], DOWN, buff=0.15)

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(p, shift=DOWN * 0.2), rt=0.6)
        water = p.water(0, 6)
        self.add(water)
        self.bring_to_back(water)
        water.stretch(0.01, 1, about_edge=DOWN)
        lm, rm = place(L, 0), place(R, 6)
        self.until(min(1.8, DUR[7] - 1.8))
        self.sfx("pop", 0.3)
        self.beat(water.animate.stretch(100, 1, about_edge=DOWN), FadeIn(lm, shift=UP * 0.2), FadeIn(rm, shift=UP * 0.2), rt=0.7)
        a = eq_line([("2", MC_AQUA), ("x", MC_GRAY), ("6", MC_WHITE), ("=", MC_GRAY), ("12", MC_GOLD)], 36).move_to([0, -1.9, 0])
        self.beat(FadeIn(a, shift=UP * 0.15), rt=0.4)
        self.close_seg()

        self.seg(8)
        short = outline(p.cols[0], MC_RED, 8)
        self.until(0.2)
        self.beat(Create(short), rt=0.4)
        # Moving the taller wall: narrower, and still capped by the short one
        ghost = p.water(0, 5, MC_RED, 0.35)
        worse = eq_line([("2", MC_AQUA), ("x", MC_GRAY), ("5", MC_WHITE), ("=", MC_GRAY), ("10", MC_RED)], 36).move_to([0, -1.9, 0])
        self.until(min(2.4, DUR[8] - 5.0))
        self.sfx("villager_no1", 0.3)
        self.beat(Transform(water, ghost), rm.animate.next_to(p.idx[5], DOWN, buff=0.15), Transform(a, worse), rt=0.6)
        self.until(min(4.6, DUR[8] - 2.6))
        good = p.water(1, 6)
        better = eq_line([("3", MC_AQUA), ("x", MC_GRAY), ("5", MC_WHITE), ("=", MC_GRAY), ("15", MC_GREEN)], 36).move_to([0, -1.9, 0])
        rule = MT("move the shorter wall", 46, MC_GOLD).move_to([0, -3.1, 0])
        self.sfx("orb", 0.3)
        self.beat(Transform(water, good), rm.animate.next_to(p.idx[6], DOWN, buff=0.15), lm.animate.next_to(p.idx[1], DOWN, buff=0.15),
                  short.animate.move_to(p.cols[1]).set_stroke(MC_YELLOW), Transform(a, better), rt=0.6)
        self.beat(FadeIn(rule, shift=UP * 0.15), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("TWO POINTERS", MC_GREEN)
        code = code_panel(CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 3, 3, MC_YELLOW)

        def chip(b):
            return chat(f"best {b}", MC_GOLD if b else MC_WHITE, 40).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)

        def formula(s, said=False):
            parts = [(f"min({H[s['l']]}, {H[s['r']]})", MC_AQUA), ("x", MC_GRAY), (str(s["r"] - s["l"]), MC_WHITE)]
            if said:
                parts += [("=", MC_GRAY), (str(s["area"]), MC_GOLD if s["new"] else MC_WHITE)]
            return eq_line(parts, 34, buff=0.22).move_to([0, -1.1, 0])

        st = {"chip": chip(0), "f": None}

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("intro", "measure_demo", "stop", "toast", "answer")]
        for k, s in enumerate(W["steps"]):
            for kind in ("measure", "said", "move"):
                ev.append((seg_time(W["first"], s[kind]), kind, k))
        ev.sort(key=lambda e: e[0])

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(st["chip"]), rt=0.35)

        def on(kind, k):
            if kind == "intro":
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
            elif kind == "measure_demo":
                self.beat(FadeIn(bar), Transform(bar, line_bar(code, 1, 1, MC_YELLOW)), rt=0.3)
            elif kind == "measure":
                s = W["steps"][k]
                f = formula(s)
                anims = [Transform(bar, line_bar(code, 4, 4, MC_YELLOW))]
                if st["f"] is None:
                    st["f"] = f
                    anims.append(FadeIn(f, shift=UP * 0.1))
                else:
                    anims.append(Transform(st["f"], f))
                self.sfx("click", 0.28)
                self.beat(*anims, rt=0.2)
            elif kind == "said":
                s = W["steps"][k]
                anims = [Transform(st["f"], formula(s, True)), Transform(bar, line_bar(code, 5, 5, MC_GREEN if s["new"] else MC_YELLOW))]
                if s["new"]:
                    anims.append(Transform(st["chip"], chip(s["best"])))
                    for d in (0.0, 0.15, 0.3):
                        self.sfx("orb", 0.26, delay=d)
                else:
                    self.sfx("pop", 0.25)
                self.beat(*anims, rt=0.22)
            elif kind == "move":
                s = W["steps"][k]
                line = 7 if s["side"] == "l" else 9
                self.sfx(f"stone_step{k % 6 + 1}", 0.3)
                self.beat(Transform(bar, line_bar(code, line, line, MC_AQUA if s["side"] == "l" else MC_GOLD)), rt=0.15)
            elif kind == "stop":
                self.beat(Transform(bar, line_bar(code, 10, 10, MC_GREEN)), FadeOut(st["f"]), rt=0.3)
            elif kind == "toast":
                t = toast("Advancement Made!", "Most water: 16", w=4.6)
                t.move_to([0, 5.5, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(st["chip"]), rt=0.5)
            elif kind == "answer":
                ans = chat("return 16", MC_GREEN, 60)
                ans.move_to([0, 4.3, 0])
                self.beat(FadeIn(ans, shift=UP * 0.2), rt=0.4)

        def on_last():
            # The 3D clip fades to sky at its end; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        look = VGroup(MT("1 pointer moves", 48, MC_WHITE), MT("per step", 48, MC_GRAY)).arrange(RIGHT, buff=0.3)
        look.move_to([0, 3.4, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n)", 1.05)).arrange(RIGHT, buff=0.4)
        tm.move_to([0, 1.65, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.6, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in look], lag_ratio=0.25), rt=0.6)
        self.until(min(2.0, DUR[16] - 1.8))
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.4)
        self.add(xp)
        for d in (0.0, 0.3, 0.6, 0.9):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=1.1)
        self.beat(Restore(xp), rt=1.2)
        self.close_seg()

        self.seg(17)
        old = big_o_pow("n", 2, 44, MC_RED)
        arrow = MT("->", 70, MC_GRAY)
        new = MT("O(n)", 44, MC_GREEN, PIXEL)
        cmp = VGroup(old, arrow, new).arrange(RIGHT, buff=0.45).move_to([0, -1.0, 0])
        strike = Line(old.get_left() + LEFT * 0.1, old.get_right() + RIGHT * 0.1, color=MC_RED, stroke_width=8)
        mem = VGroup(MT("memory", 52, MC_GRAY), MT("O(1)", 44, MC_GOLD, PIXEL)).arrange(RIGHT, buff=0.35).move_to([0, -2.8, 0])
        self.beat(FadeIn(old, shift=UP * 0.15), rt=0.4)
        self.until(min(1.2, DUR[17] - 2.4))
        self.beat(Create(strike), FadeIn(arrow), FadeIn(new, shift=LEFT * 0.2), rt=0.5)
        self.until(min(2.4, DUR[17] - 1.2))
        self.beat(FadeIn(mem, shift=UP * 0.15), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.6, width=8.4)
        bar = line_bar(code, 1, 1, MC_YELLOW)

        self.seg(18)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(min(1.4, DUR[18] - 1.4))
        self.beat(Transform(bar, line_bar(code, 3, 3, MC_AQUA)), rt=0.3)
        self.until(DUR[18] - 0.8)
        self.beat(Transform(bar, line_bar(code, 6, 9, MC_GOLD)), rt=0.3)
        self.close_seg()

        self.seg(19)
        msg = chat("Always move the shorter wall", MC_GOLD, 54).move_to([0, -2.6, 0])
        self.until(0.1)
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.5)
        self.until(DUR[19] - 1.9)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.5)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=1.0)
        self.close_seg()
