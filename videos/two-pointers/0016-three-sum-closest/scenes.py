WALK = json.load(open('walk.json', encoding='utf-8'))
RAW, NUMS, TARGET, ANSWER = WALK["raw"], WALK["nums"], WALK["target"], WALK["answer"]
ORE_OF.update(dict(zip(NUMS, WALK["ores"])))
# The best triple (2, 3, 4) in the sorted row and in the row as given
BEST_SORTED = (1, 2, 3)
BEST_RAW = tuple(RAW.index(NUMS[k]) for k in BEST_SORTED)

BRUTE_CODE = """def threeSumClosest(nums, target):
    best = nums[0] + nums[1] + nums[2]
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                s = nums[i] + nums[j] + nums[k]
                if abs(s - target) < abs(best - target):
                    best = s
    return best"""

CODE = """def threeSumClosest(nums, target):
    nums.sort()
    best = nums[0] + nums[1] + nums[2]
    for i in range(len(nums) - 2):
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if abs(s - target) < abs(best - target):
                best = s
            if s < target:
                l += 1
            else:
                r -= 1
    return best"""

PTR_COLORS = {"i": MC_GOLD, "L": MC_AQUA, "R": MC_PINK}


def at(i, phrase, nth=0):
    # Seconds into line i where the nth `phrase` starts (even speaking rate inside a line)
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
    return min(dur - 0.1, dur * k / len(text))


def index_row(row, size=30, color=MC_GRAY, buff=0.14):
    return VGroup(*[MT(str(k), size, color).next_to(b, DOWN, buff=buff) for k, b in enumerate(row)])


def target_sign(scale=1.0):
    return sign(["target", str(TARGET)], 2.2, 1.35, 46).scale(scale)


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def eq_line(parts, size=34, font=PIXEL, buff=0.3):
    return VGroup(*[MT(s, size, c, font) for s, c in parts]).arrange(RIGHT, buff=buff)


def pulse(m, k=1.15):
    # Emphasis that keeps the pixel art's colors (Indicate would paint it one flat color)
    return m.animate(rate_func=there_and_back).scale(k)


