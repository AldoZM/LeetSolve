WALK = json.load(open('walk.json', encoding='utf-8'))
NUMS, ANSWER = WALK["nums"], WALK["answer"]
ORE_OF.update(dict(zip(NUMS, WALK["ores"])))

SOLVE_CODE = """def sortableIntegers(nums):
    n, total = len(nums), 0
    for k in range(1, n + 1):
        if n % k: continue
        prev, ok = 0, True
        for s in range(0, n, k):
            b = nums[s:s + k]
            d = [i for i in range(k) if b[i] > b[(i+1) % k]]
            lo = b[(d[0] + 1) % k] if d else b[0]
            ok = ok and len(d) <= 1 and lo >= prev
            prev = b[d[0]] if d else b[0]
        total += k if ok else 0
    return total"""


def ph(i, phrase, shift=0.0):
    # Seconds into line i where `phrase` starts being spoken (even speaking rate inside a line)
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase)
    return max(0.0, min(dur - 0.25, dur * k / len(text) + shift))


def index_row(row, size=34, color=MC_GRAY, buff=0.14):
    return VGroup(*[MT(str(k), size, color).next_to(b, DOWN, buff=buff) for k, b in enumerate(row)])


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def pulse(m, s=1.15):
    # Pixel art is highlighted with a scale pulse; Indicate with a color paints it flat
    return m.animate(rate_func=there_and_back).scale(s)


def eq_line(parts, size=34, font=PIXEL, buff=0.3):
    return VGroup(*[MT(s, size, c, font) for s, c in parts]).arrange(RIGHT, buff=buff)


