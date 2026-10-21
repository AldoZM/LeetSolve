WALK = json.load(open('walk.json', encoding='utf-8'))
SYMS, VALS = WALK["syms"], WALK["vals"]
ORE_OF.update(dict(zip(SYMS, WALK["ores"])))
ISO_SIDE, ISO_FILL = 0.61, 0.88

ADD_CODE = """def romanToInt(s):
    val = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
           'C': 100, 'D': 500, 'M': 1000}
    return sum(val[ch] for ch in s)"""

CODE = """def romanToInt(s):
    val = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
           'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for i, ch in enumerate(s):
        if i + 1 < len(s) and val[ch] < val[s[i + 1]]:
            total -= val[ch]
        else:
            total += val[ch]
    return total"""


def value_row(row, size=26, color=MC_GRAY, buff=0.14):
    return VGroup(*[MT(str(v), size, color).next_to(b, DOWN, buff=buff) for v, b in zip(VALS, row)])


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def eq_line(parts, size=34, font=PIXEL, buff=0.3):
    return VGroup(*[MT(s, size, c, font) for s, c in parts]).arrange(RIGHT, buff=buff)


def pulse(m, k=1.15):
    # Emphasis that keeps the pixel art's colors (Indicate would paint it one flat color)
    return m.animate(rate_func=there_and_back).scale(k)


