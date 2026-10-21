WALK = json.load(open('walk.json', encoding='utf-8'))
NUMS, SORTED = WALK["nums"], WALK["sorted"]
ORE_OF.update(dict(zip(SORTED, WALK["ores"])))

BRUTE_CODE = """def threeSum(nums):
    res = set()
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            for k in range(j + 1, len(nums)):
                if nums[i] + nums[j] + nums[k] == 0:
                    res.add(tuple(sorted((nums[i], nums[j], nums[k]))))
    return [list(t) for t in res]"""

CODE = """def threeSum(nums):
    nums.sort(); res = []
    for i in range(len(nums) - 2):
        if i and nums[i] == nums[i - 1]: continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0: l += 1
            elif s > 0: r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                l += 1; r -= 1
                while l < r and nums[l] == nums[l - 1]: l += 1
    return res"""


def index_row(row, size=30, color=MC_GRAY, buff=0.14):
    return VGroup(*[MT(str(k), size, color).next_to(b, DOWN, buff=buff) for k, b in enumerate(row)])


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def eq_line(parts, size=34, font=PIXEL, buff=0.3):
    return VGroup(*[MT(s, size, c, font) for s, c in parts]).arrange(RIGHT, buff=buff)


def pulse(m, k=1.15):
    # Emphasis that keeps the pixel art's colors (Indicate would paint it one flat color)
    return m.animate(rate_func=there_and_back).scale(k)


