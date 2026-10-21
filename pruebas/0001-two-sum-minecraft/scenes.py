WALK = json.load(open('walk.json', encoding='utf-8'))
NUMS, TARGET = WALK["nums"], WALK["target"]
ORE_OF.update(dict(zip(NUMS, WALK["ores"])))

BRUTE_CODE = """def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]"""

HASH_CODE = """def twoSum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i"""


def index_row(row, size=34, color=MC_GRAY, buff=0.14):
    return VGroup(*[MT(str(k), size, color).next_to(b, DOWN, buff=buff) for k, b in enumerate(row)])


def target_sign(scale=1.0):
    return sign(["target", str(TARGET)], 2.2, 1.35, 46).scale(scale)


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def eq_line(parts, size=34, font=PIXEL, buff=0.3):
    return VGroup(*[MT(s, size, c, font) for s, c in parts]).arrange(RIGHT, buff=buff)


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    title = stone_title("TWO SUM", 60, width=7.8).move_to([0, 4.0, 0])
    spl = splash("Minecraft edition!", 15).move_to([2.0, 2.95, 0])
    row = block_row(NUMS, 0.95, size=1.05, gap=0.2)
    idx = index_row(row)
    pick = pickaxe(1.25).move_to([-1.3, -1.2, 0])
    chest = pixel_art("chest_front", 1.15).move_to([1.3, -1.2, 0])
    tags = VGroup(chat("LeetCode #1", MC_AQUA, 46), chat("Easy", MC_GREEN, 46), chat("Hash Map", MC_GOLD, 46))
    tags.arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
    ground = ground_strip(-5.15)
    return VGroup(ground, title, spl, row, idx, pick, chest, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, title, spl, row, idx, pick, chest, tags = art
        self.add(art)

        self.seg(0)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        # Blocks hop one after another, like a wave
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.35) for b in row], lag_ratio=0.18), rt=1.6)
        self.beat(*[ShowPassingFlash(outline(row[k], MC_GOLD, 10), time_width=0.6) for k in (4, 5)],
                  *[row[k].animate(rate_func=there_and_back).scale(1.12) for k in (4, 5)],
                  Rotate(pick, angle=-30 * DEGREES, rate_func=there_and_back), rt=0.9)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        tsign = target_sign().move_to([0, 3.55, 0])
        row = block_row(NUMS, 1.15, size=1.05, gap=0.2)
        idx = index_row(row)
        lab = MT("nums", 40, MC_WHITE).next_to(row, UP, buff=0.2).align_to(row, LEFT)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        # Blocks fall from the sky and bounce into place
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.12), rt=1.6)
        self.beat(FadeIn(idx, shift=UP * 0.1), FadeIn(lab), rt=0.4)
        self.until(3.3)
        self.beat(FadeIn(tsign, scale=0.6), rt=0.5)
        self.close_seg()

        self.seg(2)
        self.until(0.8)
        frames = VGroup(outline(row[4], MC_GOLD, 8), outline(row[5], MC_GOLD, 8))
        self.beat(Create(frames), rt=0.5)
        eq = eq_line([("8", MC_GOLD), ("+", MC_GRAY), ("15", MC_AQUA), ("=", MC_GRAY), ("23", MC_YELLOW)], 40)
        eq.move_to([0, -1.0, 0])
        self.until(1.6)
        self.beat(FadeIn(eq, shift=UP * 0.2), rt=0.5)
        ret = chat("return [4, 5]", MC_GREEN, 60)
        ret.move_to([0, -2.6, 0])
        self.until(3.5)
        self.beat(FadeIn(ret, shift=UP * 0.2), Indicate(idx[4], color=MC_YELLOW), Indicate(idx[5], color=MC_YELLOW), rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("BRUTE FORCE", MC_RED)
        row = block_row(NUMS, 3.0, size=0.95, gap=0.2)
        idx = index_row(row, 30)
        code = code_panel(BRUTE_CODE, -3.7, max_h=2.9)
        pick = pickaxe(1.05).move_to([-2.4, 1.2, 0])
        dbg = Rectangle(width=1.2, height=0.16, fill_color="#000000", fill_opacity=1, stroke_width=0)
        dbg.next_to(pick, DOWN, buff=0.15)

        def dfill(frac):
            # Durability bar: shrinks and turns from green to red
            r = Rectangle(width=max(1.16 * frac, 0.02), height=0.1, stroke_width=0, fill_opacity=1,
                          fill_color=interpolate_color(ManimColor(MC_RED), ManimColor(MC_GREEN), frac))
            r.move_to(dbg.get_left() + RIGHT * (0.02 + max(1.16 * frac, 0.02) / 2))
            return r

        def counter(k):
            c = MT(f"checks {k}", 30, MC_WHITE, PIXEL)
            c.move_to([1.0, 1.2, 0])
            return c

        fill, cnt = dfill(1.0), counter(0)
        pairs = [(i, j) for i in range(len(NUMS)) for j in range(i + 1, len(NUMS))]

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in row], lag_ratio=0.1), rt=0.9)
        self.beat(FadeIn(idx), rt=0.3)
        self.until(1.6)
        self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
        self.until(2.7)
        self.beat(FadeIn(pick, scale=0.6), FadeIn(dbg), FadeIn(fill), FadeIn(cnt), rt=0.5)
        self.close_seg()

        oi = outline(row[0], MC_YELLOW, 7)
        oj = outline(row[1], MC_WHITE, 6)
        bar = line_bar(code, 1, 1, MC_YELLOW)

        def check(k, rt):
            i, j = pairs[k]
            nf, nc = dfill(1 - (k + 1) / 16), counter(k + 1)
            anims = [oj.animate.move_to(row[j]), Transform(fill, nf), Transform(cnt, nc),
                     Rotate(pick, angle=-25 * DEGREES, rate_func=there_and_back)]
            if k == 0 or pairs[k - 1][0] != i:
                anims.append(oi.animate.move_to(row[i]))
            self.beat(*anims, rt=rt)

        self.seg(4)
        self.until(0.3)
        self.beat(Create(oi), FadeIn(bar), rt=0.35)
        self.until(1.0)
        self.beat(FadeIn(oj), Transform(bar, line_bar(code, 2, 3, MC_YELLOW)), rt=0.25)
        for k in range(5):
            check(k, 0.45)
        self.close_seg()

        self.seg(5)
        for k in range(5, 15):
            check(k, 0.32)
        # The fifteenth check is the pair that works
        self.beat(oi.animate.set_stroke(MC_GREEN), oj.animate.set_stroke(MC_GREEN),
                  Transform(bar, line_bar(code, 4, 4, MC_GREEN)), rt=0.3)
        broken = MT("almost broken!", 34, MC_RED)
        broken.next_to(dbg, DOWN, buff=0.15)
        self.until(4.3)
        self.beat(Wiggle(pick), FadeIn(broken, shift=UP * 0.1), rt=0.8)
        self.close_seg()

        self.seg(6)
        self.beat(FadeOut(VGroup(row, idx, oi, oj, code, bar, pick, dbg, fill, cnt, broken)), rt=0.5)
        n = eq_line([("n =", MC_GRAY), ("1,000,000", MC_WHITE)], 32)
        n.move_to([0, 2.6, 0])
        self.beat(FadeIn(n, shift=UP * 0.2), rt=0.5)
        big = MT("500,000,000,000", 40, MC_RED, PIXEL)
        big.move_to([0, 1.0, 0])
        pl = MT("pairs", 52, MC_GRAY)
        pl.next_to(big, DOWN, buff=0.25)
        self.until(2.0)
        self.beat(FadeIn(big, scale=1.4), FadeIn(pl), rt=0.6)
        o = big_o_pow("n", 2, 72, MC_RED)
        o.move_to([0, -1.9, 0])
        self.until(3.2)
        self.beat(FadeIn(o, scale=0.5), rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        tsign = target_sign().move_to([0, 3.55, 0])
        bar = Hotbar(9)
        bar.move_to([0, -2.6, 0])
        items = VGroup(*[Block(v, f"{ORE_OF[v]}_ore", bar.s * 0.74, num_h=0.34).move_to(bar.slots[k]) for k, v in enumerate(NUMS)])
        sel = bar.selector(5)
        name = MT("Diamond Ore  15", 44, MC_WHITE)
        name.next_to(bar, UP, buff=0.3)
        eq = eq_line([("23", MC_YELLOW), ("-", MC_GRAY), ("15", MC_AQUA), ("=", MC_GRAY)], 46)
        q = MT("?", 46, MC_WHITE, PIXEL)
        eight = MT("8", 46, MC_GOLD, PIXEL)
        VGroup(eq, q).arrange(RIGHT, buff=0.35).move_to([0, 1.5, 0])
        eight.move_to(q)

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(bar), LaggedStart(*[FadeIn(b, scale=0.6) for b in items], lag_ratio=0.1),
                  rt=0.8)
        self.until(1.1)
        self.beat(FadeIn(tsign, scale=0.6), rt=0.5)
        self.until(2.8)
        self.beat(Create(sel), FadeIn(name, shift=UP * 0.1), items[5].animate.scale(1.15), rt=0.4)
        self.until(4.3)
        self.beat(FadeIn(eq, shift=UP * 0.2), FadeIn(q, shift=UP * 0.2), rt=0.5)
        self.until(6.1)
        self.beat(Transform(q, eight), ShowPassingFlash(outline(bar.slots[4], MC_GOLD, 10), time_width=0.6),
                  items[4].animate(rate_func=there_and_back).scale(1.25), rt=0.6)
        self.close_seg()

        self.seg(8)
        lab = MT("complement", 44, MC_GOLD)
        lab.next_to(q, DOWN, buff=0.3)
        self.until(0.2)
        self.beat(FadeIn(lab, shift=UP * 0.1), rt=0.4)
        f = eq_line([("need", MC_GOLD), ("=", MC_GRAY), ("target", MC_YELLOW), ("-", MC_GRAY), ("x", MC_AQUA)], 60, TERM, 0.25)
        f.move_to([0, -0.55, 0])
        self.until(1.6)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in f], lag_ratio=0.2), rt=0.9)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("ONE PASS", MC_GREEN)
        tsign = target_sign(0.6)
        tsign.move_to([0, TOP_Y - 0.05, 0]).to_edge(RIGHT, buff=0.4)
        inv = Inventory(len(NUMS), "Chest")
        inv.move_to([0, -1.0, 0])
        title2 = MT("Chest = hash map", 38, GUI_TITLE, TERM, shadow=False)
        title2.move_to(inv.title).align_to(inv.title, LEFT)
        code = code_panel(HASH_CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 2, 2, MC_YELLOW)
        slots_items = {}
        st = {"bar": None}

        ev = [(seg_time(W["first"], W[key]), key, None)
              for key in ("intro_row", "chest_in", "hashmap", "demo_cursor", "demo_ask", "index_four", "toast", "answer")]
        for k, s in enumerate(W["steps"]):
            for kind in ("visit", "need_t", "ask", "miss", "store", "hit"):
                if kind in s:
                    ev.append((seg_time(W["first"], s[kind]), kind, k))
        ev.sort(key=lambda e: e[0])

        def move_bar(line, color=MC_YELLOW, rt=0.15):
            self.beat(Transform(bar, line_bar(code, line, line, color)), rt=rt)

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(tsign), rt=0.35)

        def on(kind, k):
            if kind == "intro_row":
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
            elif kind == "chest_in":
                self.beat(FadeIn(inv, shift=UP * 0.3), rt=0.5)
            elif kind == "hashmap":
                self.beat(Transform(inv.title, title2), rt=0.4)
            elif kind == "demo_cursor":
                self.beat(FadeIn(bar), rt=0.3)
            elif kind == "demo_ask":
                move_bar(4, rt=0.3)
            elif kind == "visit":
                move_bar(2)
            elif kind == "need_t":
                move_bar(3)
            elif kind == "ask":
                move_bar(4)
            elif kind == "miss":
                move_bar(4, MC_RED)
            elif kind == "store":
                s = W["steps"][k]
                it = inv.item(k, s["x"], k)
                slots_items[k] = it
                self.beat(Transform(bar, line_bar(code, 6, 6, MC_YELLOW)), FadeIn(it, scale=1.6), rt=0.2)
            elif kind == "hit":
                fr = outline(inv.slots[W["steps"][k]["found"]], MC_GOLD, 9, buff=0.02)
                self.beat(Transform(bar, line_bar(code, 5, 5, MC_GREEN)), Create(fr), rt=0.3)
            elif kind == "index_four":
                self.beat(Indicate(slots_items[4][1], color=MC_YELLOW, scale_factor=1.9), rt=0.6)
            elif kind == "toast":
                t = toast("Advancement Made!", "Two Sum solved")
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(tsign), rt=0.5)
            elif kind == "answer":
                ans = chat("return [4, 5]", MC_GREEN, 60)
                ans.move_to([0, 4.3, 0])
                self.beat(FadeIn(ans, shift=UP * 0.2), rt=0.4)

        def on_last():
            # The 3D clip fades to sky at its end; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        look = VGroup(pixel_art("chest_front", 0.9), MT("lookup", 52, MC_WHITE), MT("O(1)", 40, MC_GREEN, PIXEL))
        look.arrange(RIGHT, buff=0.35).move_to([0, 3.4, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), MT("O(n)", 64, MC_GREEN, PIXEL)).arrange(RIGHT, buff=0.4)
        tm.move_to([0, 1.65, 0])
        bg = Rectangle(width=7.0, height=0.3, fill_color="#1B1B1B", fill_opacity=1, stroke_color="#000000", stroke_width=4)
        bg.move_to([0, 0.6, 0])
        ticks = VGroup(*[Line([bg.get_left()[0] + 7.0 * k / 16, 0.45, 0], [bg.get_left()[0] + 7.0 * k / 16, 0.75, 0],
                              color="#000000", stroke_width=3) for k in range(1, 16)])
        xp = Rectangle(width=6.92, height=0.2, fill_color="#80FF20", fill_opacity=1, stroke_width=0)
        xp.move_to(bg)
        xp0 = xp.copy().stretch_to_fit_width(0.02).align_to(bg, LEFT).shift(RIGHT * 0.04)

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(0.5)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in look], lag_ratio=0.25), rt=0.8)
        self.until(2.4)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), FadeIn(ticks), rt=0.4)
        self.add(xp0)
        self.beat(Transform(xp0, xp), rt=1.2)
        self.close_seg()

        self.seg(17)
        old = big_o_pow("n", 2, 44, MC_RED)
        arrow = MT("->", 70, MC_GRAY)
        new = MT("O(n)", 44, MC_GREEN, PIXEL)
        cmp = VGroup(old, arrow, new).arrange(RIGHT, buff=0.45)
        cmp.move_to([0, -1.25, 0])
        strike = Line(old.get_left() + LEFT * 0.1, old.get_right() + RIGHT * 0.1, color=MC_RED, stroke_width=8)
        self.until(0.2)
        self.beat(FadeIn(old, shift=UP * 0.15), rt=0.4)
        self.until(1.2)
        self.beat(Create(strike), FadeIn(arrow), FadeIn(new, shift=LEFT * 0.2), rt=0.6)
        mem = VGroup(pixel_art("chest_front", 0.85), MT("memory", 52, MC_WHITE), MT("O(n)", 40, MC_GOLD, PIXEL))
        mem.arrange(RIGHT, buff=0.35).move_to([0, -3.1, 0])
        self.until(2.6)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in mem], lag_ratio=0.2), rt=0.7)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(HASH_CODE, 1.6, width=8.4)
        bar = line_bar(code, 2, 2, MC_YELLOW)
        icon = pixel_art("chest_front", 0.55)

        self.seg(18)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(1.2)
        icon.next_to(code.code_lines[1], RIGHT, buff=0.4)
        self.beat(Transform(bar, line_bar(code, 1, 1, MC_GOLD)), FadeIn(icon, scale=0.5), rt=0.35)
        self.until(2.4)
        self.beat(Transform(bar, line_bar(code, 0, 6, MC_GREEN)), rt=0.4)
        self.close_seg()

        self.seg(19)
        msg = chat("Trade memory for speed", MC_GOLD, 60)
        msg.move_to([0, -2.3, 0])
        self.until(0.1)
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.5)
        self.until(2.2)
        self.beat(FadeOut(Group(code, bar, icon, msg)), rt=0.5)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=1.0)
        self.close_seg()