def ptr_mark(name, block, size=38):
    # Pointer letter under its block, in the pointer's color
    m = MT(name, size, PTR_COLORS[name], PIXEL)
    m.next_to(block, DOWN, buff=0.22)
    return m


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("3SUM", width=3.2).move_to([0, 4.85, 0])
    t2 = stone_title("CLOSEST", width=5.6).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    row = block_row(NUMS, 1.45, size=1.05, gap=0.2)
    frames = VGroup(*[outline(row[k], MC_GOLD, 8) for k in BEST_SORTED])
    marks = VGroup(*[ptr_mark(n, row[k]) for n, k in zip("iLR", BEST_SORTED)])
    tsign = target_sign(0.62).move_to([-2.0, -0.85, 0])
    best = chat("closest 9", MC_GOLD, 52).move_to([1.35, -0.85, 0])
    tags = VGroup(chat("LeetCode #16", MC_AQUA, 40), chat("Medium", MC_GOLD, 40), chat("Two Pointers", MC_GREEN, 40))
    tags.arrange(RIGHT, buff=0.22).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, row, frames, marks, tsign, best, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, row, frames, marks, tsign, best, tags = art
        self.add(art)

        self.seg(0)
        self.beat(pulse(spl), rt=0.8)
        # Blocks hop one after another, like a wave
        self.sfx("stone_dig1", 0.35, delay=0.35)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.35) for b in row], lag_ratio=0.18), rt=1.6)
        # The pointers close in on the best triple
        self.sfx("orb", 0.3, delay=0.3)
        self.beat(*[ShowPassingFlash(outline(row[k], MC_GOLD, 10), time_width=0.6) for k in BEST_SORTED],
                  LaggedStart(*[pulse(m, 1.3) for m in marks], lag_ratio=0.25), pulse(best, 1.1), rt=1.1)
        self.beat(pulse(tsign, 1.08), rt=0.6)
        self.beat(pulse(spl), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        tsign = target_sign().move_to([0, 3.55, 0])
        row = block_row(RAW, 1.15, size=1.05, gap=0.2)
        idx = index_row(row, 34)
        lab = MT("nums", 40, MC_WHITE).next_to(row, UP, buff=0.2).align_to(row, LEFT)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.35)
        # Blocks fall from the sky and bounce into place
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(len(row)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.32, delay=k * 0.1 + 0.3)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.1), rt=1.3)
        self.beat(FadeIn(idx, shift=UP * 0.1), FadeIn(lab), rt=0.3)
        self.until(at(1, "a target") - 0.1)
        self.sfx("wood_dig1", 0.4)
        self.beat(FadeIn(tsign, scale=0.6), rt=0.4)
        self.close_seg()

        self.seg(2)
        self.until(at(2, "three blocks") - 0.1)
        frames = VGroup(*[outline(row[k], MC_GOLD, 8) for k in BEST_RAW])
        self.sfx("click", 0.3)
        self.beat(Create(frames), rt=0.5)
        eq = eq_line([("4", MC_WHITE), ("+", MC_GRAY), ("2", MC_WHITE), ("+", MC_GRAY), ("3", MC_WHITE), ("=", MC_GRAY),
                      ("9", MC_GOLD)], 44)
        eq.move_to([0, -0.85, 0])
        self.until(at(2, "as close") - 0.2)
        self.beat(FadeIn(eq, shift=UP * 0.2), rt=0.4)
        off = eq_line([("|9 - 10|", MC_WHITE), ("=", MC_GRAY), ("1", MC_GREEN)], 36)
        off.move_to([0, -1.85, 0])
        lab2 = MT("closest of all triples", 38, MC_GRAY).next_to(off, DOWN, buff=0.25)
        self.until(at(2, "to the target") - 0.1)
        self.beat(FadeIn(off, shift=UP * 0.15), FadeIn(lab2), rt=0.4)
        ret = chat("return 9", MC_GREEN, 60)
        ret.move_to([0, -4.0, 0])
        self.until(at(2, "return that") - 0.1)
        self.sfx("pop", 0.4)
        self.beat(FadeIn(ret, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("BRUTE FORCE", MC_RED)
        row = block_row(RAW, 3.0, size=0.95, gap=0.2)
        idx = index_row(row, 30)
        code = code_panel(BRUTE_CODE, -3.7, max_h=2.9)
        pick = pickaxe(1.05).move_to([-2.4, 1.0, 0])
        dbg = Rectangle(width=1.2, height=0.16, fill_color="#000000", fill_opacity=1, stroke_width=0)
        dbg.next_to(pick, DOWN, buff=0.15)
        trips = [(i, j, k) for i in range(5) for j in range(i + 1, 5) for k in range(j + 1, 5)]

        def dfill(frac):
            # Durability bar: shrinks and turns from green to red
            r = Rectangle(width=max(1.16 * frac, 0.02), height=0.1, stroke_width=0, fill_opacity=1,
                          fill_color=interpolate_color(ManimColor(MC_RED), ManimColor(MC_GREEN), frac))
            r.move_to(dbg.get_left() + RIGHT * (0.02 + max(1.16 * frac, 0.02) / 2))
            return r

        def counter(k):
            c = MT(f"triples {k}", 30, MC_WHITE, PIXEL)
            c.move_to([1.0, 1.0, 0])
            return c

        fill = dfill(1.0)
        st = {"cnt": counter(0)}

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in row], lag_ratio=0.1), rt=0.8)
        self.beat(FadeIn(idx), rt=0.3)
        self.until(1.4)
        self.beat(FadeIn(code, shift=UP * 0.3), rt=0.5)
        self.until(2.4)
        self.beat(FadeIn(pick, scale=0.6), FadeIn(dbg), FadeIn(fill), FadeIn(st["cnt"]), rt=0.5)
        self.close_seg()

        frames = [outline(row[k], c, 7) for k, c in zip((0, 1, 2), (MC_YELLOW, MC_WHITE, MC_AQUA))]
        bar = line_bar(code, 3, 3, MC_YELLOW)

        self.seg(4)
        self.until(at(4, "Fix one"))
        self.beat(Create(frames[0]), FadeIn(bar), rt=0.35)
        self.until(at(4, "a second") - 0.1)
        self.beat(Create(frames[1]), Transform(bar, line_bar(code, 4, 4, MC_YELLOW)), rt=0.35)
        self.until(at(4, "a third") - 0.1)
        self.beat(Create(frames[2]), Transform(bar, line_bar(code, 5, 5, MC_YELLOW)), rt=0.35)
        self.close_seg()

        def check(n, rt):
            i, j, k = trips[n]
            nc = counter(n + 1)
            anims = [frames[0].animate.move_to(row[i]), frames[1].animate.move_to(row[j]), frames[2].animate.move_to(row[k]),
                     Transform(fill, dfill(1 - (n + 1) / 14)), FadeTransform(st["cnt"], nc),
                     Transform(bar, line_bar(code, 6, 7, MC_YELLOW)),
                     Rotate(pick, angle=-25 * DEGREES, rate_func=there_and_back)]
            # The pickaxe hits the block halfway through its swing
            self.sfx(f"stone_dig{n % 4 + 1}", 0.22, delay=rt * 0.5)
            self.beat(*anims, rt=rt)
            st["cnt"] = nc

        self.seg(5)
        for n in range(len(trips)):
            check(n, 0.2)
        wear = MT("wearing out!", 30, MC_RED)
        wear.next_to(dbg, DOWN, buff=0.15)
        self.until(at(5, "Our pickaxe") - 0.1)
        self.sfx("stone_dig3", 0.35)
        self.beat(Wiggle(pick), FadeIn(wear, shift=UP * 0.1), rt=0.7)
        self.close_seg()

        self.seg(6)
        self.beat(FadeOut(Group(row, idx, *frames, code, bar, pick, dbg, fill, st["cnt"], wear)), rt=0.4)
        o = big_o_pow("n", 3, 72, MC_RED)
        o.move_to([0, 2.4, 0])
        self.until(at(6, "n cubed") - 0.2)
        self.beat(FadeIn(o, scale=0.5), rt=0.4)
        n = eq_line([("n =", MC_GRAY), ("3,000", MC_WHITE)], 32)
        n.move_to([0, 0.9, 0])
        self.until(at(6, "A few") - 0.1)
        self.beat(FadeIn(n, shift=UP * 0.2), rt=0.4)
        big = MT("4,495,501,000", 40, MC_RED, PIXEL)
        big.move_to([0, -0.5, 0])
        pl = MT("checks", 52, MC_GRAY)
        pl.next_to(big, DOWN, buff=0.25)
        self.until(at(6, "billions") - 0.2)
        self.beat(FadeIn(big, scale=1.4), FadeIn(pl), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        row = block_row(RAW, 2.4, size=1.0, gap=0.25)
        srt = block_row(NUMS, 2.4, size=1.0, gap=0.25)
        order = [NUMS.index(v) for v in RAW]   # sorted place of each raw block

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(row, shift=DOWN * 0.2), rt=0.6)
        self.until(at(7, "sort the row") - 0.1)
        self.sfx("stone_step2", 0.3)
        self.sfx("stone_step4", 0.3, delay=0.5)
        self.beat(*[row[k].animate(path_arc=-PI / 3).move_to(srt[order[k]]) for k in range(len(RAW))], rt=0.9)
        # From here on, sorted[k] is the block in sorted place k
        blocks = [row[RAW.index(v)] for v in NUMS]
        im = ptr_mark("i", blocks[0])
        fi = outline(blocks[0], MC_GOLD, 8)
        self.until(at(7, "fix one") - 0.1)
        self.sfx("click", 0.3)
        self.beat(Create(fi), FadeIn(im, shift=UP * 0.2), rt=0.4)
        lm, rm = ptr_mark("L", blocks[1]), ptr_mark("R", blocks[4])
        fl, fr = outline(blocks[1], MC_AQUA, 7), outline(blocks[4], MC_PINK, 7)
        self.until(at(7, "two pointers") - 0.1)
        self.sfx("click", 0.3)
        self.beat(Create(fl), Create(fr), FadeIn(lm, shift=UP * 0.2), FadeIn(rm, shift=UP * 0.2), rt=0.4)
        self.close_seg()

        small = eq_line([("sum < target", MC_AQUA), ("->", MC_GRAY), ("L moves right", MC_AQUA)], 42, TERM, 0.3)
        small.move_to([0, 0.0, 0])
        bigg = eq_line([("sum > target", MC_PINK), ("->", MC_GRAY), ("R moves left", MC_PINK)], 42, TERM, 0.3)
        bigg.move_to([0, -1.1, 0])

        self.seg(8)
        self.until(0.1)
        self.beat(FadeIn(small[0], shift=UP * 0.15), rt=0.4)
        self.until(at(8, "the left pointer") - 0.1)
        self.sfx("stone_step1", 0.3)
        self.beat(FadeIn(small[1:], shift=UP * 0.15), lm.animate.next_to(blocks[2], DOWN, buff=0.22),
                  fl.animate.move_to(blocks[2]), rt=0.5)
        self.until(at(8, "If it's") - 0.1)
        self.beat(FadeIn(bigg[0], shift=UP * 0.15), rt=0.4)
        self.until(at(8, "the right pointer") - 0.1)
        self.sfx("stone_step3", 0.3)
        self.beat(FadeIn(bigg[1:], shift=UP * 0.15), rm.animate.next_to(blocks[3], DOWN, buff=0.22),
                  fr.animate.move_to(blocks[3]), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("2 POINTERS", MC_GREEN)
        tsign = target_sign(0.6)
        tsign.move_to([0, TOP_Y - 0.05, 0]).to_edge(RIGHT, buff=0.4)
        code = code_panel(CODE, -3.85, max_h=3.7)
        bar = line_bar(code, 1, 2, MC_YELLOW)
        st = {"sum": None, "best": None}

        def sum_line(s, judged=False):
            # "-5 + 2 + 7 = 4 < 10"; once judged worse, the miss distance in red instead of the direction
            a, b, c = NUMS[s["i"]], NUMS[s["l"]], NUMS[s["r"]]
            parts = [(str(a), MC_GOLD), ("+", MC_GRAY), (str(b), MC_AQUA), ("+", MC_GRAY), (str(c), MC_PINK), ("=", MC_GRAY),
                     (str(s["sum"]), MC_WHITE)]
            if judged:
                parts += [("off", MC_GRAY), (str(abs(s["sum"] - TARGET)), MC_RED)]
            elif s["sum"] < TARGET:
                parts += [("<", MC_AQUA), (str(TARGET), MC_YELLOW)]
            else:
                parts += [(">", MC_PINK), (str(TARGET), MC_YELLOW)]
            line = eq_line(parts, 32, buff=0.22)
            line.move_to([0, -0.45, 0])
            return line

        def best_line(v):
            line = eq_line([("best =", MC_GRAY), (str(v), MC_GOLD), ("off", MC_GRAY), (str(abs(v - TARGET)), MC_GREEN)], 32, buff=0.25)
            line.move_to([0, -1.2, 0])
            return line

        def swap(key, new, rt=0.15):
            anims = [FadeIn(new)]
            if st[key] is not None:
                anims.append(FadeOut(st[key]))
            st[key] = new
            self.beat(*anims, rt=rt)

        def move_bar(k0, k1=None, color=MC_YELLOW, rt=0.12):
            self.beat(Transform(bar, line_bar(code, k0, k1, color)), rt=rt)

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("row_in", "target_t", "stays", "toast", "answer_t")]
        for k, s in enumerate(W["steps"]):
            for kind in ("fix", "sum_t", "judge", "move_t"):
                if s.get(kind) is not None:
                    ev.append((seg_time(W["first"], s[kind]), kind, k))
        ev.sort(key=lambda e: e[0])

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(tsign), rt=0.35)

        def on(kind, k):
            s = W["steps"][k] if k is not None else None
            if kind == "row_in":
                for i in range(5):
                    self.sfx(f"stone_dig{i % 4 + 1}", 0.28, delay=0.12 * i + 0.35)
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.5)
            elif kind == "target_t":
                self.sfx("wood_dig2", 0.35)
                self.beat(FadeIn(bar), pulse(tsign, 1.12), rt=0.4)
            elif kind == "fix":
                self.sfx("click", 0.3)
                move_bar(3, 4, MC_GOLD, rt=0.2)
                if st["sum"] is not None:
                    self.beat(FadeOut(st["sum"]), rt=0.1)
                    st["sum"] = None
            elif kind == "sum_t":
                self.sfx(f"stone_step{k % 6 + 1}", 0.3)
                move_bar(6, rt=0.08)
                swap("sum", sum_line(s), rt=0.12)
            elif kind == "judge":
                if s["better"]:
                    self.sfx("orb", 0.28)
                    move_bar(7, 8, MC_GREEN, rt=0.08)
                    swap("best", best_line(s["best"]), rt=0.12)
                else:
                    self.sfx("villager_no2", 0.35)
                    move_bar(7, None, MC_RED, rt=0.1)
                    swap("sum", sum_line(s, judged=True), rt=0.15)
            elif kind == "move_t":
                self.sfx("stone_step2", 0.28)
                if s["move"] == "L":
                    move_bar(9, 10, MC_AQUA, rt=0.12)
                else:
                    move_bar(11, 12, MC_PINK, rt=0.12)
            elif kind == "stays":
                self.beat(pulse(st["best"], 1.12), rt=0.4)
            elif kind == "toast":
                t = toast("Advancement Made!", "3Sum Closest solved", w=4.6)
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(tsign), Transform(bar, line_bar(code, 13, 13, MC_GREEN)), rt=0.5)
            elif kind == "answer_t":
                ans = chat(f"return {ANSWER}", MC_GREEN, 56)
                ans.move_to([0, 4.4, 0])
                self.beat(FadeIn(ans, shift=UP * 0.2), rt=0.4)

        def on_last():
            # The 3D clip fades to sky at its end; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        srt = VGroup(MT("sort", 52, MC_GRAY), MT("O(n log n)", 36, MC_WHITE, PIXEL)).arrange(RIGHT, buff=0.35)
        srt.move_to([0, 3.5, 0])
        sweep = MT("n fixed blocks x 1 sweep", 46, MC_GRAY)
        sweep.move_to([0, 2.5, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n²)", 1.05)).arrange(RIGHT, buff=0.4)
        tm.move_to([0, 1.3, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.25, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(srt, shift=UP * 0.15), rt=0.5)
        self.until(at(16, "each fixed") - 0.2)
        self.sfx("stone_step2", 0.3)
        self.beat(FadeIn(sweep, shift=UP * 0.15), rt=0.4)
        self.until(at(16, "n squared") - 0.4)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.4)
        self.add(xp)
        for d in (0.0, 0.3, 0.6):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=0.9)
        self.beat(Restore(xp), rt=1.0)
        self.close_seg()

        old = big_o_pow("n", 3, 44, MC_RED)
        arrow = MT("->", 70, MC_GRAY)
        new = big_o_pow("n", 2, 44, MC_GREEN)
        cmp = VGroup(old, arrow, new).arrange(RIGHT, buff=0.45)
        cmp.move_to([0, -1.2, 0])
        strike = Line(old.get_left() + LEFT * 0.1, old.get_right() + RIGHT * 0.1, color=MC_RED, stroke_width=8)
        keep = chat("best = 9", MC_GOLD, 46)
        keep.move_to([0, -2.6, 0])
        sp = VGroup(MT("space", 56, MC_GRAY), level_text("O(1)", 1.05)).arrange(RIGHT, buff=0.4)
        sp.move_to([0, -3.9, 0])

        self.seg(17)
        self.beat(FadeIn(old, shift=UP * 0.15), rt=0.4)
        self.until(at(17, "cubed"))
        self.beat(Create(strike), FadeIn(arrow), FadeIn(new, shift=LEFT * 0.2), rt=0.5)
        self.until(at(17, "the best sum") - 0.2)
        self.sfx("pop", 0.3)
        self.beat(FadeIn(keep, scale=0.6), rt=0.4)
        self.until(at(17, "Constant") - 0.2)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.6, width=8.4, max_h=6.6)
        bar = line_bar(code, 1, 1, MC_YELLOW)

        self.seg(18)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.05), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.2)
        self.until(at(18, "fix one") - 0.1)
        self.beat(Transform(bar, line_bar(code, 3, 3, MC_GOLD)), rt=0.25)
        self.until(at(18, "squeeze") - 0.1)
        self.beat(Transform(bar, line_bar(code, 5, 12, MC_AQUA)), rt=0.3)
        self.close_seg()

        self.seg(19)
        msg = chat("Every move has a direction", MC_GOLD, 52)
        msg.move_to([0, -2.7, 0])
        self.until(0.1)
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.4)
        self.until(DUR[19] - 1.6)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.45)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.9)
        self.close_seg()
