WALK = json.load(open('walk.json', encoding='utf-8'))
STEPS = WALK["steps"]
X_ORE, H_ORE, NEG_ORE = "iron_ore", "gold_ore", "redstone_ore"

CODE = """def isPalindrome(x):
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    half = 0
    while x > half:
        half = half * 10 + x % 10
        x //= 10
    return x == half or x == half // 10"""


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


def sign_row(chars, y, size=0.9, gap=0.12):
    # Characters of a number written out: the minus sign on redstone, digits on iron
    row = VGroup(*[Block(c, NEG_ORE if c == "-" else X_ORE, size) for c in chars]).arrange(RIGHT, buff=gap)
    row.move_to([0, y, 0])
    return row


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("PALINDROME", width=7.6).move_to([0, 4.85, 0])
    t2 = stone_title("NUMBER", width=7.6)
    t2.scale_to_fit_height(t1.height)
    t2.move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    xr = digit_row(WALK["x"], X_ORE, 1.55)
    arrow = MT("v", 56, MC_YELLOW, PIXEL).move_to([0, 0.65, 0])
    left = digit_row(12, X_ORE, 0)
    right = digit_row(12, H_ORE, 0)
    eq = MT("=", 48, MC_GREEN, PIXEL)
    halves = VGroup(left, eq, right).arrange(RIGHT, buff=0.35)
    halves.move_to([0, -0.25, 0])
    yes = chat("palindrome!", MC_GREEN, 40).move_to([0, -1.45, 0])
    tags = VGroup(chat("LeetCode #9", MC_AQUA, 46), chat("Easy", MC_GREEN, 46), chat("Math", MC_GOLD, 46))
    tags.arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, xr, arrow, halves, yes, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, xr, arrow, halves, yes, tags = art
        self.add(art)

        self.seg(0)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        # Mirror pairs hop together: the outer ones, then the inner ones, then the middle
        self.sfx("stone_dig1", 0.35, delay=0.1)
        self.sfx("stone_dig2", 0.32, delay=0.5)
        self.sfx("stone_dig3", 0.3, delay=0.9)
        self.beat(LaggedStart(*[AnimationGroup(*[xr[i].animate(rate_func=there_and_back).shift(UP * 0.3) for i in pair])
                                for pair in ((0, 4), (1, 3), (2,))], lag_ratio=0.4), rt=1.3)
        self.sfx("orb", 0.3, delay=0.2)
        self.beat(pulse(halves[0], 1.15), pulse(halves[2], 1.15), rt=0.8)
        self.beat(pulse(yes, 1.12), rt=0.7)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        row = digit_row(121, X_ORE, 3.25, size=1.0, gap=0.15)
        fw = eq_line([("forward", MC_GRAY), ("1 2 1", MC_WHITE)], 34).move_to([0, 2.0, 0])
        bw = eq_line([("backward", MC_GRAY), ("1 2 1", MC_WHITE)], 34).move_to([0, 1.35, 0])
        fw.shift(RIGHT * (bw[1].get_center()[0] - fw[1].get_center()[0]) / 2)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(3):
            self.sfx(f"stone_dig{k + 1}", 0.32, delay=k * 0.12 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.12), rt=1.2)
        self.until(at(1, "forward") - 0.1)
        self.beat(FadeIn(fw, shift=RIGHT * 0.2), rt=0.4)
        self.until(at(1, "backward") - 0.1)
        self.beat(FadeIn(bw, shift=LEFT * 0.2), rt=0.4)
        self.close_seg()

        yes = chat("true", MC_GREEN, 48).move_to([0, 0.35, 0])
        neg = sign_row("-121", -1.0)
        arrow = MT("v", 44, MC_YELLOW, PIXEL).move_to([0, -1.9, 0])
        rev = sign_row("121-", -2.8)
        no = chat("false", MC_RED, 48).move_to([0, -4.0, 0])

        self.seg(2)
        self.until(at(2, "is a palindrome") - 0.2)
        self.sfx("orb", 0.3)
        self.beat(FadeIn(yes, shift=UP * 0.15), rt=0.4)
        self.until(at(2, "Minus") - 0.1)
        self.sfx("stone_dig4", 0.32)
        self.beat(FadeIn(neg, shift=DOWN * 0.2), rt=0.5)
        self.until(at(2, "is not") - 0.2)
        self.sfx("villager_no1", 0.35)
        self.beat(FadeIn(arrow, shift=DOWN * 0.15), FadeIn(rev, shift=DOWN * 0.2), FadeIn(no, shift=UP * 0.15), rt=0.5)
        self.until(at(2, "minus sign") - 0.1)
        self.beat(pulse(neg[0], 1.25), pulse(rev[-1], 1.25), rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene3_String(Base):
    def construct(self):
        h = hdr("STRING?", MC_RED)
        s1 = chat("s = str(x)", MC_WHITE, 56).move_to([0, 3.5, 0])
        s2 = chat("s == s[::-1]", MC_WHITE, 56).move_to([0, 2.45, 0])
        easy = MT("easy to write", 42, MC_GREEN).move_to([0, 1.5, 0])

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(at(3, "turn the number") - 0.1)
        self.sfx("book_flip1", 0.35)
        self.beat(FadeIn(s1, shift=UP * 0.2), rt=0.5)
        self.until(at(3, "compare") - 0.1)
        self.sfx("book_flip2", 0.3)
        self.beat(FadeIn(s2, shift=UP * 0.2), rt=0.5)
        self.until(at(3, "reverse") - 0.2)
        self.beat(FadeIn(easy, shift=UP * 0.1), rt=0.4)
        self.close_seg()

        book = pixel_art("writable_book", 0.7)
        fu = chat("Follow up: no strings!", MC_GOLD, 44)
        follow = VGroup(book, fu).arrange(RIGHT, buff=0.25).move_to([0, 0.35, 0])
        strike = VGroup(*[Line(m.get_left() + LEFT * 0.1, m.get_right() + RIGHT * 0.1, stroke_color=MC_RED, stroke_width=8)
                          for m in (s1, s2)])

        self.seg(4)
        self.until(at(4, "It works") + 0.1)
        self.beat(pulse(easy, 1.1), rt=0.5)
        self.until(at(4, "follow up") - 0.1)
        self.sfx("book_put", 0.35)
        self.beat(FadeIn(follow, shift=UP * 0.15), rt=0.5)
        self.until(at(4, "without converting") - 0.1)
        self.sfx("villager_no2", 0.35)
        self.beat(Create(strike[0]), Create(strike[1]), FadeOut(easy), rt=0.5)
        self.close_seg()

        whole = eq_line([("1999999999", MC_WHITE), ("->", MC_GRAY), ("9999999991", MC_GOLD)], 30, buff=0.25)
        whole.move_to([0, -1.05, 0])
        lab = MT("reverse the whole number", 38, MC_GRAY).move_to([0, -0.3, 0])
        big = eq_line([("9999999991", MC_RED), (">", MC_GRAY), ("2147483647", MC_WHITE)], 30, buff=0.25).move_to([0, -2.0, 0])
        ovf = chat("overflow!", MC_RED, 52).move_to([0, -3.2, 0])

        self.seg(5)
        self.until(at(5, "reverse the whole") - 0.2)
        self.beat(FadeIn(lab, shift=UP * 0.1), rt=0.4)
        self.sfx("stone_dig1", 0.3)
        self.beat(FadeIn(whole, shift=UP * 0.15), rt=0.5)
        self.until(at(5, "could overflow") - 0.4)
        self.beat(FadeIn(big, shift=UP * 0.15), rt=0.4)
        self.sfx("villager_no3", 0.35)
        self.beat(FadeIn(ovf, shift=UP * 0.15), rt=0.35)
        self.clear_all(rt=0.4)
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        xr = digit_row(WALK["x"], X_ORE, 3.4, size=0.95, gap=0.15)
        box = SurroundingRectangle(VGroup(xr[3], xr[4]), color=MC_GOLD, buff=0.1, stroke_width=6, corner_radius=0)
        lab = MT("half", 40, MC_GOLD).next_to(box, DOWN, buff=0.15)

        self.seg(6)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(xr), rt=0.5)
        self.until(at(6, "only half") - 0.1)
        self.sfx("pop", 0.32)
        self.beat(Create(box), FadeIn(lab, shift=UP * 0.1), rt=0.6)
        self.close_seg()

        hlab = MT("half", 40, MC_GOLD).move_to([-1.6, 1.15, 0])
        first = Block(1, H_ORE, 0.95).move_to([-0.4, 1.15, 0])
        push = eq_line([("half", MC_GOLD), ("=", MC_GRAY), ("half * 10 + x % 10", MC_WHITE)], 30, buff=0.25)
        push.move_to([0, -0.1, 0])
        until = eq_line([("until", MC_GRAY), ("half", MC_GOLD), (">=", MC_GRAY), ("x", MC_WHITE)], 34, buff=0.3)
        until.move_to([0, -1.0, 0])

        self.seg(7)
        self.until(at(7, "Pop digits") - 0.1)
        self.beat(FadeOut(box), FadeOut(lab), pulse(xr[4], 1.25), rt=0.5)
        self.until(at(7, "push them") - 0.3)
        self.sfx("stone_dig2", 0.35)
        self.beat(FadeIn(hlab), Transform(xr[4], first, path_arc=0.8), rt=0.7)
        self.sfx("pop", 0.3)
        self.beat(FadeIn(push, shift=UP * 0.15), rt=0.45)
        self.until(at(7, "until that number") - 0.1)
        self.beat(FadeIn(until, shift=UP * 0.15), rt=0.45)
        self.until(at(7, "catches up") + 0.1)
        self.beat(pulse(until, 1.1), rt=0.5)
        self.close_seg()

        match = eq_line([("x", MC_WHITE), ("==", MC_GREEN), ("half", MC_GOLD), ("?", MC_GREEN)], 44, buff=0.3)
        match.move_to([0, -2.3, 0])

        self.seg(8)
        self.until(at(8, "halves") - 0.3)
        self.sfx("orb", 0.3)
        self.beat(FadeIn(match, shift=UP * 0.15), rt=0.4)
        self.clear_all(rt=0.4)
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("HALF FOLD", MC_GREEN)
        code = code_panel(CODE, -4.4, max_h=2.9)
        bar = line_bar(code, 3, 3, MC_YELLOW)
        xl = chat("x = %d" % W["x"], MC_WHITE, 36).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)
        st = {"x": None, "half": None, "chk": None}

        def x_text(x):
            return eq_line([("x =", MC_GRAY), (str(x), MC_WHITE)], 40, buff=0.3).move_to([0, -0.45, 0])

        def half_text(parts, size=40):
            return eq_line([("half =", MC_GRAY)] + parts, size, buff=0.3).move_to([0, -1.2, 0])

        def chk_text(parts):
            return eq_line(parts, 36, buff=0.25).move_to([0, -2.0, 0])

        def swap(key, new, rt=0.2):
            anims = [FadeIn(new)]
            if st[key] is not None:
                anims.append(FadeOut(st[key]))
            st[key] = new
            self.beat(*anims, rt=rt)

        def move_bar(k0, k1=None, color=MC_YELLOW, rt=0.12):
            self.beat(Transform(bar, line_bar(code, k0, k1, color)), rt=rt)

        ev = [(seg_time(W["first"], W[key]), key, None)
              for key in ("row_in", "zero", "stop", "stop_t", "odd", "middle", "drop", "equal", "toast")]
        for k, s in enumerate(STEPS):
            for kind in ("pop", "x_t", "half_t"):
                ev.append((seg_time(W["first"], s[kind]), kind, k))
        ev.sort(key=lambda e: e[0])

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(xl), rt=0.35)

        def on(kind, k):
            if kind == "row_in":
                for i in range(5):
                    self.sfx(f"stone_dig{i % 4 + 1}", 0.28, delay=0.15 * i + 0.3)
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.5)
            elif kind == "zero":
                self.beat(FadeIn(bar), rt=0.15)
                swap("x", x_text(W["x"]))
                swap("half", half_text([("0", MC_GOLD)]))
            elif kind == "pop":
                s = STEPS[k]
                self.sfx("stone_dig%d" % (k % 4 + 1), 0.38)
                move_bar(4, None, MC_GREEN)
                swap("chk", chk_text([(str(s["x_before"]), MC_WHITE), (">", MC_GREEN), (str(s["half_before"]), MC_GOLD),
                                      ("loop", MC_GREEN)]), rt=0.15)
            elif kind == "x_t":
                s = STEPS[k]
                move_bar(5, 6)
                swap("x", x_text(s["x_after"]), rt=0.15)
            elif kind == "half_t":
                s = STEPS[k]
                self.sfx("pop", 0.35)
                swap("half", half_text([(str(s["half_after"]), MC_GOLD)]), rt=0.15)
            elif kind == "stop":
                self.sfx("villager_no2", 0.38)
                move_bar(4, None, MC_RED, rt=0.15)
                swap("chk", chk_text([(str(W["x_end"]), MC_WHITE), (">", MC_RED), (str(W["half_end"]), MC_GOLD),
                                      ("no", MC_RED)]), rt=0.2)
            elif kind == "stop_t":
                self.beat(pulse(st["chk"], 1.1), rt=0.35)
            elif kind == "odd":
                move_bar(7, None, MC_YELLOW, rt=0.15)
                swap("chk", chk_text([("5 digits:", MC_GRAY), ("odd", MC_GOLD)]), rt=0.2)
            elif kind == "middle":
                self.beat(pulse(st["half"], 1.12), rt=0.4)
            elif kind == "drop":
                self.sfx("stone_dig3", 0.36)
                swap("half", half_text([("123 // 10", MC_WHITE), ("=", MC_GRAY), ("12", MC_GOLD)], 34), rt=0.25)
            elif kind == "equal":
                self.sfx("orb", 0.3)
                move_bar(7, None, MC_GREEN, rt=0.15)
                swap("chk", chk_text([("12", MC_WHITE), ("==", MC_GREEN), ("12", MC_GOLD), ("true", MC_GREEN)]), rt=0.2)
            elif kind == "toast":
                t = toast("Advancement Made!", "Palindrome Number", w=4.6)
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                ans = chat("return True", MC_GREEN, 52).move_to([0, -0.85, 0])
                self.beat(t.animate.shift(LEFT * 7), FadeOut(xl), FadeOut(st["x"]), FadeOut(st["half"]),
                          FadeIn(ans, shift=UP * 0.15), rt=0.5)

        def on_last():
            # The rows leave the 3D clip when the walk ends; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        xr = digit_row(WALK["x"], X_ORE, 3.5, size=0.85, gap=0.12)
        cnt = MT("3 pops for 5 digits", 40, MC_WHITE).move_to([0, 2.45, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(log x)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, 1.2, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.25, 0])
        xp = fill(0.5)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(15)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(xr), rt=0.5)
        self.until(at(15, "half of the digits") - 0.2)
        # Only the right half is popped
        self.sfx("stone_dig1", 0.25)
        self.beat(LaggedStart(*[pulse(b, 1.2) for b in reversed(xr[2:])], lag_ratio=0.25), rt=0.8)
        self.beat(FadeIn(cnt, shift=UP * 0.15), rt=0.35)
        self.until(at(15, "log of x") - 0.4)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.35)
        self.add(xp)
        self.sfx("orb", 0.25)
        self.sfx("levelup", 0.3, delay=0.3)
        self.beat(Restore(xp), rt=0.45)
        self.close_seg()

        nos = chat("no str, no list", MC_RED, 44).move_to([0, -1.1, 0])
        nums = VGroup(chat("x", MC_WHITE, 46), chat("half", MC_GOLD, 46)).arrange(RIGHT, buff=0.3).move_to([0, -2.1, 0])
        sp = VGroup(MT("space", 56, MC_GRAY), level_text("O(1)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, -3.4, 0])

        self.seg(16)
        self.sfx("villager_no1", 0.3)
        self.beat(FadeIn(nos, shift=UP * 0.15), rt=0.4)
        self.until(at(16, "just two numbers") - 0.2)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(*[FadeIn(p, scale=0.6) for p in nums], lag_ratio=0.25), rt=0.5)
        self.until(at(16, "Constant") - 0.3)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.4)
        self.clear_all(rt=0.4)
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.6, width=8.4)
        bar = line_bar(code, 1, 2, MC_RED)

        self.seg(17)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.sfx("villager_no3", 0.3)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(at(17, "The rest") - 0.1)
        self.sfx("pop", 0.3)
        self.beat(Transform(bar, line_bar(code, 4, 6, MC_GREEN)), rt=0.35)
        self.close_seg()

        self.seg(18)
        msg = chat("Meet in the middle", MC_GOLD, 58)
        msg.move_to([0, -2.3, 0])
        self.beat(FadeIn(msg, shift=UP * 0.2), Transform(bar, line_bar(code, 7, 7, MC_GOLD)), rt=0.4)
        self.until(1.3)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.4)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.8)
        self.close_seg()
