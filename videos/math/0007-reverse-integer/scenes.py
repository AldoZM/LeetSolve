WALK = json.load(open('walk.json', encoding='utf-8'))
RUN1, RUN2 = WALK["run1"], WALK["run2"]
LIMIT = WALK["limit"]
X_ORE, R_ORE = "iron_ore", "emerald_ore"

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


def at(i, phrase, nth=0):
    # Seconds into line i where the nth `phrase` starts (even speaking rate inside a line)
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
    return min(dur - 0.1, dur * k / len(text))


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def eq_line(parts, size=34, font=PIXEL, buff=0.3):
    return VGroup(*[MT(s, size, c, font) for s, c in parts]).arrange(RIGHT, buff=buff)


def pulse(m, k=1.15):
    # Emphasis that keeps the pixel art's colors (Indicate would paint it one flat color)
    return m.animate(rate_func=there_and_back).scale(k)


def digit_row(num, ore, y, size=0.8, gap=0.12, x=0.0):
    row = VGroup(*[Block(int(c), ore, size) for c in str(num)]).arrange(RIGHT, buff=gap)
    row.move_to([x, y, 0])
    return row


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("REVERSE", width=5.6).move_to([0, 4.85, 0])
    t2 = stone_title("INTEGER", width=5.6).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    xr = digit_row(1463, X_ORE, 1.55)
    arrow = MT("v", 56, MC_YELLOW, PIXEL).move_to([0, 0.65, 0])
    rr = digit_row(3641, R_ORE, -0.25)
    bar = pixel_art("barrier", 0.62).next_to(rr, RIGHT, buff=0.35)
    lim = chat("max 2147483647", MC_RED, 40).move_to([0, -1.45, 0])
    tags = VGroup(chat("LeetCode #7", MC_AQUA, 46), chat("Medium", MC_GOLD, 46), chat("Math", MC_GREEN, 46))
    tags.arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, xr, arrow, rr, bar, lim, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, xr, arrow, rr, bar, lim, tags = art
        self.add(art)

        self.seg(0)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        # The digits hop right to left, then the reversed row answers left to right
        self.sfx("stone_dig1", 0.35, delay=0.3)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.3) for b in reversed(xr)], lag_ratio=0.25), rt=1.2)
        self.sfx("orb", 0.3, delay=0.2)
        self.beat(LaggedStart(*[pulse(b, 1.2) for b in rr], lag_ratio=0.25), rt=1.2)
        self.sfx("villager_no1", 0.3)
        self.beat(pulse(bar, 1.35), pulse(lim, 1.1), rt=0.8)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        xr = digit_row(123, X_ORE, 3.0, size=1.0, gap=0.15)
        arrow = MT("v", 64, MC_YELLOW, PIXEL).move_to([0, 1.9, 0])
        rr = digit_row(321, R_ORE, 0.8, size=1.0, gap=0.15)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        for b in xr:
            b.shift(UP * 8)
        self.add(xr)
        for k in range(3):
            self.sfx(f"stone_dig{k + 1}", 0.32, delay=k * 0.12 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in xr],
                              lag_ratio=0.12), rt=1.2)
        self.until(at(1, "reverse its") - 0.1)
        self.beat(FadeIn(arrow, shift=DOWN * 0.2), rt=0.4)
        self.until(at(1, "three two one") - 0.3)
        self.sfx("pop", 0.35)
        self.beat(LaggedStart(*[FadeIn(b, scale=0.5) for b in rr], lag_ratio=0.3), rt=0.8)
        self.close_seg()

        rng = chat("-2147483648 ... 2147483647", MC_WHITE, 42).move_to([0, -0.9, 0])
        lab = MT("32-bit range", 36, MC_GRAY).next_to(rng, UP, buff=0.15)
        zero = chat("too big? return 0", MC_RED, 52).move_to([0, -2.6, 0])

        self.seg(2)
        self.beat(FadeIn(lab), FadeIn(rng, shift=UP * 0.15), rt=0.5)
        self.until(at(2, "return zero") - 0.3)
        self.sfx("villager_no2", 0.35)
        self.beat(FadeIn(zero, shift=UP * 0.15), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene3_String(Base):
    def construct(self):
        h = hdr("STRING?", MC_RED)
        code = chat("int(str(x)[::-1])", MC_WHITE, 60).move_to([0, 3.2, 0])
        easy = MT("easy to write", 42, MC_GREEN).move_to([0, 2.1, 0])
        big = eq_line([("9646324351", MC_RED), (">", MC_GRAY), ("2147483647", MC_WHITE)], 40, buff=0.3).move_to([0, 0.5, 0])
        need = MT("catch it with no bigger int type", 40, MC_RED).move_to([0, -0.7, 0])

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.sfx("book_flip1", 0.35)
        self.beat(FadeIn(code, shift=UP * 0.2), rt=0.5)
        self.until(at(3, "easy") - 0.2)
        self.beat(FadeIn(easy, shift=UP * 0.1), rt=0.4)
        self.until(at(3, "catching") - 0.3)
        self.beat(FadeIn(big, shift=UP * 0.15), rt=0.5)
        self.until(at(3, "without") - 0.2)
        self.sfx("villager_no1", 0.35)
        self.beat(FadeIn(need, shift=UP * 0.1), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene4_Math(Base):
    def construct(self):
        h = hdr("THE MATH", MC_GOLD)
        xr = digit_row(1463, X_ORE, 3.3, size=0.95, gap=0.15)
        pop = eq_line([("1463 % 10", MC_WHITE), ("=", MC_GRAY), ("3", MC_GOLD)], 44).move_to([0, 1.8, 0])
        cut = eq_line([("1463 // 10", MC_WHITE), ("=", MC_GRAY), ("146", MC_WHITE)], 44).move_to([0, 0.95, 0])

        self.seg(4)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(xr), rt=0.5)
        self.until(at(4, "Mod ten") - 0.1)
        self.sfx("stone_dig2", 0.35)
        self.beat(FadeIn(pop, shift=UP * 0.15), pulse(xr[-1], 1.25), rt=0.5)
        self.until(at(4, "dividing") - 0.1)
        self.beat(FadeIn(cut, shift=UP * 0.15), xr[-1].animate.shift(DOWN * 4.6).scale(0.85), rt=0.6)
        self.close_seg()

        push = eq_line([("rev", MC_GREEN), ("=", MC_GRAY), ("rev * 10 + d", MC_WHITE)], 44).move_to([0, -0.3, 0])
        rev = Block(3, R_ORE, 0.8).move_to([0, -1.35, 0])

        self.seg(5)
        self.until(at(5, "times ten") - 0.2)
        self.beat(FadeIn(push, shift=UP * 0.15), rt=0.5)
        self.until(at(5, "pushes") - 0.2)
        self.sfx("pop", 0.35)
        self.beat(Transform(xr[-1], rev), rt=0.5)
        self.close_seg()

        check = eq_line([("rev", MC_GREEN), (">", MC_RED), ("(LIMIT - d) // 10 ?", MC_WHITE)], 40, buff=0.25).move_to([0, -2.5, 0])
        build = VGroup(pixel_art("barrier", 0.6), chat("Height limit reached", MC_RED, 44)).arrange(RIGHT, buff=0.3)
        build.move_to([0, -3.75, 0])

        self.seg(6)
        self.until(at(6, "check") - 0.2)
        self.beat(FadeIn(check, shift=UP * 0.15), rt=0.5)
        self.until(at(6, "Like the build") - 0.2)
        self.sfx("villager_no3", 0.35)
        self.beat(FadeIn(build, shift=UP * 0.15), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("POP & PUSH", MC_GREEN)
        code = code_panel(CODE, -4.4, max_h=2.9)
        bar = line_bar(code, 2, 2, MC_YELLOW)
        lim = chat("max 2147483647", MC_RED, 36).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)
        st = {"x": None, "rev": None, "chk": None}

        def x_text(x, d=None):
            parts = [("x =", MC_GRAY), (str(x), MC_WHITE)] + ([("d =", MC_GRAY), (str(d), MC_GOLD)] if d is not None else [])
            return eq_line(parts, 40, buff=0.25).move_to([0, -0.4, 0])

        def rev_text(v, color=MC_GREEN):
            return eq_line([("rev =", MC_GRAY), (str(v), color)], 44, buff=0.3).move_to([0, -1.2, 0])

        def chk_text(rev, d, ok):
            bound = (LIMIT - d) // 10
            # The bound is (LIMIT - d) // 10; past it, one more push would overflow
            return eq_line([(str(rev), MC_WHITE), ("≤" if ok else ">", MC_GREEN if ok else MC_RED), (str(bound), MC_WHITE),
                            ("ok" if ok else "!", MC_GREEN if ok else MC_RED)], 32, buff=0.22).move_to([0, -2.0, 0])

        def swap(key, new, rt=0.2):
            anims = [FadeIn(new)]
            if st[key] is not None:
                anims.append(FadeOut(st[key]))
            st[key] = new
            self.beat(*anims, rt=rt)

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("row1_in", "zero", "reset", "row2_in", "growing", "toast", "caught")]
        for k, o in enumerate(RUN1):
            for kind in ("pop", "check", "push"):
                ev.append((seg_time(W["first"], o[kind]), "1" + kind, k))
        for k, o in enumerate(RUN2):
            if o["overflow"]:
                for kind in ("pop", "check", "stop", "zero"):
                    ev.append((seg_time(W["first"], o[kind]), "2" + kind, k))
            else:
                ev.append((seg_time(W["first"], o["push"]), "2fast", k))
        ev.sort(key=lambda e: e[0])

        def move_bar(k0, k1=None, color=MC_YELLOW, rt=0.12):
            self.beat(Transform(bar, line_bar(code, k0, k1, color)), rt=rt)

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(lim), rt=0.35)

        def on(kind, k):
            if kind == "row1_in":
                for i in range(4):
                    self.sfx(f"stone_dig{i + 1}", 0.28, delay=0.12 * i + 0.35)
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.5)
            elif kind == "zero":
                self.beat(FadeIn(bar), rt=0.15)
                swap("x", x_text(W["x1"]))
                swap("rev", rev_text(0))
            elif kind == "1pop":
                o = RUN1[k]
                self.sfx("stone_dig%d" % (k % 4 + 1), 0.38)
                move_bar(5)
                swap("x", x_text(o["x_after"], o["d"]), rt=0.15)
            elif kind == "1check":
                o = RUN1[k]
                move_bar(6, None, MC_GREEN)
                swap("chk", chk_text(o["rev_before"], o["d"], True), rt=0.15)
            elif kind == "1push":
                o = RUN1[k]
                self.sfx("pop", 0.35)
                move_bar(8, None, MC_GREEN)
                swap("rev", rev_text(o["rev_after"]), rt=0.15)
            elif kind == "reset":
                self.sfx("stone_dig3", 0.3)
                for key in ("chk",):
                    if st[key] is not None:
                        self.beat(FadeOut(st[key]), rt=0.15)
                        st[key] = None
                move_bar(2, rt=0.15)
            elif kind == "row2_in":
                for i in range(0, 10, 2):
                    self.sfx(f"stone_dig{i % 4 + 1}", 0.26, delay=0.3 * i + 0.3)
                swap("x", x_text(W["x2"]), rt=0.25)
                swap("rev", rev_text(0), rt=0.2)
            elif kind == "2fast":
                o = RUN2[k]
                self.sfx("pop", 0.28)
                self.beat(Transform(bar, line_bar(code, 8, 8, MC_GREEN)), rt=0.08)
                swap("x", x_text(o["x_after"], o["d"]), rt=0.1)
                swap("rev", rev_text(o["rev_after"]), rt=0.1)
            elif kind == "growing":
                self.beat(pulse(st["rev"], 1.1), rt=0.3)
            elif kind == "2pop":
                o = RUN2[k]
                self.sfx("stone_dig1", 0.38)
                move_bar(5)
                swap("x", x_text(o["x_after"], o["d"]), rt=0.2)
            elif kind == "2check":
                o = RUN2[k]
                self.sfx("villager_no2", 0.4)
                move_bar(6, None, MC_RED, rt=0.15)
                swap("chk", chk_text(o["rev_before"], o["d"], False), rt=0.25)
            elif kind == "2stop":
                move_bar(7, None, MC_RED, rt=0.2)
            elif kind == "2zero":
                swap("rev", chat("return 0", MC_GREEN, 56).move_to([0, -1.2, 0]), rt=0.3)
            elif kind == "toast":
                t = toast("Advancement Made!", "Overflow caught", w=4.6)
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(lim), rt=0.5)
            elif kind == "caught":
                self.beat(pulse(st["chk"], 1.08), rt=0.4)

        def on_last():
            # The rows leave the 3D clip when the walk ends; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        xr = digit_row(WALK["x2"], X_ORE, 3.5, size=0.7, gap=0.1)
        cnt = MT("10 digits = log10(x) + 1", 40, MC_WHITE).move_to([0, 2.5, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(log x)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, 1.2, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.25, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(14)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(xr), rt=0.5)
        self.until(at(14, "removes") - 0.3)
        # One step per digit, right to left
        self.sfx("stone_dig1", 0.25)
        self.beat(LaggedStart(*[pulse(b, 1.2) for b in reversed(xr)], lag_ratio=0.2), rt=1.4)
        self.until(at(14, "number of digits") - 0.2)
        self.beat(FadeIn(cnt, shift=UP * 0.15), rt=0.4)
        self.until(at(14, "log of x") - 0.4)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.35)
        self.add(xp)
        self.sfx("orb", 0.25)
        self.sfx("levelup", 0.3, delay=0.4)
        self.beat(Restore(xp), rt=0.5)
        self.close_seg()

        ptrs = VGroup(*[chat(s, MC_WHITE, 46) for s in ("x", "d", "rev")]).arrange(RIGHT, buff=0.3).move_to([0, -1.4, 0])
        sp = VGroup(MT("space", 56, MC_GRAY), level_text("O(1)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, -2.8, 0])

        self.seg(15)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(*[FadeIn(p, scale=0.6) for p in ptrs], lag_ratio=0.2), rt=0.6)
        self.until(at(15, "constant") - 0.4)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.6, width=8.4)
        bar = line_bar(code, 5, 5, MC_YELLOW)

        self.seg(16)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(at(16, "push") - 0.1)
        self.beat(Transform(bar, line_bar(code, 8, 8, MC_GREEN)), rt=0.35)
        self.until(at(16, "check") - 0.1)
        self.beat(Transform(bar, line_bar(code, 6, 7, MC_RED)), rt=0.35)
        self.close_seg()

        self.seg(17)
        msg = chat("Check before you push", MC_GOLD, 58)
        msg.move_to([0, -2.3, 0])
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.4)
        self.until(1.6)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.45)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.9)
        self.close_seg()