def cut(row, k, gap=0.4):
    # Animations that open gaps between the pieces of size k (centered again)
    n = len(row)
    step = 1.05 + 0.18  # block size plus gap, as in block_row
    anims = []
    for i, b in enumerate(row):
        x = (i - (n - 1) / 2) * step + (i // k - (n // k - 1) / 2) * gap
        anims.append(b.animate.set_x(x))
    return anims


def circle_piece(values, center, r=1.0, size=0.7):
    # A piece drawn as a circle: blocks clockwise from the top, a ring behind them
    k = len(values)
    pos = [center + r * np.array([np.sin(2 * np.pi * j / k), np.cos(2 * np.pi * j / k), 0]) for j in range(k)]
    ring = Circle(radius=r, color=MC_GRAY, stroke_width=6).move_to(center)
    blocks = VGroup(*[Block(v, f"{ORE_OF[v]}_ore", size).move_to(p) for v, p in zip(values, pos)])
    return ring, blocks, pos


def drop_marks(values, pos, center, r=1.0):
    # A red mark on the ring between each block and the next one when it drops
    k = len(values)
    marks = VGroup()
    for j in range(k):
        if values[j] > values[(j + 1) % k]:
            a = 2 * np.pi * (j + 0.5) / k
            m = MT("v", 40, MC_RED, PIXEL).move_to(center + (r + 0.05) * np.array([np.sin(a), np.cos(a), 0]))
            marks.add(m)
    return marks


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    title = stone_title("SORTABLE K", 60, width=7.8).move_to([0, 4.0, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.25, 2.75, 0])
    row = block_row(NUMS, 0.95, size=1.05, gap=0.18)
    idx = index_row(row)
    pick = pickaxe(1.25).move_to([-1.3, -1.2, 0])
    chest = chest_icon(1.15).move_to([1.3, -1.2, 0])
    tags = VGroup(chat("LeetCode #3886", MC_AQUA, 46), chat("Hard", MC_RED, 46), chat("Rotation", MC_GREEN, 46))
    tags.arrange(RIGHT, buff=0.2)
    if tags.width > 8.4:
        tags.scale_to_fit_width(8.4)
    tags.move_to([0, -3.05, 0])
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, title, spl, row, idx, pick, chest, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, title, spl, row, idx, pick, chest, tags = art
        self.add(art)

        self.seg(0)
        self.beat(pulse(spl), rt=0.8)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.35) for b in row], lag_ratio=0.18), rt=1.6)
        self.sfx("stone_dig1", 0.35, delay=0.35)
        self.until(ph(0, "LeetCode"))
        self.sfx("click", 0.35)
        self.beat(pulse(VGroup(*row[3:]), 1.08), rt=0.8)
        self.until(ph(0, "and a tricky"))
        self.beat(pulse(spl), Rotate(pick, angle=-30 * DEGREES, rate_func=there_and_back), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        row = block_row(NUMS, 2.6, size=1.05, gap=0.18)
        lab = MT("nums", 40, MC_WHITE).next_to(row, UP, buff=0.2).align_to(row, LEFT)
        divs = chat("k = 1, 2, 3, 6", MC_GOLD, 44)
        divs.move_to([0, 0.9, 0])

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(len(row)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.3, delay=k * 0.12 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.12), rt=1.6)
        self.beat(FadeIn(lab), rt=0.3)
        self.until(ph(1, "We pick"))
        self.beat(FadeIn(divs, shift=UP * 0.15), rt=0.5)
        self.until(ph(1, "cut the row"))
        self.sfx("stone_step1", 0.3)
        self.beat(*cut(row, 3), FadeOut(lab), rt=0.6)
        self.close_seg()

        # A piece spins like a carousel: 3 4 3 turns into 3 3 4
        self.seg(2)
        piece = [row[3], row[4], row[5]]
        self.until(ph(2, "spin like a carousel"))
        self.sfx("stone_step2", 0.3, delay=0.3)
        self.beat(piece[2].animate(path_arc=-200 * DEGREES).move_to(piece[0]), piece[0].animate.move_to(piece[1]),
                  piece[1].animate.move_to(piece[2]), rt=0.8)
        ok = SurroundingRectangle(row, color=MC_GREEN, buff=0.12, stroke_width=7)
        self.until(ph(2, "whole row ends up sorted"))
        self.sfx("orb", 0.3)
        self.beat(Create(ok), rt=0.5)
        self.close_seg()

        self.seg(3)
        s = chat("sum of every k that works", MC_GOLD, 40)
        s.move_to([0, -0.4, 0])
        self.until(ph(3, "Return the sum"))
        self.beat(FadeIn(s, shift=UP * 0.15), rt=0.4)
        two = eq_line([("2", MC_GREEN), ("+", MC_GRAY), ("3", MC_GREEN), ("=", MC_GRAY), ("5", MC_GOLD)], 48)
        two.move_to([0, -1.6, 0])
        self.until(ph(3, "sizes two and three"))
        self.beat(FadeIn(two, shift=UP * 0.15), rt=0.5)
        ans = chat(f"return {ANSWER}", MC_GREEN, 60)
        ans.move_to([0, -3.0, 0])
        self.until(ph(3, "the answer is five", -0.2))
        self.sfx("pop", 0.35)
        self.beat(FadeIn(ans, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("BRUTE FORCE", MC_RED)
        piece = [3, 4, 3]
        turns = VGroup()
        for r in range(3):
            t = block_row(piece[r:] + piece[:r], 0, size=0.75, gap=0.1)
            turns.add(t)
        turns.arrange(DOWN, buff=0.3).move_to([-1.3, 1.9, 0])
        marks = VGroup()
        for r, t in enumerate(turns):
            vals = piece[r:] + piece[:r]
            good = vals == sorted(vals)
            m = MT("ok" if good else "no", 34, MC_GREEN if good else MC_RED, PIXEL).next_to(t, RIGHT, buff=0.4)
            marks.add(m)
        pick = pickaxe(1.0).move_to([2.7, 1.9, 0])

        self.seg(4)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(pick, scale=0.6), rt=0.5)
        self.until(ph(4, "spin every piece"))
        for r in range(3):
            self.sfx(f"stone_step{r + 1}", 0.28)
            self.beat(FadeIn(turns[r], shift=RIGHT * 0.2), FadeIn(marks[r]), rt=0.35)
        self.close_seg()

        self.seg(5)
        e1 = eq_line([("k", MC_WHITE), ("turns", MC_GRAY)], 44, TERM, 0.25)
        e2 = eq_line([("x  k", MC_WHITE), ("steps each", MC_GRAY)], 44, TERM, 0.25)
        VGroup(e1, e2).arrange(DOWN, buff=0.2).move_to([0, -0.6, 0])
        self.until(ph(5, "has k turns"))
        self.beat(FadeIn(e1, shift=UP * 0.15), rt=0.4)
        self.until(ph(5, "takes k steps"))
        self.beat(FadeIn(e2, shift=UP * 0.15), rt=0.4)
        self.close_seg()

        self.seg(6)
        o = big_o_pow("n", 2, 64, MC_RED)
        o.move_to([0, -2.3, 0])
        self.until(ph(6, "k as big as n"))
        self.beat(FadeIn(o, scale=0.5), rt=0.5)
        big = MT("10,000,000,000", 40, MC_RED, PIXEL)
        big.move_to([0, -3.4, 0])
        self.until(ph(6, "ten billion", -0.2))
        self.beat(FadeIn(big, scale=1.3), rt=0.4)
        broken = MT("broken!", 34, MC_RED)
        broken.next_to(pick, DOWN, buff=0.15)
        self.until(ph(6, "and the pickaxe", -0.1))
        self.sfx("break", 0.45)
        self.beat(Wiggle(pick), FadeIn(broken, shift=UP * 0.1), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        c1, c2 = np.array([-2.0, 2.0, 0]), np.array([2.0, 2.0, 0])
        good, bad = [3, 4, 3], [1, 3, 2, 4]
        r1, b1, p1 = circle_piece(good, c1)
        r2, b2, p2 = circle_piece(bad, c2)
        m1, m2 = drop_marks(good, p1, c1), drop_marks(bad, p2, c2)
        l1 = chat("1 drop: spins", MC_GREEN, 36).next_to(r1, DOWN, buff=0.45)
        l2 = chat("2 drops: never", MC_RED, 36).next_to(r2, DOWN, buff=0.45)

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        # Rings go in before the blocks so they stay behind them
        self.add(r1, b1)
        self.beat(Create(r1), LaggedStart(*[FadeIn(b, scale=0.6) for b in b1], lag_ratio=0.15), rt=0.7)
        self.until(ph(7, "count the drops"))
        self.sfx("villager_no1", 0.22)
        self.beat(FadeIn(m1, scale=1.4), rt=0.4)
        self.close_seg()

        self.seg(8)
        self.until(ph(8, "at most one drop"))
        self.beat(FadeIn(l1, shift=UP * 0.1), rt=0.4)
        self.add(r2, b2)
        self.until(ph(8, "counting the wrap"))
        self.beat(Create(r2), LaggedStart(*[FadeIn(b, scale=0.6) for b in b2], lag_ratio=0.12), rt=0.6)
        self.sfx("villager_no2", 0.22)
        self.beat(FadeIn(m2, scale=1.4), FadeIn(l2, shift=UP * 0.1), rt=0.4)
        self.close_seg()

        # Pieces chain: each one starts at or above where the last one ended
        self.seg(9)
        self.beat(FadeOut(VGroup(r1, b1, m1, l1, r2, b2, m2, l2)), rt=0.4)
        pa = block_row([1, 2, 3], 0, size=0.85, gap=0.12)
        pb = block_row([3, 3, 4], 0, size=0.85, gap=0.12)
        VGroup(pa, pb).arrange(RIGHT, buff=0.7).move_to([0, 1.6, 0])
        mx = chat("max 3", MC_AQUA, 34).next_to(pa, DOWN, buff=0.3)
        mn = chat("min 3", MC_AQUA, 34).next_to(pb, DOWN, buff=0.3)
        rule = chat("next min  >=  last max", MC_GOLD, 44)
        rule.move_to([0, -0.9, 0])
        self.beat(FadeIn(pa, shift=UP * 0.15), FadeIn(pb, shift=UP * 0.15), rt=0.5)
        self.until(ph(9, "smallest and largest"))
        self.beat(FadeIn(mx), FadeIn(mn), rt=0.4)
        self.until(ph(9, "every piece must start", -0.2))
        self.sfx("pop", 0.35)
        self.beat(FadeIn(rule, shift=UP * 0.15), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("SPIN TEST", MC_GREEN)
        code = code_panel(SOLVE_CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 2, 2, MC_YELLOW)
        st = {"ro": None}

        def show(text, color):
            g = chat(text, color, 40)
            g.move_to([0, -1.15, 0])
            old = st["ro"]
            st["ro"] = g
            self.beat(*([FadeOut(old)] if old is not None else []), FadeIn(g, shift=UP * 0.15), rt=0.3)

        def move_bar(a, b=None, color=MC_YELLOW, rt=0.15):
            self.beat(Transform(bar, line_bar(code, a, a if b is None else b, color)), rt=rt)

        ev = [(seg_time(W["first"], a[0]), "size", a[1]) for a in W["arrangements"]]
        ev += [(seg_time(W["first"], m[0]), "mark", None) for m in W["marks"]]
        ev += [(seg_time(W["first"], v[1]), "verdict", j) for j, v in enumerate(W["verdicts"])]
        ev += [(seg_time(W["first"], W[k]), k, None) for k in ("chain", "toast", "sum_t")]
        ev.sort(key=lambda e: e[0])
        sums = {1: "sum 0", 2: "sum 2", 3: "sum 2 + 3", 6: "sum 5"}
        seen = set()

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(code, shift=UP * 0.3), FadeIn(bar), rt=0.5)

        def on(kind, k):
            if kind == "size":
                if k in seen:
                    # The same size again: the pieces spin
                    self.sfx("stone_step3", 0.3, delay=0.3)
                    move_bar(8)
                    return
                seen.add(k)
                self.sfx("stone_step1", 0.3)
                move_bar(2)
                show(f"k = {k}", MC_WHITE)
            elif kind == "mark":
                self.sfx("villager_no3", 0.2)
                move_bar(7)
            elif kind == "chain":
                move_bar(9)
            elif kind == "verdict":
                kk, _, ok = W["verdicts"][k]
                self.sfx("orb" if ok else "villager_no1", 0.3)
                move_bar(11, color=MC_GREEN if ok else MC_RED)
                show(f"k = {kk}  {'works' if ok else 'fails'}   {sums[kk] if ok else ''}".rstrip(), MC_GREEN if ok else MC_RED)
            elif kind == "toast":
                t = toast("Advancement Made!", "Sizes summed", w=4.6)
                t.move_to([0, 5.5, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                self.beat(t.animate.shift(LEFT * 7), Transform(bar, line_bar(code, 12, 12, MC_GREEN)), rt=0.5)
            elif kind == "sum_t":
                ans = chat(f"return {ANSWER}", MC_GREEN, 60)
                ans.move_to([0, -1.15, 0])
                self.beat(FadeOut(st["ro"]), FadeIn(ans, shift=UP * 0.2), rt=0.4)

        def on_last():
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        per = MT("each size walks the row once", 44, MC_WHITE)
        per.move_to([0, 3.4, 0])
        tm = VGroup(MT("per size", 52, MC_GRAY), level_text("O(n)", 1.05)).arrange(RIGHT, buff=0.4)
        tm.move_to([0, 1.65, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.6, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(ph(16, "walks the row", -0.3))
        self.beat(FadeIn(per, shift=UP * 0.15), rt=0.5)
        self.until(ph(16, "linear", -0.5))
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.35)
        self.add(xp)
        self.sfx("levelup", 0.3, delay=0.3)
        self.beat(Restore(xp), rt=0.5)
        self.close_seg()

        self.seg(17)
        divs = chat("at most 128 divisors", MC_GOLD, 44)
        divs.move_to([0, -1.4, 0])
        self.until(ph(17, "at most", -0.3))
        self.sfx("click", 0.3)
        self.beat(FadeIn(divs, shift=UP * 0.15), rt=0.4)
        tot = VGroup(MT("total", 52, MC_GRAY), MT("O(n x d)", 48, MC_GREEN, PIXEL)).arrange(RIGHT, buff=0.4)
        tot.move_to([0, -3.0, 0])
        self.until(ph(17, "stays small", -0.5))
        self.sfx("pop", 0.35)
        self.beat(FadeIn(tot, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(SOLVE_CODE, 1.6, width=8.4)
        bar = line_bar(code, 2, 2, MC_YELLOW)

        self.seg(18)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.06), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(ph(18, "count the drops"))
        self.beat(Transform(bar, line_bar(code, 7, 7, MC_GOLD)), rt=0.3)
        self.until(ph(18, "chain the pieces"))
        self.beat(Transform(bar, line_bar(code, 8, 10, MC_GREEN)), rt=0.3)
        self.close_seg()

        self.seg(19)
        msg = chat("One drop, one spin", MC_GOLD, 56)
        msg.move_to([0, -3.0, 0])
        self.until(ph(19, "A circle sorts"))
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.5)
        # The lesson stays until the cover replaces it, so the screen is never empty; the cover is the first frame too
        self.finish(FadeOut(Group(code, bar, msg)), FadeIn(cover()), rt=1.0)
        self.close_seg()