def triple(t, color=MC_GREEN, size=44):
    return chat("[" + ", ".join(str(v) for v in t) + "]", color, size)


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    title = stone_title("3SUM", 60, width=5.2).move_to([0, 4.2, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.25, 2.95, 0])
    row = block_row(SORTED, 1.2, size=1.05, gap=0.2)
    zero = VGroup(MT("= 0", 60, MC_GOLD, PIXEL)).move_to([0, -0.35, 0])
    trips = VGroup(triple(WALK["res"][0], MC_GREEN, 40), triple(WALK["res"][1], MC_GREEN, 40)).arrange(RIGHT, buff=0.35)
    trips.move_to([0, -1.55, 0])
    tags = VGroup(chat("LeetCode #15", MC_AQUA, 46), chat("Medium", MC_GOLD, 46), chat("Two Pointers", MC_GREEN, 46))
    tags.arrange(RIGHT, buff=0.22).move_to([0, -3.05, 0])
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, title, spl, row, zero, trips, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, title, spl, row, zero, trips, tags = art
        self.add(art)

        self.seg(0)
        self.beat(pulse(spl), rt=0.8)
        self.sfx("stone_dig1", 0.35, delay=0.35)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.35) for b in row], lag_ratio=0.18), rt=1.5)
        self.sfx("orb", 0.3, delay=0.3)
        self.beat(*[ShowPassingFlash(outline(row[k], MC_GOLD, 10), time_width=0.6) for k in (1, 2, 5)], pulse(trips[0]), rt=0.9)
        self.beat(pulse(spl), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        row = block_row(NUMS, 1.6, size=1.05, gap=0.2)
        idx = index_row(row)
        lab = MT("nums", 40, MC_WHITE).next_to(row, UP, buff=0.2).align_to(row, LEFT)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(len(row)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.3, delay=k * 0.12 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.12), rt=1.6)
        self.beat(FadeIn(idx, shift=UP * 0.1), FadeIn(lab), rt=0.4)
        goal = eq_line([("a", MC_WHITE), ("+", MC_GRAY), ("b", MC_WHITE), ("+", MC_GRAY), ("c", MC_WHITE), ("=", MC_GRAY),
                        ("0", MC_GOLD)], 44).move_to([0, -0.4, 0])
        self.until(min(4.0, DUR[1] - 1.2))
        self.beat(FadeIn(goal, shift=UP * 0.2), rt=0.5)
        self.close_seg()

        self.seg(2)
        t1 = triple(WALK["res"][0]).move_to([-2.0, -1.9, 0])
        t2 = triple(WALK["res"][1]).move_to([2.0, -1.9, 0])
        once = MT("each one only once", 40, MC_GRAY).move_to([0, -3.1, 0])
        self.until(0.4)
        self.beat(FadeIn(once, shift=UP * 0.1), rt=0.4)
        self.until(min(2.6, DUR[2] - 1.4))
        self.sfx("pop", 0.35)
        self.beat(FadeIn(t1, shift=UP * 0.2), rt=0.4)
        self.sfx("pop", 0.35)
        self.beat(FadeIn(t2, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("EVERY TRIPLE", MC_RED)
        row = block_row(NUMS, 3.0, size=0.95, gap=0.2)
        idx = index_row(row, 28)
        code = code_panel(BRUTE_CODE, -3.7, max_h=2.9)
        pick = pickaxe(1.0).move_to([-2.9, 0.9, 0])
        dbg = Rectangle(width=1.2, height=0.16, fill_color="#000000", fill_opacity=1, stroke_width=0)
        dbg.next_to(pick, DOWN, buff=0.15)
        trip = [(i, j, k) for i in range(6) for j in range(i + 1, 6) for k in range(j + 1, 6)]

        def dfill(frac):
            r = Rectangle(width=max(1.16 * frac, 0.02), height=0.1, stroke_width=0, fill_opacity=1,
                          fill_color=interpolate_color(ManimColor(MC_RED), ManimColor(MC_GREEN), frac))
            r.move_to(dbg.get_left() + RIGHT * (0.02 + max(1.16 * frac, 0.02) / 2))
            return r

        def counter(k):
            return MT(f"triples {k}", 32, MC_WHITE, PIXEL).move_to([1.0, 0.9, 0])

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in row], lag_ratio=0.1), rt=0.8)
        self.beat(FadeIn(idx), rt=0.3)
        self.until(1.6)
        self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
        self.close_seg()

        fill = dfill(1.0)
        st = {"cnt": counter(0)}
        frames = VGroup(*[outline(row[k], c, 7) for k, c in zip((0, 1, 2), (MC_YELLOW, MC_WHITE, MC_AQUA))])
        bar = line_bar(code, 2, 4, MC_YELLOW)
        found = VGroup()
        self.seg(4)
        self.beat(FadeIn(pick, scale=0.6), FadeIn(dbg), FadeIn(fill), FadeIn(st["cnt"]), Create(frames), FadeIn(bar), rt=0.5)

        def check(n, rt):
            i, j, k = trip[n]
            nc = counter(n + 1)
            hit = NUMS[i] + NUMS[j] + NUMS[k] == 0
            anims = [frames[0].animate.move_to(row[i]), frames[1].animate.move_to(row[j]), frames[2].animate.move_to(row[k]),
                     Transform(fill, dfill(1 - (n + 1) / 21)), FadeTransform(st["cnt"], nc),
                     Rotate(pick, angle=-25 * DEGREES, rate_func=there_and_back)]
            if hit:
                key = tuple(sorted((NUMS[i], NUMS[j], NUMS[k])))
                dup = any(m.key == key for m in found)
                t = triple(key, MC_GOLD if dup else MC_GREEN, 36)
                t.key = key
                t.move_to([0, 0.0 - 0.6 * len(found), 0]).shift(RIGHT * 1.6)
                if dup:
                    t.add(MT("repeat!", 30, MC_GOLD).next_to(t, LEFT, buff=0.2))
                found.add(t)
                anims.append(FadeIn(t, shift=UP * 0.1))
                self.sfx("orb" if not dup else "villager_no1", 0.3)
            else:
                self.sfx(f"stone_dig{n % 4 + 1}", 0.2, delay=rt * 0.5)
            self.beat(*anims, rt=rt)
            st["cnt"] = nc

        n4 = 6
        for n in range(n4):
            check(n, min(0.5, (DUR[4] - 0.8) / n4))
        self.close_seg()

        self.seg(5)
        for n in range(n4, len(trip)):
            check(n, min(0.24, (DUR[5] - 1.5) / (len(trip) - n4)))
        broken = MT("almost broken!", 30, MC_RED).next_to(dbg, DOWN, buff=0.12)
        self.sfx("break", 0.45)
        self.beat(Wiggle(pick), FadeIn(broken, shift=UP * 0.1), rt=0.6)
        self.close_seg()

        self.seg(6)
        self.beat(FadeOut(Group(*self.mobjects)), rt=0.5)
        n = eq_line([("n =", MC_GRAY), ("1,000", MC_WHITE)], 32).move_to([0, 2.6, 0])
        self.beat(FadeIn(n, shift=UP * 0.2), rt=0.4)
        big = MT("166,167,000", 44, MC_RED, PIXEL).move_to([0, 1.0, 0])
        pl = MT("triples", 52, MC_GRAY).next_to(big, DOWN, buff=0.25)
        self.until(min(2.4, DUR[6] - 2.2))
        self.beat(FadeIn(big, scale=1.4), FadeIn(pl), rt=0.5)
        o = big_o_pow("n", 3, 72, MC_RED).move_to([0, -1.9, 0])
        self.until(DUR[6] - 1.1)
        self.beat(FadeIn(o, scale=0.5), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        row = block_row(NUMS, 2.6, size=1.0, gap=0.2)
        srt = block_row(SORTED, 2.6, size=1.0, gap=0.2)

        def mark(s, k, color):
            return MT(s, 40, color, PIXEL).next_to(srt[k], DOWN, buff=0.25)

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(row, shift=DOWN * 0.2), rt=0.6)
        self.until(1.3)
        self.sfx("stone_step2", 0.3)
        self.beat(*[Transform(row[k], srt[sorted(range(6), key=lambda q: (NUMS[q], q)).index(k)]) for k in range(6)], rt=0.9)
        im, lm, rm = mark("i", 0, MC_GOLD), mark("L", 1, MC_AQUA), mark("R", 5, MC_PINK)
        self.until(min(3.2, DUR[7] - 2.4))
        self.beat(Create(outline(srt[0], MC_GOLD, 8)), FadeIn(im, shift=UP * 0.2), rt=0.4)
        self.until(min(4.4, DUR[7] - 1.0))
        self.beat(FadeIn(lm, shift=UP * 0.2), FadeIn(rm, shift=UP * 0.2), rt=0.4)
        self.close_seg()

        self.seg(8)
        small = eq_line([("sum < 0", MC_AQUA), ("->", MC_GRAY), ("L ->", MC_AQUA)], 40, TERM, 0.3).move_to([0, -0.4, 0])
        bigg = eq_line([("sum > 0", MC_PINK), ("->", MC_GRAY), ("<- R", MC_PINK)], 40, TERM, 0.3).move_to([0, -1.5, 0])
        self.until(0.2)
        self.sfx("click", 0.3)
        self.beat(FadeIn(small, shift=UP * 0.15), lm.animate.next_to(srt[2], DOWN, buff=0.25), rt=0.5)
        self.until(min(2.6, DUR[8] - 1.6))
        self.sfx("click", 0.3)
        self.beat(FadeIn(bigg, shift=UP * 0.15), rm.animate.next_to(srt[4], DOWN, buff=0.25), rt=0.5)
        sq = MT("a squeeze", 50, MC_GOLD).move_to([0, -2.8, 0])
        self.until(DUR[8] - 0.9)
        self.beat(FadeIn(sq, shift=UP * 0.1), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("SQUEEZE", MC_GREEN)
        code = code_panel(CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 1, 1, MC_YELLOW)

        def chip(i):
            return chat(f"i = {i}", MC_GOLD, 40).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)

        def sumline(e):
            col = {"small": MC_AQUA, "big": MC_PINK, "zero": MC_GREEN}[e["verdict"]]
            parts = [(str(SORTED[e["i"]]), MC_GOLD), ("+", MC_GRAY), (str(SORTED[e["l"]]), MC_AQUA), ("+", MC_GRAY),
                     (str(SORTED[e["r"]]), MC_PINK), ("=", MC_GRAY), (str(e["s"]), col)]
            return eq_line(parts, 34, buff=0.2).move_to([0, -0.9, 0])

        st = {"chip": None, "sum": None}
        found = VGroup()

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("sort_t", "step_in", "meet", "toast", "answer")]
        for k, e in enumerate(W["events"]):
            ev.append((seg_time(W["first"], e["t"]), e["kind"], k))
            if "found" in e:
                ev.append((seg_time(W["first"], e["found"]), "found", k))
        ev.sort(key=lambda x: x[0])

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.35)

        def on(kind, k):
            e = W["events"][k] if k is not None else None
            if kind == "sort_t":
                self.sfx("stone_step3", 0.3)
                self.beat(FadeIn(code, shift=UP * 0.3), FadeIn(bar), rt=0.6)
            elif kind == "fix":
                c = chip(e["i"])
                anims = [Transform(bar, line_bar(code, 2, 2, MC_GOLD))]
                if st["chip"] is None:
                    st["chip"] = c
                    anims.append(FadeIn(c))
                else:
                    anims.append(FadeTransform(st["chip"], c))
                    st["chip"] = c
                self.sfx("click", 0.3)
                self.beat(*anims, rt=0.25)
            elif kind == "skip":
                c = chip(e["i"])
                self.sfx("villager_no2", 0.3)
                self.beat(FadeTransform(st["chip"], c), Transform(bar, line_bar(code, 3, 3, MC_RED)), rt=0.3)
                st["chip"] = c
            elif kind == "check":
                s = sumline(e)
                line = {"small": 7, "big": 8, "zero": 10}[e["verdict"]]
                col = {"small": MC_AQUA, "big": MC_PINK, "zero": MC_GREEN}[e["verdict"]]
                anims = [Transform(bar, line_bar(code, line, line, col))]
                if st["sum"] is None:
                    anims.append(FadeIn(s, shift=UP * 0.1))
                else:
                    anims.append(FadeTransform(st["sum"], s))
                st["sum"] = s
                self.sfx(f"stone_step{k % 6 + 1}", 0.28)
                self.beat(*anims, rt=0.2)
            elif kind == "found":
                t = triple([SORTED[e["i"]], SORTED[e["l"]], SORTED[e["r"]]], MC_GREEN, 44)
                # Two answers: each takes its half of the line
                t.move_to([-2.0 + 4.0 * len(found), -1.9, 0])
                found.add(t)
                for d in (0.0, 0.18, 0.36):
                    self.sfx("orb", 0.28, delay=d)
                self.beat(FadeIn(t, shift=UP * 0.15), rt=0.35)
            elif kind == "step_in":
                self.beat(Transform(bar, line_bar(code, 11, 12, MC_YELLOW)), rt=0.25)
            elif kind == "meet":
                self.beat(Transform(bar, line_bar(code, 5, 5, MC_GRAY)), FadeOut(st["sum"]), rt=0.3)
            elif kind == "toast":
                t = toast("Advancement Made!", "Three Sum solved", w=4.6)
                t.move_to([0, 5.5, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(st["chip"]), Transform(bar, line_bar(code, 13, 13, MC_GREEN)), rt=0.5)
            elif kind == "answer":
                self.beat(pulse(found, 1.1), rt=0.5)

        def on_last():
            # The 3D clip fades to sky at its end; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        srt = VGroup(MT("sort", 48, MC_GRAY), MT("O(n log n)", 36, MC_WHITE, PIXEL)).arrange(RIGHT, buff=0.35).move_to([0, 3.4, 0])
        walk = VGroup(MT("n fixes x 1 squeeze", 44, MC_GRAY)).move_to([0, 2.5, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), big_o_pow("n", 2, 56, MC_GREEN)).arrange(RIGHT, buff=0.4)
        tm.move_to([0, 1.3, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.3, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(srt, shift=UP * 0.15), rt=0.5)
        self.until(min(2.0, DUR[16] - 3.0))
        self.beat(FadeIn(walk, shift=UP * 0.15), rt=0.4)
        self.until(min(4.0, DUR[16] - 1.8))
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.4)
        self.add(xp)
        for d in (0.0, 0.3, 0.6, 0.9):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=1.1)
        self.beat(Restore(xp), rt=1.2)
        self.close_seg()

        self.seg(17)
        old = big_o_pow("n", 3, 44, MC_RED)
        arrow = MT("->", 70, MC_GRAY)
        new = big_o_pow("n", 2, 44, MC_GREEN)
        cmp = VGroup(old, arrow, new).arrange(RIGHT, buff=0.45).move_to([0, -1.4, 0])
        strike = Line(old.get_left() + LEFT * 0.1, old.get_right() + RIGHT * 0.1, color=MC_RED, stroke_width=8)
        rep = MT("repeats sit side by side", 40, MC_WHITE).move_to([0, -2.8, 0])
        self.beat(FadeIn(old, shift=UP * 0.15), rt=0.4)
        self.until(min(1.2, DUR[17] - 2.6))
        self.beat(Create(strike), FadeIn(arrow), FadeIn(new, shift=LEFT * 0.2), rt=0.5)
        self.until(min(2.8, DUR[17] - 1.2))
        self.beat(FadeIn(rep, shift=UP * 0.1), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.4, width=8.4)
        bar = line_bar(code, 1, 1, MC_YELLOW)

        self.seg(18)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.06), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.2)
        self.until(min(1.3, DUR[18] - 1.4))
        self.beat(Transform(bar, line_bar(code, 2, 2, MC_GOLD)), rt=0.25)
        self.until(DUR[18] - 0.8)
        self.beat(Transform(bar, line_bar(code, 5, 8, MC_AQUA)), rt=0.3)
        self.close_seg()

        self.seg(19)
        msg = chat("Sort, then squeeze", MC_GOLD, 60).move_to([0, -3.0, 0])
        self.until(0.1)
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.5)
        self.until(DUR[19] - 1.9)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.5)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=1.0)
        self.close_seg()
