WALK = json.load(open('walk.json', encoding='utf-8'))
NUMS, BITS, ANSWER = WALK["nums"], WALK["bits"], WALK["answer"]
ORE_OF.update(dict(zip(NUMS, WALK["ores"])))
MISPLACED = [i for i, x in enumerate(NUMS) if x != i]

BRUTE_CODE = """def maxK(nums):
    for k in range(len(nums) - 1, 0, -1):
        ok = [(a, b) for a in nums for b in nums
              if a < b and a & b == k]
        if can_sort(nums, ok):
            return k
    return 0"""

AND_CODE = """def maxK(nums):
    ans = -1
    for i, x in enumerate(nums):
        if x != i:
            ans &= x
    return max(ans, 0)"""


def ph(i, phrase, shift=0.0):
    # Seconds into line i where `phrase` starts being spoken (even speaking rate inside a line)
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase)
    return max(0.0, min(dur - 0.25, dur * k / len(text) + shift))


def bits_of(v):
    return [(v >> (BITS - 1 - b)) & 1 for b in range(BITS)]


def bit_str(v):
    return "".join(str(b) for b in bits_of(v))


def lamp(on, w=0.28):
    return pixel_art("redstone_lamp_on" if on else "redstone_lamp", w)


def lamp_bits(v, w=0.28, buff=0.03):
    row = VGroup(*[lamp(b, w) for b in bits_of(v)]).arrange(RIGHT, buff=buff)
    return row


def index_row(row, size=34, color=MC_GRAY, buff=0.14):
    return VGroup(*[MT(str(k), size, color).next_to(b, DOWN, buff=buff) for k, b in enumerate(row)])


def lamp_row(row, idx, w=0.28, buff=0.12):
    # The three bit lamps of each block, under its index
    lamps = VGroup(*[lamp_bits(v, w).next_to(i, DOWN, buff=buff) for v, i in zip(NUMS, idx)])
    for g, b in zip(lamps, row):
        g.set_x(b.get_x())
    return lamps


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def eq_line(parts, size=34, font=PIXEL, buff=0.3):
    return VGroup(*[MT(s, size, c, font) for s, c in parts]).arrange(RIGHT, buff=buff)


