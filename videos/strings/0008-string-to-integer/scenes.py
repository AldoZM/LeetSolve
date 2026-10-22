WALK = json.load(open('walk.json', encoding='utf-8'))
S, LOOKS, STEPS = WALK["s"], WALK["looks"], WALK["steps"]
RES_ORE = "emerald_ore"

CODE = """def myAtoi(s):
    i, n, sign, res = 0, len(s), 1, 0
    while i < n and s[i] == ' ':
        i += 1
    if i < n and s[i] in '+-':
        sign = -1 if s[i] == '-' else 1
        i += 1
    while i < n and s[i].isdigit():
        d = int(s[i])
        if res > (2**31 - 1 - d) // 10:
            return 2**31 - 1 if sign > 0 else -2**31
        res = res * 10 + d
        i += 1
    return sign * res"""


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


def char_block(c, look, size):
    # A space is a bare stone block; every other character is printed on its block
    b = Block("_" if c == ' ' else c, look, size)
    if c == ' ':
        b.remove(b.num)
    return b


def char_row(y, size=0.9, gap=0.12):
    row = VGroup(*[char_block(c, LOOKS[k], size) for k, c in enumerate(S)]).arrange(RIGHT, buff=gap)
    row.move_to([0, y, 0])
    return row


def digit_row(num, ore, y, size=0.8, gap=0.12):
    row = VGroup(*[Block(c, ore, size) for c in str(num)]).arrange(RIGHT, buff=gap)
    row.move_to([0, y, 0])
    return row


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("STRING TO", width=6.4).move_to([0, 4.85, 0])
    t2 = stone_title("INTEGER", width=5.0).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    row = char_row(1.55, size=0.82, gap=0.1)
    arrow = MT("v", 56, MC_YELLOW, PIXEL).move_to([0, 0.6, 0])
    ans = digit_row(42, RES_ORE, -0.3)
    minus = Block("-", "redstone_ore", 0.8).next_to(ans, LEFT, buff=0.12)
    pick = pickaxe(0.9).move_to([-2.7, -0.3, 0])
    tags = VGroup(chat("LeetCode #8", MC_AQUA, 46), chat("Medium", MC_GOLD, 46), chat("Strings", MC_GREEN, 46))
    tags.arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, row, arrow, VGroup(minus, ans), pick, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, row, arrow, ans, pick, tags = art
        self.add(art)

        self.seg(0)
        self.beat(pulse(spl), rt=0.8)
        # The characters hop left to right, then the parsed number answers
        self.sfx("stone_dig1", 0.35, delay=0.3)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.3) for b in row], lag_ratio=0.2), rt=1.4)
        self.sfx("orb", 0.3, delay=0.2)
        self.beat(LaggedStart(*[pulse(b, 1.2) for b in ans], lag_ratio=0.25), Rotate(pick, angle=-30 * DEGREES, rate_func=there_and_back),
                  rt=1.0)
        self.beat(pulse(spl), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        row = char_row(2.6, size=0.92)
        lab = MT('s = "  -042a7"', 40, MC_WHITE).next_to(row, UP, buff=0.3).align_to(row, LEFT)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(0, len(row), 2):
            self.sfx(f"stone_dig{k // 2 % 4 + 1}", 0.3, delay=k * 0.1 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.1), rt=1.4)
        self.beat(FadeIn(lab), rt=0.3)
        self.until(at(1, "the integer") - 0.2)
        ans = chat("-42", MC_GREEN, 64).move_to([0, 0.9, 0])
        self.sfx("pop", 0.35)
        self.beat(FadeIn(ans, shift=UP * 0.2), rt=0.4)
        self.close_seg()

        # The three phases, each over its part of the string
        spaces, sgn, digs = VGroup(row[0], row[1]), row[2], VGroup(row[3], row[4], row[5])
        p1 = MT("1 skip", 30, MC_GRAY).next_to(spaces, DOWN, buff=0.25)
        p2 = MT("2 sign", 30, MC_RED).next_to(sgn, DOWN, buff=0.25)
        p3 = MT("3 digits", 30, MC_GREEN).next_to(digs, DOWN, buff=0.25)
        stop = outline(row[6], MC_RED, 8)

        self.seg(2)
        self.beat(FadeOut(ans), rt=0.3)
        self.until(at(2, "skip") - 0.2)
        self.beat(FadeIn(p1, shift=UP * 0.1), *[pulse(b) for b in spaces], rt=0.5)
        self.until(at(2, "sign") - 0.3)
        self.sfx("click", 0.3)
        self.beat(FadeIn(p2, shift=UP * 0.1), pulse(sgn, 1.2), rt=0.5)
        self.until(at(2, "read digits") - 0.2)
        self.beat(FadeIn(p3, shift=UP * 0.1), LaggedStart(*[pulse(b) for b in digs], lag_ratio=0.3), rt=0.8)
        self.until(at(2, "not a digit") - 0.2)
        self.sfx("villager_no1", 0.3)
        self.beat(Create(stop), rt=0.4)
        self.close_seg()

        big = chat("-91283472332", MC_RED, 50).move_to([0, -1.2, 0])
        arrow = MT("v", 48, MC_YELLOW, PIXEL).move_to([0, -2.25, 0])
        clamp = chat("-2147483648", MC_GREEN, 50).move_to([0, -3.3, 0])
        lab2 = MT("clamp to the 32-bit range", 34, MC_GRAY).move_to([0, -4.3, 0])

        self.seg(3)
        self.until(at(3, "leaves") - 0.3)
        self.sfx("book_flip1", 0.3)
        self.beat(FadeIn(big, shift=UP * 0.15), rt=0.45)
        self.until(at(3, "clamp") - 0.3)
        self.sfx("stone_dig2", 0.35)
        self.beat(FadeIn(arrow, shift=DOWN * 0.15), FadeIn(clamp, shift=DOWN * 0.15), rt=0.45)
        self.beat(FadeIn(lab2), rt=0.3)
        self.clear_all()
        self.close_seg()