def signed(k):
    v = VALS[k]
    sub = k + 1 < len(VALS) and v < VALS[k + 1]
    return (f"-{v}", MC_RED) if sub else (f"+{v}", MC_GREEN)


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("ROMAN", width=5.0).move_to([0, 4.85, 0])
    t2 = stone_title("TO INTEGER", width=7.6).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.45, 2.75, 0])
    row = block_row(SYMS, 1.15, size=0.95, gap=0.18)
    vals = value_row(row)
    eq = VGroup(MT("=", 60, MC_GRAY, PIXEL), level_text("1994", 0.9)).arrange(RIGHT, buff=0.35)
    eq.move_to([0, -1.25, 0])
    tags = VGroup(chat("LeetCode #13", MC_AQUA, 46), chat("Easy", MC_GREEN, 46), chat("Math", MC_GOLD, 46))
    tags.arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, row, vals, eq, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, row, vals, eq, tags = art
        self.add(art)

        self.seg(0)
        self.beat(pulse(spl), rt=0.8)
        self.sfx("stone_dig1", 0.35, delay=0.35)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.35) for b in row], lag_ratio=0.18), rt=1.6)
        self.sfx("orb", 0.3, delay=0.3)
        self.beat(pulse(eq, 1.12), *[ShowPassingFlash(outline(row[k], MC_GOLD, 10), time_width=0.6) for k in (1, 3, 5)], rt=0.9)
        self.beat(pulse(spl), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        row = block_row(SYMS, 1.9, size=0.95, gap=0.18)
        vals = value_row(row, 30)
        lab = MT("s", 44, MC_WHITE).next_to(row, UP, buff=0.2).align_to(row, LEFT)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(len(row)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.3, delay=k * 0.12 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.12), rt=1.7)
        self.beat(FadeIn(lab), rt=0.3)
        self.until(2.6)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(*[FadeIn(v, shift=UP * 0.1) for v in vals], lag_ratio=0.12), rt=0.9)
        self.close_seg()

        self.seg(2)
        roman = chat("MCMXCIV", MC_WHITE, 60).move_to([0, -0.6, 0])
        arrow = MT("->", 60, MC_GRAY).next_to(roman, DOWN, buff=0.3)
        num = level_text("1994", 0.95).next_to(arrow, DOWN, buff=0.35)
        self.until(1.0)
        self.beat(FadeIn(roman, shift=UP * 0.2), rt=0.5)
        self.until(3.0)
        self.beat(FadeIn(arrow), rt=0.3)
        self.until(4.0)
        self.sfx("levelup", 0.3)
        self.beat(FadeIn(num, scale=0.6), rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene3_AddAll(Base):
    def construct(self):
        h = hdr("ADD EVERYTHING", MC_RED)
        row = block_row(SYMS, 3.0, size=0.9, gap=0.18)
        vals = value_row(row, 26)
        code = code_panel(ADD_CODE, -3.7, max_h=2.9)

        def total_at(k):
            m = MT(f"sum {sum(VALS[:k])}", 46, MC_WHITE, PIXEL)
            m.move_to([0, 0.6, 0])
            return m

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in row], lag_ratio=0.1),
                  rt=0.9)
        self.beat(FadeIn(vals), rt=0.3)
        self.until(1.6)
        self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
        self.close_seg()

        bar = line_bar(code, 3, 3, MC_YELLOW)
        cur = outline(row[0], MC_YELLOW, 7)
        tot = total_at(0)
        self.seg(4)
        self.beat(FadeIn(bar), Create(cur), FadeIn(tot), rt=0.35)
        step = max(0.3, (DUR[4] - 0.8) / len(SYMS))
        for k in range(len(SYMS)):
            self.sfx("orb", 0.22)
            self.beat(cur.animate.move_to(row[k]), Transform(tot, total_at(k + 1)), pulse(row[k], 1.12), rt=min(step, 0.45))
        self.close_seg()

        self.seg(5)
        wrong = MT("2216", 72, MC_RED, PIXEL).move_to([0, 0.6, 0])
        self.sfx("villager_no1", 0.4)
        self.beat(FadeOut(cur), FadeOut(tot), FadeIn(wrong, scale=1.4), Transform(bar, line_bar(code, 3, 3, MC_RED)), rt=0.5)
        should = MT("should be 1994", 40, MC_GRAY).next_to(wrong, DOWN, buff=0.3)
        self.until(min(2.4, DUR[5] - 0.8))
        self.beat(FadeIn(should, shift=UP * 0.1), Wiggle(wrong), rt=0.7)
        self.close_seg()

        self.seg(6)
        self.beat(FadeOut(wrong), FadeOut(should), rt=0.3)
        pair = VGroup(outline(row[1], MC_GOLD, 8), outline(row[2], MC_GOLD, 8))
        self.until(1.6)
        self.beat(Create(pair), rt=0.4)
        cm = eq_line([("CM", MC_GOLD), ("=", MC_GRAY), ("1000", MC_WHITE), ("-", MC_RED), ("100", MC_WHITE), ("=", MC_GRAY),
                      ("900", MC_GREEN)], 32, buff=0.22)
        cm.move_to([0, 0.75, 0])
        self.beat(FadeIn(cm, shift=UP * 0.15), rt=0.5)
        not11 = MT("not 1100", 40, MC_RED).next_to(cm, DOWN, buff=0.3)
        self.until(DUR[6] - 1.3)
        self.beat(FadeIn(not11), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        pair = block_row(["C", "M"], 2.6, size=1.5, gap=1.4)
        vc = MT("100", 36, MC_GRAY).next_to(pair[0], DOWN, buff=0.15)
        vm = MT("1000", 36, MC_GRAY).next_to(pair[1], DOWN, buff=0.15)
        cur = outline(pair[0], MC_YELLOW, 8)
        peek = outline(pair[1], MC_AQUA, 8)
        lt = MT("<", 70, MC_AQUA, PIXEL).move_to(pair)
        rule1 = eq_line([("next bigger", MC_AQUA), ("->", MC_GRAY), ("subtract", MC_RED)], 46, TERM, 0.3).move_to([0, 0.2, 0])
        rule2 = eq_line([("otherwise", MC_WHITE), ("->", MC_GRAY), ("add", MC_GREEN)], 46, TERM, 0.3).move_to([0, -0.9, 0])
        minus = MT("-100", 46, MC_RED, PIXEL).next_to(vc, DOWN, buff=0.25)

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(pair, shift=DOWN * 0.3), FadeIn(vc), FadeIn(vm), rt=0.6)
        self.until(1.4)
        self.beat(Create(cur), rt=0.3)
        self.until(2.4)
        self.sfx("click", 0.35)
        self.beat(Create(peek), FadeIn(lt, scale=0.5), rt=0.4)
        self.until(min(4.4, DUR[7] - 1.5))
        self.sfx("pop", 0.35)
        self.beat(FadeIn(rule1, shift=UP * 0.15), FadeIn(minus, shift=DOWN * 0.1), rt=0.5)
        self.close_seg()

        self.seg(8)
        self.until(0.2)
        self.beat(FadeIn(rule2, shift=UP * 0.15), rt=0.5)
        one = MT("1 comparison per block", 44, MC_GOLD).move_to([0, -2.6, 0])
        self.until(min(2.0, DUR[8] - 1.0))
        self.beat(FadeIn(one, shift=UP * 0.15), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("ONE PASS", MC_GREEN)
        word = chat("MCMXCIV", MC_WHITE, 40).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)
        code = code_panel(CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 4, 4, MC_YELLOW)
        bg, fill = xp_bar(7.4)
        bg.move_to([0, -1.55, 0])
        st = {"lvl": level_text("0", 0.8).move_to([0, -0.95, 0]), "xp": fill(0.001)}
        # The sum as it is written: each term takes its final place when its verdict comes
        terms = VGroup(*[MT(signed(k)[0], 30, signed(k)[1], PIXEL) for k in range(len(SYMS))])
        terms.arrange(RIGHT, buff=0.18).move_to([0, -2.15, 0])

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("intro_row", "xp_in", "hundred", "toast", "answer")]
        for k, s in enumerate(W["steps"]):
            for kind in ("visit", "peek", "verdict"):
                ev.append((seg_time(W["first"], s[kind]), kind, k))
        ev.sort(key=lambda e: e[0])

        def move_bar(line, color=MC_YELLOW, rt=0.15):
            self.beat(Transform(bar, line_bar(code, line, line, color)), rt=rt)

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(word), rt=0.35)

        def on(kind, k):
            if kind == "intro_row":
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
            elif kind == "xp_in":
                self.sfx("orb", 0.25)
                self.beat(FadeIn(bg), FadeIn(st["lvl"], shift=UP * 0.1), Transform(bar, line_bar(code, 3, 3, MC_YELLOW)), rt=0.4)
                self.add(st["xp"])
            elif kind == "visit":
                move_bar(4)
            elif kind == "peek":
                self.sfx("click", 0.3)
                move_bar(5, MC_AQUA)
            elif kind == "verdict":
                s = W["steps"][k]
                col = signed(k)[1]
                lvl = level_text(str(s["total"]), 0.8).move_to(st["lvl"])
                xp = fill(max(s["total"], 2) / 1994)
                if s["sub"]:
                    self.sfx("stone_dig2", 0.32)
                else:
                    for d in (0.0, 0.15):
                        self.sfx("orb", 0.26, delay=d)
                self.beat(Transform(bar, line_bar(code, 6 if s["sub"] else 8, 6 if s["sub"] else 8, col)),
                          Transform(st["lvl"], lvl), Transform(st["xp"], xp), FadeIn(terms[k], shift=UP * 0.15), rt=0.25)
            elif kind == "hundred":
                self.beat(pulse(st["lvl"], 1.25), rt=0.5)
            elif kind == "toast":
                t = toast("Advancement Made!", "Roman to Integer", w=4.6)
                t.move_to([0, 5.5, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                self.sfx("levelup", 0.25, delay=0.3)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(word), Transform(bar, line_bar(code, 9, 9, MC_GREEN)), rt=0.5)
            elif kind == "answer":
                ans = chat("return 1994", MC_GREEN, 60)
                ans.move_to([0, 4.3, 0])
                self.beat(FadeIn(ans, shift=UP * 0.2), rt=0.4)

        def on_last():
            # The 3D clip fades to sky at its end; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        look = VGroup(MT("1 look", 52, MC_WHITE), MT("per symbol", 52, MC_GRAY)).arrange(RIGHT, buff=0.3)
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
        self.until(0.5)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in look], lag_ratio=0.25), rt=0.7)
        self.until(min(2.6, DUR[16] - 1.8))
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.4)
        self.add(xp)
        for d in (0.0, 0.3, 0.6, 0.9):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=1.2)
        self.beat(Restore(xp), rt=1.2)
        self.close_seg()

        self.seg(17)
        mem = VGroup(MT("memory", 56, MC_GRAY), MT("O(1)", 52, MC_GOLD, PIXEL)).arrange(RIGHT, buff=0.4)
        mem.move_to([0, -1.4, 0])
        one = MT("just the total", 44, MC_WHITE).next_to(mem, DOWN, buff=0.35)
        self.until(0.3)
        self.beat(FadeIn(mem, shift=UP * 0.15), rt=0.5)
        self.until(min(2.0, DUR[17] - 1.0))
        self.beat(FadeIn(one, shift=UP * 0.1), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.6, width=8.4)
        bar = line_bar(code, 4, 4, MC_YELLOW)

        self.seg(18)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(min(1.6, DUR[18] - 1.6))
        self.beat(Transform(bar, line_bar(code, 5, 5, MC_AQUA)), rt=0.35)
        self.until(DUR[18] - 0.9)
        self.beat(Transform(bar, line_bar(code, 1, 2, MC_GOLD)), rt=0.35)
        self.close_seg()

        self.seg(19)
        msg = VGroup(chat("Smaller before bigger", MC_GOLD, 54), chat("means subtract", MC_RED, 54)).arrange(DOWN, buff=0.2)
        msg.move_to([0, -2.6, 0])
        self.until(0.1)
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.5)
        self.until(DUR[19] - 1.9)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.5)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=1.0)
        self.close_seg()