def pulse(m, s=1.15):
    # Pixel art is highlighted with a scale pulse; Indicate with a color paints it flat
    return m.animate(rate_func=there_and_back).scale(s)


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    title = stone_title("MAXIMUM K", 60, width=7.8).move_to([0, 4.0, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.25, 2.75, 0])
    row = block_row(NUMS, 1.05, size=0.95, gap=0.18)
    idx = index_row(row, 30)
    lamps = lamp_row(row, idx, 0.27, 0.1)
    pick = pickaxe(1.15).move_to([-1.3, -1.5, 0])
    lit = iso_block("redstone_lamp_on", 1.15).move_to([1.3, -1.5, 0])
    tags = VGroup(chat("LeetCode #3644", MC_AQUA, 46), chat("Medium", MC_GOLD, 46), chat("Bits", MC_RED, 46))
    tags.arrange(RIGHT, buff=0.2)
    if tags.width > 8.4:
        tags.scale_to_fit_width(8.4)
    tags.move_to([0, -3.15, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, title, spl, row, idx, lamps, pick, lit, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, title, spl, row, idx, lamps, pick, lit, tags = art
        self.add(art)

        self.seg(0)
        self.beat(pulse(spl), rt=0.8)
        # Blocks hop one after another, like a wave
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.35) for b in row], lag_ratio=0.18), rt=1.6)
        self.sfx("stone_dig1", 0.35, delay=0.35)
        self.until(ph(0, "LeetCode"))
        self.sfx("click", 0.35)
        self.beat(pulse(lit, 1.2), *[pulse(lamps[k], 1.2) for k in MISPLACED], rt=0.8)
        self.until(ph(0, "and a neat"))
        self.beat(pulse(spl), Rotate(pick, angle=-30 * DEGREES, rate_func=there_and_back), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        row = block_row(NUMS, 2.7, size=0.95, gap=0.18)
        idx = index_row(row, 32)
        lamps = lamp_row(row, idx)
        lab = MT("nums", 40, MC_WHITE).next_to(row, UP, buff=0.2).align_to(row, LEFT)
        w = VGroup(*[MT(str(1 << (BITS - 1 - b)), 24, MC_YELLOW, PIXEL) for b in range(BITS)])
        for t, l in zip(w, lamps[0]):
            t.next_to(l, DOWN, buff=0.1)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        # Blocks fall from the sky and bounce into place
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(len(row)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.3, delay=k * 0.12 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.12), rt=1.6)
        self.beat(FadeIn(idx, shift=UP * 0.1), FadeIn(lab), rt=0.4)
        self.until(ph(1, "all mixed"))
        self.beat(*[Wiggle(row[k]) for k in MISPLACED], rt=0.7)
        self.until(ph(1, "three redstone"))
        self.sfx("click", 0.35)
        self.beat(LaggedStart(*[FadeIn(g, scale=0.6) for g in lamps], lag_ratio=0.1), FadeIn(w), rt=0.9)
        self.close_seg()

        # The rule, with the pair 3 and 5 as an example
        self.seg(2)
        rule = chat("swap a, b  only if  a AND b == k", MC_WHITE, 40)
        rule.move_to([0, -0.15, 0])
        self.until(ph(2, "swap"))
        self.beat(FadeIn(rule, shift=UP * 0.2), rt=0.5)
        a, b = NUMS.index(3), NUMS.index(5)
        frames = VGroup(outline(row[a], MC_YELLOW, 7), outline(row[b], MC_YELLOW, 7))
        ex = VGroup(*[VGroup(MT(s, 34, c, PIXEL), lamp_bits(v, 0.36)).arrange(DOWN, buff=0.15)
                      for s, c, v in (("3", MC_AQUA, 3), ("5", MC_AQUA, 5), ("1", MC_GOLD, 1))])
        ops = [MT("AND", 30, MC_GRAY, PIXEL), MT("=", 30, MC_GRAY, PIXEL)]
        eq = VGroup(ex[0], ops[0], ex[1], ops[1], ex[2]).arrange(RIGHT, buff=0.35)
        eq.move_to([0, -1.9, 0])
        self.until(ph(2, "bitwise AND"))
        self.beat(Create(frames), LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in eq], lag_ratio=0.15), rt=0.9)
        self.until(ph(2, "exactly k"))
        self.sfx("pop", 0.35)
        self.beat(pulse(ex[2]), rt=0.5)
        self.close_seg()

        # With k = 1, two swaps sort the row
        self.seg(3)
        ask = chat("largest k ?", MC_GOLD, 48)
        ask.move_to([0, -3.4, 0])
        self.until(ph(3, "largest"))
        self.beat(FadeIn(ask, shift=UP * 0.2), FadeOut(frames), rt=0.4)
        cols = [VGroup(row[i], lamps[i]) for i in range(len(NUMS))]
        order = list(NUMS)
        self.until(ph(3, "sort the whole"))
        for x, y in ((3, 1), (5, 3)):
            i, j = order.index(x), order.index(y)
            self.sfx("stone_step1", 0.3, delay=0.25)
            self.beat(CyclicReplace(cols[i], cols[j], path_arc=-90 * DEGREES), rt=0.55)
            cols[i], cols[j] = cols[j], cols[i]
            order[i], order[j] = order[j], order[i]
        ans = chat("return 1", MC_GREEN, 60)
        ans.move_to([0, -4.7, 0])
        self.until(ph(3, "the answer"))
        self.sfx("orb", 0.3)
        self.beat(FadeIn(ans, shift=UP * 0.2), Transform(ask, chat("k = 1", MC_GOLD, 48).move_to(ask)), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("BRUTE FORCE", MC_RED)
        row = block_row(NUMS, 3.1, size=0.85, gap=0.16)
        idx = index_row(row, 28)
        code = code_panel(BRUTE_CODE, -3.75, max_h=2.9)
        pick = pickaxe(1.0).move_to([-2.6, 1.15, 0])
        dbg = Rectangle(width=1.2, height=0.16, fill_color="#000000", fill_opacity=1, stroke_width=0)
        dbg.next_to(pick, DOWN, buff=0.15)
        n = len(NUMS)
        pairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
        total = (n - 1) * len(pairs)

        def dfill(frac):
            # Durability bar: shrinks and turns from green to red
            r = Rectangle(width=max(1.16 * frac, 0.02), height=0.1, stroke_width=0, fill_opacity=1,
                          fill_color=interpolate_color(ManimColor(MC_RED), ManimColor(MC_GREEN), frac))
            r.move_to(dbg.get_left() + RIGHT * (0.02 + max(1.16 * frac, 0.02) / 2))
            return r

        # Chat boxes keep the readouts legible over the birch trunks behind
        def counter(c):
            m = chat(f"checks {c}", MC_WHITE, 30, PIXEL)
            m.move_to([1.2, 0.75, 0])
            return m

        def klabel(k):
            m = chat(f"k = {k}", MC_GOLD, 34, PIXEL)
            m.move_to([1.2, 1.6, 0])
            return m

        fill, cnt, kl = dfill(1.0), counter(0), klabel(n - 1)

        self.seg(4)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in row], lag_ratio=0.1), rt=0.9)
        self.beat(FadeIn(idx), rt=0.3)
        self.until(ph(4, "try every"))
        self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
        bar = line_bar(code, 1, 1, MC_YELLOW)
        self.until(ph(4, "from the top"))
        self.beat(FadeIn(bar), FadeIn(kl, shift=DOWN * 0.1), FadeIn(pick, scale=0.6), FadeIn(dbg), FadeIn(fill), FadeIn(cnt), rt=0.5)
        self.close_seg()

        # k = 6: sweep all 21 pairs, then the sort check fails
        self.seg(5)
        oa, ob = outline(row[0], MC_YELLOW, 6), outline(row[1], MC_WHITE, 6)
        self.until(ph(5, "test every"))
        self.beat(Create(oa), Create(ob), Transform(bar, line_bar(code, 2, 3, MC_YELLOW)), rt=0.3)
        span = ph(5, "then check") - ph(5, "test every") - 0.45
        rt = max(2 / 30, math.floor(span / len(pairs) * 30) / 30)
        for c, (a, b) in enumerate(pairs):
            anims = [ob.animate.move_to(row[b]), Transform(cnt, counter(c + 1)),
                     Transform(fill, dfill(1 - (c + 1) / (total + 6)))]
            if c == 0 or pairs[c - 1][0] != a:
                anims.append(oa.animate.move_to(row[a]))
            if c % 3 == 0:
                self.sfx(f"stone_dig{c % 4 + 1}", 0.22)
            self.beat(*anims, rt=rt)
        self.until(ph(5, "then check"))
        self.sfx("villager_no1", 0.3)
        self.beat(Transform(bar, line_bar(code, 4, 4, MC_RED)), *[Wiggle(b) for b in row], rt=0.7)
        self.close_seg()

        # The other values of k, one sweep each, until the pickaxe breaks
        self.seg(6)
        self.beat(FadeOut(oa), FadeOut(ob), Transform(bar, line_bar(code, 1, 3, MC_YELLOW)), rt=0.3)
        end = ph(6, "a hundred")
        step = max(0.2, math.floor((end - 0.4) / (n - 2) * 30) / 30)
        for j, k in enumerate(range(n - 2, 0, -1)):
            c = (j + 2) * len(pairs)
            self.sfx(f"stone_dig{j % 4 + 1}", 0.25, delay=step * 0.4)
            self.beat(Transform(kl, klabel(k)), Transform(cnt, counter(c)), Transform(fill, dfill(1 - c / (total + 6))),
                      Rotate(pick, angle=-25 * DEGREES, rate_func=there_and_back), rt=step)
        self.until(ph(6, "a hundred"))
        self.beat(pulse(cnt, 1.3), rt=0.5)
        broken = MT("broken!", 34, MC_RED)
        broken.next_to(dbg, DOWN, buff=0.15)
        self.until(ph(6, "pickaxe is gone"))
        self.sfx("break", 0.45)
        self.beat(Wiggle(pick), Transform(fill, dfill(0.0)), FadeIn(broken, shift=UP * 0.1), rt=0.7)
        self.close_seg()

        self.seg(7)
        self.beat(FadeOut(VGroup(row, idx, oa, ob, code, bar, pick, dbg, fill, cnt, kl, broken)), rt=0.5)
        l1 = eq_line([("n", MC_WHITE), ("values of k", MC_GRAY)], 56, TERM, 0.3)
        l2 = eq_line([("n^2", MC_WHITE), ("pairs each", MC_GRAY)], 56, TERM, 0.3)
        VGroup(l1, l2).arrange(DOWN, buff=0.35).move_to([0, 2.2, 0])
        self.beat(FadeIn(l1, shift=UP * 0.2), rt=0.3)
        self.beat(FadeIn(l2, shift=UP * 0.2), rt=0.3)
        o = big_o_pow("n", 3, 72, MC_RED)
        o.move_to([0, -0.4, 0])
        self.until(ph(7, "n cubed", -0.5))
        self.beat(FadeIn(o, scale=0.5), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        row = block_row(NUMS, 3.1, size=0.95, gap=0.18)
        idx = index_row(row, 30)
        lamps = lamp_row(row, idx)
        reds = VGroup(*[outline(row[k], MC_RED, 7) for k in MISPLACED])

        self.seg(8)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(row), FadeIn(idx), FadeIn(lamps), rt=0.6)
        self.until(ph(8, "out of place"))
        self.sfx("villager_no2", 0.25)
        self.beat(Create(reds), rt=0.5)
        a = MISPLACED[0]
        self.until(ph(8, "has to move"))
        self.beat(VGroup(row[a], reds[0]).animate(rate_func=there_and_back).shift(UP * 0.45), rt=0.7)
        must = chat("out of place  ->  must swap", MC_YELLOW, 40)
        must.move_to([0, 0.2, 0])
        self.until(ph(8, "part of some"))
        self.beat(FadeIn(must, shift=UP * 0.2), rt=0.5)
        self.close_seg()

        # Every bit of k must be lit in both blocks of the swap: 3, 5 and k = 1 line up by bit
        self.seg(9)
        rows = [(f"{v}", MC_AQUA, v) for v in (3, 5)] + [("k", MC_GOLD, 1)]
        grid = VGroup()
        for s, c, v in rows:
            r = VGroup(MT(s, 36, c, PIXEL), lamp_bits(v, 0.55, 0.08)).arrange(RIGHT, buff=0.5)
            grid.add(r)
        grid.arrange(DOWN, buff=0.22, aligned_edge=RIGHT)
        grid.move_to([0, -2.0, 0])
        self.until(ph(9, "a swap"))
        self.beat(FadeOut(must), LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in grid], lag_ratio=0.25), rt=0.8)
        col = SurroundingRectangle(VGroup(*[r[1][BITS - 1] for r in grid]), color=MC_GREEN, buff=0.08, stroke_width=7)
        self.until(ph(9, "lit in both"))
        self.sfx("orb", 0.3)
        self.beat(Create(col), *[pulse(r[1][BITS - 1], 1.15) for r in grid], rt=0.6)
        self.close_seg()

        self.seg(10)
        self.until(ph(10, "every misplaced"))
        self.beat(*[pulse(row[k], 1.12) for k in MISPLACED], *[pulse(r, 1.06) for r in reds], rt=0.6)
        f = eq_line([("k", MC_GOLD), ("=", MC_GRAY), ("AND", MC_AQUA), ("of misplaced", MC_WHITE)], 52, TERM, 0.25)
        f.move_to([0, 0.15, 0])
        self.until(ph(10, "The biggest"))
        self.beat(FadeOut(VGroup(grid, col)), rt=0.3)
        self.sfx("pop", 0.4)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in f], lag_ratio=0.2), rt=0.9)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("ONE PASS", MC_GREEN)
        code = code_panel(AND_CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 2, 2, MC_YELLOW)

        def readout(v):
            r = VGroup(MT("panel", 40, MC_GRAY), MT(bit_str(v), 46, MC_GOLD, PIXEL), MT(f"= {v}", 40, MC_WHITE, PIXEL))
            r.arrange(RIGHT, buff=0.35)
            box = chat("", MC_WHITE, 40)
            box[0].stretch_to_fit_width(r.width + 0.6).stretch_to_fit_height(r.height + 0.35)
            g = VGroup(box[0].move_to([0, -1.15, 0]), r.move_to([0, -1.15, 0]))
            return g

        full = (1 << BITS) - 1
        ro = readout(full)
        tag = MT("running AND", 32, MC_GOLD)
        tag.next_to(ro, UP, buff=0.15)

        ev = [(seg_time(W["first"], W[key]), key, None)
              for key in ("intro_row", "panel_in", "lit", "running", "toast", "answer_t")]
        for k, s in enumerate(W["steps"]):
            for kind in ("visit", "verdict", "and", "dark"):
                if kind in s:
                    ev.append((seg_time(W["first"], s[kind]), kind, k))
        ev.sort(key=lambda e: e[0])

        def move_bar(line, color=MC_YELLOW, rt=0.15):
            self.beat(Transform(bar, line_bar(code, line, line, color)), rt=rt)

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.35)

        def on(kind, k):
            if kind == "intro_row":
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.5)
            elif kind == "panel_in":
                self.sfx("stone_dig2", 0.35)
                self.beat(FadeIn(bar), rt=0.2)
                move_bar(1, rt=0.2)
            elif kind == "lit":
                for d in (0.0, 0.25, 0.5):
                    self.sfx("click", 0.3, delay=d)
                self.beat(FadeIn(ro, shift=UP * 0.2), rt=0.4)
            elif kind == "running":
                self.beat(FadeIn(tag, shift=UP * 0.1), rt=0.4)
            elif kind == "visit":
                move_bar(2)
            elif kind == "verdict":
                s = W["steps"][k]
                if s["home"]:
                    self.sfx("stone_step2", 0.25)
                    move_bar(3, MC_GREEN)
                else:
                    self.sfx("villager_no3", 0.22)
                    move_bar(3, MC_RED)
            elif kind == "and":
                self.sfx("pop", 0.35, delay=0.45)
                move_bar(4)
            elif kind == "dark":
                s = W["steps"][k]
                new = readout(s["after"])
                self.sfx("click", 0.35)
                if s["after"] != s["before"]:
                    self.sfx("stone_dig3", 0.3, delay=0.05)
                self.beat(Transform(ro, new), rt=0.25)
            elif kind == "toast":
                t = toast("Advancement Made!", "Max K solved", "redstone_lamp_on", w=4.6)
                t.move_to([0, 5.5, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                for d in (0.0, 0.2, 0.4, 0.6):
                    self.sfx("orb", 0.3, delay=d)
                self.sfx("challenge", 0.32)
                self.beat(t.animate.shift(LEFT * 7), Transform(bar, line_bar(code, 5, 5, MC_GREEN)), rt=0.5)
            elif kind == "answer_t":
                # The answer takes the place of the panel readout: higher up it would cover the 3D row
                ans = chat(f"return {ANSWER}", MC_GREEN, 60)
                ans.move_to([0, -1.15, 0])
                self.beat(FadeOut(ro), FadeOut(tag), FadeIn(ans, shift=UP * 0.2), rt=0.4)

        def on_last():
            # The 3D clip fades to the roam at its end; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        per = VGroup(lamp_bits(5, 0.42), MT("one AND per block", 44, MC_WHITE))
        per.arrange(RIGHT, buff=0.35).move_to([0, 3.4, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n)", 1.05)).arrange(RIGHT, buff=0.4)
        tm.move_to([0, 1.65, 0])
        # The game's experience bar fills up as the walk goes linear
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.6, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(17)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(ph(17, "one AND"))
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in per], lag_ratio=0.25), rt=0.7)
        self.until(ph(17, "That's"))
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.35)
        self.add(xp)
        for d in (0.0, 0.2, 0.4):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=0.6)
        self.beat(Restore(xp), rt=0.6)
        self.close_seg()

        self.seg(18)
        panel = lamp_bits(ANSWER, 0.6, 0.06)
        num = MT("one number", 44, MC_WHITE)
        pv = VGroup(panel, num).arrange(RIGHT, buff=0.4)
        pv.move_to([0, -1.4, 0])
        self.until(ph(18, "single number", -0.3))
        self.sfx("click", 0.3)
        self.beat(FadeIn(pv, shift=UP * 0.15), rt=0.5)
        sp = VGroup(MT("space", 56, MC_GRAY), MT("O(1)", 52, MC_GOLD, PIXEL)).arrange(RIGHT, buff=0.4)
        sp.move_to([0, -3.1, 0])
        self.until(ph(18, "constant", -0.6))
        self.sfx("pop", 0.35)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(AND_CODE, 1.6, width=8.4)
        bar = line_bar(code, 2, 2, MC_YELLOW)

        self.seg(19)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(ph(19, "one check"))
        self.beat(Transform(bar, line_bar(code, 3, 3, MC_YELLOW)), rt=0.3)
        self.until(ph(19, "one AND"))
        self.beat(Transform(bar, line_bar(code, 4, 4, MC_GOLD)), rt=0.3)
        zero = chat("already sorted  ->  0", MC_AQUA, 44)
        zero.move_to([0, -1.7, 0])
        self.until(ph(19, "If nothing"))
        self.beat(Transform(bar, line_bar(code, 5, 5, MC_GREEN)), FadeIn(zero, shift=UP * 0.2), rt=0.4)
        self.close_seg()

        self.seg(20)
        msg = chat("Only misplaced blocks matter", MC_GOLD, 52)
        if msg.width > 8.4:
            msg.scale_to_fit_width(8.4)
        msg.move_to([0, -3.0, 0])
        self.until(0.1)
        self.beat(FadeOut(zero), FadeIn(msg, shift=UP * 0.2), rt=0.5)
        self.until(ph(20, "That's the big", -0.1))
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.4)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.9)
        self.close_seg()