class Scene3_Lazy(Base):
    def construct(self):
        h = hdr("JUST int()?", MC_RED)
        c1 = chat('int("  -042a7")', MC_WHITE, 56).move_to([0, 3.0, 0])
        e1 = MT("ValueError!", 48, MC_RED, PIXEL).move_to([0, 1.85, 0])
        c2 = chat('int("-")', MC_WHITE, 56).move_to([0, 0.2, 0])
        e2 = MT("ValueError!", 48, MC_RED, PIXEL).move_to([0, -0.95, 0])
        pick = pickaxe(1.1).move_to([0, -2.6, 0])

        self.seg(4)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(at(4, "call int") - 0.2)
        self.sfx("book_flip2", 0.35)
        self.beat(FadeIn(c1, shift=UP * 0.2), rt=0.5)
        self.close_seg()

        self.seg(5)
        self.until(at(5, "crash") - 0.4)
        self.sfx("villager_no2", 0.35)
        self.beat(FadeIn(e1, scale=1.3), rt=0.4)
        self.until(at(5, "a lone minus") - 0.2)
        self.beat(FadeIn(c2, shift=UP * 0.2), rt=0.4)
        self.until(at(5, "not a number") - 0.2)
        self.sfx("villager_no3", 0.35)
        self.sfx("break", 0.35, delay=0.4)
        self.beat(FadeIn(e2, scale=1.3), FadeIn(pick), rt=0.4)
        self.beat(Wiggle(pick), rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene4_Machine(Base):
    def construct(self):
        h = hdr("THE MACHINE", MC_GOLD)
        row = char_row(3.3, size=0.82)
        phases = VGroup(chat("SPACES", MC_GRAY, 44), MT("->", 44, MC_GRAY), chat("SIGN", MC_RED, 44), MT("->", 44, MC_GRAY),
                        chat("DIGITS", MC_GREEN, 44)).arrange(RIGHT, buff=0.18).move_to([0, 1.9, 0])
        cursor = outline(row[0], MC_YELLOW, 8)

        self.seg(6)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(row), rt=0.5)
        self.until(at(6, "one character") - 0.3)
        self.beat(Create(cursor), rt=0.3)
        for k in range(1, len(S)):
            self.sfx("stone_step%d" % (k % 6 + 1), 0.22)
            self.beat(cursor.animate.move_to(row[k]), rt=0.16)
        self.until(at(6, "three phases") - 0.2)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in phases], lag_ratio=0.2), FadeOut(cursor), rt=0.8)
        self.close_seg()

        push = eq_line([("res", MC_GREEN), ("=", MC_GRAY), ("res * 10 + d", MC_WHITE)], 44).move_to([0, 0.4, 0])
        res = VGroup(*[Block(c, RES_ORE, 0.8) for c in "42"]).arrange(RIGHT, buff=0.12).move_to([0, -0.75, 0])

        self.seg(7)
        self.until(at(7, "Spaces") - 0.1)
        self.beat(pulse(phases[0]), rt=0.35)
        self.until(at(7, "a sign") - 0.1)
        self.beat(pulse(phases[2]), rt=0.35)
        self.until(at(7, "digits.") - 0.1)
        self.beat(pulse(phases[4]), rt=0.35)
        self.until(at(7, "pushed") - 0.2)
        self.beat(FadeIn(push, shift=UP * 0.15), rt=0.5)
        self.until(at(7, "plus the digit") - 0.2)
        self.sfx("pop", 0.35)
        self.beat(LaggedStart(*[FadeIn(b, scale=0.5) for b in res], lag_ratio=0.3), rt=0.6)
        self.close_seg()

        check = eq_line([("res", MC_GREEN), (">", MC_RED), ("(LIMIT - d) // 10 ?", MC_WHITE)], 38, buff=0.25)
        check.move_to([0, -2.1, 0])
        build = VGroup(pixel_art("barrier", 0.6), chat("Height limit reached", MC_RED, 44)).arrange(RIGHT, buff=0.3)
        build.move_to([0, -3.35, 0])

        self.seg(8)
        self.until(at(8, "we check") - 0.2)
        self.beat(FadeIn(check, shift=UP * 0.15), rt=0.5)
        self.until(at(8, "never overflow") - 0.4)
        self.sfx("villager_no1", 0.3)
        self.beat(FadeIn(build, shift=UP * 0.15), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("READ IT", MC_GREEN)
        code = code_panel(CODE, -3.75, max_h=3.9)
        bar = line_bar(code, 1, 1, MC_YELLOW)
        st = {"i": None, "res": None}

        def i_text(i, ch):
            shown = "' '" if ch == ' ' else f"'{ch}'"
            return eq_line([("i =", MC_GRAY), (str(i), MC_WHITE), ("s[i] =", MC_GRAY), (shown, MC_GOLD)], 34, buff=0.22).move_to([0, -0.45, 0])

        def res_text(sign, res, color=MC_GREEN):
            return eq_line([("sign =", MC_GRAY), (str(sign), MC_RED if sign < 0 else MC_WHITE), ("res =", MC_GRAY), (str(res), color)],
                           34, buff=0.22).move_to([0, -1.15, 0])

        def swap(key, new, rt=0.2):
            anims = [FadeIn(new)]
            if st[key] is not None:
                anims.append(FadeOut(st[key]))
            st[key] = new
            self.beat(*anims, rt=rt)

        def move_bar(k0, k1=None, color=MC_YELLOW, rt=0.15):
            self.beat(Transform(bar, line_bar(code, k0, k1, color)), rt=rt)

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("row_in", "seven", "toast", "apply", "answer_t")]
        for k, s in enumerate(STEPS):
            for kind in ("visit", "skip", "sign_t", "push", "stop_t"):
                if kind in s:
                    ev.append((seg_time(W["first"], s[kind]), kind, k))
        ev.sort(key=lambda e: e[0])
        state = {"sign": 1, "res": 0}

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.35)

        def on(kind, k):
            s = STEPS[k] if k is not None else None
            if kind == "row_in":
                for i in range(0, len(S), 2):
                    self.sfx(f"stone_dig{i // 2 % 4 + 1}", 0.26, delay=0.1 * i + 0.35)
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.5)
                self.beat(FadeIn(bar), rt=0.2)
                swap("res", res_text(1, 0, MC_WHITE))
            elif kind == "visit":
                ch = S[s["i"]]
                line = {"space": 2, "sign": 4, "digit": 7, "stop": 7}[s["kind"]]
                self.sfx("stone_step%d" % (k % 6 + 1), 0.28)
                move_bar(line)
                swap("i", i_text(s["i"], ch), rt=0.15)
            elif kind == "skip":
                move_bar(3, None, MC_GRAY)
            elif kind == "sign_t":
                state["sign"] = s["sign"]
                self.sfx("click", 0.35)
                move_bar(5, None, MC_RED)
                swap("res", res_text(state["sign"], state["res"]), rt=0.2)
            elif kind == "push":
                state["res"] = s["res"]
                self.sfx("pop", 0.35)
                move_bar(8, 11, MC_GREEN)
                swap("res", res_text(state["sign"], state["res"]), rt=0.2)
            elif kind == "stop_t":
                self.sfx("villager_no2", 0.4)
                move_bar(7, None, MC_RED, rt=0.2)
            elif kind == "seven":
                self.beat(pulse(st["i"], 1.06), rt=0.3)
            elif kind == "toast":
                t = toast("Advancement Made!", "String parsed", w=4.6)
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                self.beat(t.animate.shift(LEFT * 7), rt=0.5)
            elif kind == "apply":
                move_bar(13, None, MC_GREEN, rt=0.2)
            elif kind == "answer_t":
                ans = chat("return -42", MC_GREEN, 56).move_to([0, -1.15, 0])
                self.beat(FadeOut(st["res"]), FadeIn(ans, scale=1.2), rt=0.35)
                st["res"] = ans

        def on_last():
            # The rows leave the 3D clip when the walk ends; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        row = char_row(3.5, size=0.8)
        once = MT("each character once", 40, MC_WHITE).move_to([0, 2.45, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, 1.2, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.25, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(15)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(row), rt=0.5)
        self.until(at(15, "each character") - 0.3)
        self.sfx("stone_step1", 0.25)
        self.beat(LaggedStart(*[pulse(b, 1.2) for b in row], lag_ratio=0.2), FadeIn(once, shift=UP * 0.1), rt=1.3)
        self.until(at(15, "linear") - 0.4)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.35)
        self.add(xp)
        self.sfx("orb", 0.25)
        self.sfx("levelup", 0.3, delay=0.4)
        self.beat(Restore(xp), rt=0.6)
        self.close_seg()

        keep = VGroup(*[chat(s, MC_WHITE, 46) for s in ("i", "sign", "res")]).arrange(RIGHT, buff=0.3).move_to([0, -1.4, 0])
        sp = VGroup(MT("space", 56, MC_GRAY), level_text("O(1)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, -2.8, 0])

        self.seg(16)
        self.until(at(16, "an index") - 0.3)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(*[FadeIn(p, scale=0.6) for p in keep], lag_ratio=0.25), rt=0.8)
        self.until(at(16, "Constant") - 0.3)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.6, width=8.4, max_h=6.2)
        bar = line_bar(code, 2, 3, MC_GRAY)

        self.seg(17)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.06), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(at(17, "read the sign") - 0.1)
        self.beat(Transform(bar, line_bar(code, 4, 6, MC_RED)), rt=0.3)
        self.until(at(17, "push digits") - 0.1)
        self.beat(Transform(bar, line_bar(code, 7, 12, MC_GREEN)), rt=0.3)
        self.until(at(17, "check the limit") - 0.1)
        self.beat(Transform(bar, line_bar(code, 9, 10, MC_GOLD)), rt=0.3)
        self.close_seg()

        self.seg(18)
        msg = chat("One phase at a time", MC_GOLD, 58)
        msg.move_to([0, -3.2, 0])
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.4)
        self.until(1.3)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.45)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.9)
        self.close_seg()
