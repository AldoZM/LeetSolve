WALK = json.load(open('walk.json', encoding='utf-8'))
L1, L2, RESULT = WALK["l1"], WALK["l2"], WALK["result"]
STEPS = WALK["steps"]
MC_BLUE = "#5577FF"
WOOD = "#9C7A48"
NULL_EDGE = "#5A2A2A"
ORE = {"l1": "diamond_ore", "l2": "lapis_ore", "sum": "emerald_ore"}

ADD_CODE = """def addTwoNumbers(l1, l2):
    dummy = tail = ListNode()
    carry = 0
    while l1 or l2 or carry:
        a = l1.val if l1 else 0
        b = l2.val if l2 else 0
        carry, digit = divmod(a + b + carry, 10)
        tail.next = ListNode(digit)
        tail = tail.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next"""


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


class Chain2D(VGroup):
    """A linked list: ore blocks joined by wooden rods (next pointers), with a barrier as the null at the end."""

    def __init__(self, values, tex, y, size=0.95, step=1.4, x0=-2.8, null=True, **kwargs):
        super().__init__(**kwargs)
        xs = [x0 + k * step for k in range(len(values) + 1)]
        self.blocks = VGroup(*[Block(v, tex, size).move_to([xs[k], y, 0]) for k, v in enumerate(values)])
        self.rods = VGroup(*[Line([xs[k] + size / 2, y, 0], [xs[k + 1] - size / 2, y, 0], color=WOOD, stroke_width=11 * size)
                             for k in range(len(values) - 1)])
        self.null = VGroup()
        if null:
            bar = pixel_art("barrier", size * 0.62).move_to([xs[-1], y, 0])
            rod = Line([xs[-2] + size / 2, y, 0], [xs[-1] - size * 0.31, y, 0], color=NULL_EDGE, stroke_width=8 * size)
            self.null = VGroup(rod, bar)
        # Rods first, so the blocks are drawn on top of them
        self.add(self.rods, self.null, self.blocks)


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("ADD TWO", width=5.6).move_to([0, 4.85, 0])
    t2 = stone_title("NUMBERS", width=6.4).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    c1 = Chain2D(L1, ORE["l1"], 1.75, size=0.8, step=1.25, x0=-2.5)
    c2 = Chain2D(L2, ORE["l2"], 0.55, size=0.8, step=1.25, x0=-2.5)
    plus = MT("+", 60, MC_WHITE, PIXEL).move_to([-3.75, 0.55, 0])
    rule = Rectangle(width=7.4, height=0.07, fill_color=MC_WHITE, fill_opacity=0.85, stroke_width=0).move_to([0, -0.2, 0])
    c3 = Chain2D(RESULT, ORE["sum"], -1.0, size=0.8, step=1.25, x0=-2.5, null=False)
    tags = VGroup(chat("LeetCode #2", MC_AQUA, 46), chat("Medium", MC_GOLD, 46), chat("Linked List", MC_GREEN, 46))
    tags.arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, c1, c2, plus, rule, c3, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, c1, c2, plus, rule, c3, tags = art
        self.add(art)

        self.seg(0)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        # Both chains hop from the ones digit onward, then the sum answers column by column
        self.sfx("stone_dig1", 0.3, delay=0.3)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.3) for b in [*c1.blocks, *c2.blocks]],
                              lag_ratio=0.15), rt=1.6)
        self.sfx("orb", 0.3, delay=0.2)
        self.beat(LaggedStart(*[pulse(b, 1.2) for b in c3.blocks], lag_ratio=0.2), rt=1.4)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        c1 = Chain2D(L1, ORE["l1"], 3.3)
        c2 = Chain2D(L2, ORE["l2"], 1.9)
        n1 = MT("l1", 36, MC_AQUA).next_to(c1.blocks[0], LEFT, buff=0.18)
        n2 = MT("l2", 36, MC_BLUE).next_to(c2.blocks[0], LEFT, buff=0.18)
        nxt = MT("next", 30, MC_YELLOW).next_to(c1.rods[0], DOWN, buff=0.12)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        # The blocks fall from the sky, l1 first and then l2
        blocks = [*c1.blocks, *c2.blocks]
        for b in blocks:
            b.shift(UP * 8)
        self.add(*blocks)
        for k in range(len(blocks)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.3, delay=k * 0.12 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in blocks],
                              lag_ratio=0.12), rt=1.7)
        self.beat(FadeIn(n1), FadeIn(n2), rt=0.3)
        self.until(at(1, "points"))
        # Rods behind the blocks: added first, then the blocks again on top
        self.add(c1.rods, c1.null, c2.rods, c2.null, *blocks)
        self.sfx("wood_dig1", 0.35)
        self.beat(Create(c1.rods), Create(c2.rods), FadeIn(c1.null), FadeIn(c2.null), FadeIn(nxt, shift=UP * 0.1), rt=0.6)
        self.close_seg()

        places = ["ones", "tens", "hund.", "thou."]
        labels = VGroup(*[MT(p, 36, MC_YELLOW if k == 0 else MC_GRAY).move_to([-2.8 + 1.4 * k, 4.3, 0])
                          for k, p in enumerate(places)])
        firsts = VGroup(outline(c1.blocks[0], MC_YELLOW, 8), outline(c2.blocks[0], MC_YELLOW, 8))

        self.seg(2)
        self.beat(FadeOut(nxt), rt=0.3)
        self.until(at(2, "reverse"))
        self.beat(LaggedStart(*[FadeIn(p, shift=DOWN * 0.15) for p in labels], lag_ratio=0.25), rt=1.0)
        self.until(at(2, "ones digit"))
        self.sfx("click", 0.3)
        self.beat(Create(firsts), pulse(c1.blocks[0]), pulse(c2.blocks[0]), rt=0.5)
        self.close_seg()

        def reading(values, color, name, y):
            lab = MT(f"{name} =", 44, color)
            digs = VGroup(*[MT(str(v), 60, color, PIXEL) for v in reversed(values)]).arrange(RIGHT, buff=0.12)
            VGroup(lab, digs).arrange(RIGHT, buff=0.4).move_to([0, y, 0])
            return lab, digs

        lab1, digs1 = reading(L1, MC_AQUA, "l1", 0.35)
        lab2, digs2 = reading(L2, MC_BLUE, "l2", -0.95)

        self.seg(3)
        self.beat(FadeOut(firsts), FadeIn(lab1), rt=0.3)
        # Read from the last block back to the first: the number shows up from its ones digit
        self.until(at(3, "nine hundred") - 0.3)
        self.beat(LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in reversed(digs1)], lag_ratio=0.35), rt=1.0)
        self.until(at(3, "nine thousand") - 0.4)
        self.beat(FadeIn(lab2), rt=0.3)
        self.beat(LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in reversed(digs2)], lag_ratio=0.3), rt=1.2)
        self.close_seg()

        eq = eq_line([("942", MC_AQUA), ("+", MC_GRAY), ("9465", MC_BLUE), ("=", MC_GRAY), ("10407", MC_GREEN)], 38, buff=0.25)
        eq.move_to([0, -2.3, 0])
        c3 = Chain2D(RESULT, ORE["sum"], -3.9, null=False)
        n3 = MT("sum", 36, MC_GREEN).next_to(c3.blocks[0], LEFT, buff=0.18)

        self.seg(4)
        self.beat(FadeIn(eq, shift=UP * 0.2), rt=0.5)
        self.until(at(4, "new chain") - 0.2)
        self.add(c3.rods, c3.blocks)
        for k in range(len(RESULT)):
            self.sfx("pop", 0.3, delay=0.12 * k + 0.1)
        self.beat(FadeIn(n3), LaggedStart(*[FadeIn(b, scale=0.5) for b in c3.blocks], lag_ratio=0.15), Create(c3.rods), rt=1.0)
        self.clear_all()
        self.close_seg()


class Scene3_Shortcut(Base):
    def construct(self):
        h = hdr("SHORTCUT?", MC_RED)
        code = chat("int(l1) + int(l2)", MC_WHITE, 60).move_to([0, 3.4, 0])
        eq = eq_line([("942", MC_AQUA), ("+", MC_GRAY), ("9465", MC_BLUE), ("=", MC_GRAY), ("10407", MC_GREEN)], 38, buff=0.25)
        eq.move_to([0, 1.9, 0])
        ok = MT("works for small numbers", 42, MC_GREEN).move_to([0, 0.8, 0])

        self.seg(5)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(at(5, "turn both") - 0.2)
        self.sfx("book_flip1", 0.35)
        self.beat(FadeIn(code, shift=UP * 0.2), rt=0.5)
        self.until(at(5, "just add"))
        self.beat(FadeIn(eq, shift=UP * 0.2), rt=0.5)
        self.beat(FadeIn(ok, shift=UP * 0.15), rt=0.4)
        self.close_seg()

        # One chain of a hundred digits: a 10 x 10 grid of digit cells
        cs, gap = 0.5, 0.08
        cells = VGroup(*[Rectangle(width=cs, height=cs, fill_color="#2E3A66", fill_opacity=0.9, stroke_color="#000000",
                                   stroke_width=2).move_to([(c - 4.5) * (cs + gap), -0.6 - (r - 4.5) * (cs + gap), 0])
                         for r in range(10) for c in range(10)])
        cap = MT("one chain, 100 digits", 40, MC_AQUA).move_to([0, 2.75, 0])
        fits, spill = cells[:19], cells[19:]
        fit_lab = MT("a 64-bit integer holds 19", 34, MC_GREEN).move_to([0, -3.95, 0])
        stamp = MT("OVERFLOW!", 64, MC_RED, PIXEL).move_to([0, -4.95, 0])

        self.seg(6)
        self.beat(FadeOut(VGroup(code, eq, ok), shift=UP * 0.3), FadeIn(cap), rt=0.4)
        self.beat(LaggedStart(*[FadeIn(c, scale=0.6) for c in cells], lag_ratio=0.01), rt=1.1)
        self.until(at(6, "overflows") - 0.9)
        self.beat(*[c.animate.set_fill("#2E8B3A") for c in fits], FadeIn(fit_lab, shift=UP * 0.15), rt=0.5)
        self.until(at(6, "overflows"))
        self.sfx("villager_no2", 0.4)
        self.beat(LaggedStart(*[c.animate.set_fill("#A02828") for c in spill], lag_ratio=0.008), FadeIn(stamp, scale=1.4), rt=0.8)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        xs = [2.4, 1.3, 0.2, -0.9, -2.0]  # column x by place: ones, tens, ...
        Y_C, Y_A, Y_B, Y_L, Y_R = 4.15, 3.2, 2.05, 1.4, 0.75
        top = VGroup(*[MT(str(d), 64, MC_AQUA, PIXEL).move_to([xs[k], Y_A, 0]) for k, d in enumerate(L1)])
        bot = VGroup(*[MT(str(d), 64, MC_BLUE, PIXEL).move_to([xs[k], Y_B, 0]) for k, d in enumerate(L2)])
        plus = MT("+", 64, MC_GRAY, PIXEL).move_to([-3.2, Y_B, 0])
        rule = Rectangle(width=6.8, height=0.08, fill_color=MC_WHITE, fill_opacity=0.85, stroke_width=0).move_to([-0.3, Y_L, 0])
        beam = Rectangle(width=0.95, height=Y_C - Y_R + 0.95, stroke_color=MC_YELLOW, stroke_width=6, fill_color=MC_YELLOW,
                         fill_opacity=0.12).move_to([xs[0], (Y_C + Y_R) / 2, 0])
        arrow = Arrow([3.4, -0.45, 0], [-2.6, -0.45, 0], buff=0, color=MC_YELLOW, stroke_width=8)
        start = MT("start at the ones place", 36, MC_YELLOW).move_to([0, -1.05, 0])
        mini = Chain2D(L1, ORE["l1"], -2.5, size=0.8, step=1.25, x0=-1.9)
        mini_first = outline(mini.blocks[0], MC_YELLOW, 8)
        mini_cap = MT("the chain starts there too", 34, MC_GRAY).move_to([0, -3.6, 0])

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(at(7, "Reverse"))
        self.beat(LaggedStart(*[FadeIn(m, shift=DOWN * 0.2) for m in [*reversed(top), plus, *reversed(bot)]], lag_ratio=0.08),
                  FadeIn(rule), rt=1.0)
        self.until(at(7, "starting"))
        self.sfx("click", 0.3)
        self.beat(GrowArrow(arrow), FadeIn(start), FadeIn(beam), rt=0.6)
        self.beat(FadeIn(mini, shift=UP * 0.2), rt=0.4)
        self.beat(Create(mini_first), FadeIn(mini_cap), rt=0.4)
        self.close_seg()

        self.seg(8)
        self.beat(FadeOut(VGroup(arrow, start, mini, mini_first, mini_cap)), rt=0.35)
        for s in STEPS:
            k = s["k"]
            anims = [beam.animate.move_to([xs[k], (Y_C + Y_R) / 2, 0])] if k else []
            digit = MT(str(s["digit"]), 64, MC_GREEN, PIXEL).move_to([xs[k], Y_R, 0])
            self.sfx("pop", 0.3, delay=0.25)
            self.beat(*anims, FadeIn(digit, shift=DOWN * 0.3), rt=0.45)
            if s["cout"]:
                c = MT("1", 40, MC_GOLD, PIXEL).move_to([xs[k + 1], Y_C, 0])
                self.sfx("orb", 0.28)
                self.beat(FadeIn(c, shift=UP * 0.3, scale=0.5), rt=0.3)
            else:
                self.hold(0.3)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("ADD COLUMNS", MC_GREEN)
        code = code_panel(ADD_CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 3, 3, MC_YELLOW)
        st = {"badge": None, "ro": None}

        def badge(v):
            return chat(f"carry {v}", MC_GOLD if v else MC_GRAY, 42).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)

        def readout(s):
            a = "0" if s["a"] is None else str(s["a"])
            b = "0" if s["b"] is None else str(s["b"])
            return eq_line([(a, MC_GRAY if s["a"] is None else MC_AQUA), ("+", MC_GRAY), (b, MC_GRAY if s["b"] is None else MC_BLUE),
                            ("+", MC_GRAY), (str(s["cin"]), MC_GOLD), ("=", MC_GRAY), (str(s["total"]), MC_WHITE)], 50, buff=0.28
                           ).move_to([0, -1.0, 0])

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("rows_in", "cursor", "hold", "run_out", "toast", "number")]
        ev += [(seg_time(W["first"], spec), "read", k) for k, spec in enumerate(W["read"])]
        for k, s in enumerate(STEPS):
            ev.append((seg_time(W["first"], s["visit"]), "visit", k))
            ev.append((seg_time(W["first"], s["visit"]) + 0.45, "ab", k))
            for kind in ("sum", "place", "carry"):
                if kind in s:
                    ev.append((seg_time(W["first"], s[kind]), kind, k))
        ev.sort(key=lambda e: e[0])
        chain = VGroup()
        for k, d in enumerate(RESULT):
            chain.add(MT(str(d), 56, MC_GREEN, PIXEL))
            if k < len(RESULT) - 1:
                chain.add(MT("->", 44, MC_GRAY))
        chain.arrange(RIGHT, buff=0.22).move_to([0, -1.0, 0])

        def move_bar(k0, k1=None, color=MC_YELLOW, rt=0.15):
            self.beat(Transform(bar, line_bar(code, k0, k1, color)), rt=rt)

        def swap_ro(new, rt=0.25):
            anims = [FadeIn(new, scale=1.15)] if new is not None else []
            if st["ro"] is not None:
                anims.append(FadeOut(st["ro"]))
            st["ro"] = new
            self.beat(*anims, rt=rt)

        def on_first():
            st["badge"] = badge(0)
            self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.35)

        def on(kind, k):
            if kind == "rows_in":
                # The 3D chains drop in one block after another
                for i in range(len(L1) + len(L2)):
                    self.sfx(f"stone_dig{i % 4 + 1}", 0.28, delay=0.35 + 0.12 * (i % 4) + (0.45 if i >= len(L1) else 0))
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.5)
            elif kind == "cursor":
                self.beat(FadeIn(bar), rt=0.3)
            elif kind == "hold":
                self.sfx("orb", 0.25)
                self.beat(FadeIn(st["badge"], shift=LEFT * 0.2), rt=0.4)
            elif kind == "visit":
                self.sfx("click", 0.25)
                move_bar(3)
                if st["ro"] is not None:
                    swap_ro(None, rt=0.2)
            elif kind == "ab":
                move_bar(4, 5)
            elif kind == "run_out":
                swap_ro(MT("l1 ran out: 0", 46, MC_GRAY).move_to([0, -1.0, 0]), rt=0.3)
            elif kind == "sum":
                s = STEPS[k]
                move_bar(6, rt=0.12)
                swap_ro(readout(s), rt=0.25)
                if s["cin"] and not s["cout"]:
                    new = badge(0)
                    self.beat(Transform(st["badge"], new), rt=0.2)
            elif kind == "place":
                self.sfx(f"stone_dig{k % 4 + 1}", 0.38, delay=0.3)
                move_bar(7, 8, MC_GREEN, rt=0.12)
            elif kind == "carry":
                self.sfx("orb", 0.32)
                self.beat(Transform(st["badge"], badge(1)), move_bar_anim(9, 10), rt=0.25)
            elif kind == "toast":
                t = toast("Advancement Made!", "Two numbers added", w=4.6)
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(st["badge"]), Transform(bar, line_bar(code, 11, 11, MC_GREEN)), rt=0.5)
                swap_ro(None, rt=0.2)
            elif kind == "read":
                self.sfx("click", 0.22)
                parts = [chain[2 * k]] + ([chain[2 * k - 1]] if k else [])
                self.beat(*[FadeIn(p, shift=UP * 0.15) for p in parts], rt=0.25)
            elif kind == "number":
                num = eq_line([("=", MC_GRAY), ("10407", MC_GOLD)], 64, buff=0.35).move_to([0, -1.0, 0])
                self.beat(FadeOut(chain, shift=UP * 0.3), FadeIn(num, shift=UP * 0.3), rt=0.45)

        def move_bar_anim(k0, k1):
            return Transform(bar, line_bar(code, k0, k1, MC_YELLOW))

        def on_last():
            # The chains leave the 3D clip when the walk ends; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        a = Chain2D(L1, ORE["l1"], 3.6, size=0.75, step=1.1, x0=-3.0)
        b = Chain2D(L2, ORE["l2"], 2.45, size=0.75, step=1.1, x0=-3.0)
        la = MT("m = 3", 40, MC_AQUA, PIXEL).move_to([2.9, 3.6, 0])
        lb = MT("n = 4", 40, MC_BLUE, PIXEL).move_to([2.9, 2.45, 0])
        cur = outline(b.blocks[0], MC_YELLOW, 8)
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(max(m, n))", 0.8)).arrange(RIGHT, buff=0.4).move_to([0, 1.05, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.1, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(a), FadeIn(b), rt=0.5)
        self.beat(FadeIn(la), FadeIn(lb), rt=0.3)
        self.until(at(16, "visited"))
        self.beat(Create(cur), rt=0.25)
        for k in range(1, len(L2)):
            self.sfx("click", 0.22)
            self.beat(cur.animate.move_to(b.blocks[k]), rt=0.3)
        self.until(at(16, "linear") - 0.6)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), FadeOut(cur), rt=0.4)
        self.add(xp)
        for d in (0.0, 0.3, 0.6):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=0.9)
        self.beat(Restore(xp), rt=1.0)
        self.close_seg()

        res = Chain2D(RESULT, ORE["sum"], -1.65, size=0.75, step=1.1, x0=-2.2, null=False)
        sp = VGroup(MT("space", 56, MC_GRAY), level_text("O(max(m, n))", 0.8)).arrange(RIGHT, buff=0.4).move_to([0, -3.2, 0])

        self.seg(17)
        self.add(res.rods, res.blocks)
        for k in range(len(RESULT)):
            self.sfx("pop", 0.28, delay=0.12 * k + 0.1)
        self.beat(LaggedStart(*[FadeIn(x, scale=0.5) for x in res.blocks], lag_ratio=0.15), Create(res.rods), rt=0.9)
        self.until(at(17, "extra") - 0.3)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(ADD_CODE, 1.6, width=8.4)
        bar = line_bar(code, 3, 3, MC_YELLOW)

        self.seg(18)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.06), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(at(18, "one carry") - 0.1)
        self.beat(Transform(bar, line_bar(code, 6, 6, MC_GOLD)), rt=0.35)
        self.until(at(18, "dummy") - 0.1)
        self.beat(Transform(bar, line_bar(code, 1, 1, MC_AQUA)), rt=0.35)
        self.until(at(18, "clean"))
        self.beat(Transform(bar, line_bar(code, 0, 11, MC_GREEN)), rt=0.4)
        self.close_seg()

        self.seg(19)
        msg = chat("Carry the one", MC_GOLD, 60)
        msg.move_to([0, -2.6, 0])
        self.until(0.1)
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.5)
        self.until(2.1)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.5)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=1.0)
        self.close_seg()
