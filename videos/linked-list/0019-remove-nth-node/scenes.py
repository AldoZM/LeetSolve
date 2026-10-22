WALK = json.load(open('walk.json', encoding='utf-8'))
VALS, MOVES = WALK["vals"], WALK["moves"]
WOOD = "#9C7A48"
NULL_EDGE = "#5A2A2A"
NODE_ORE, DUMMY_ORE = "lapis_ore", "stone"
NULL_SLOT = len(VALS) + 1

CODE = """def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next
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


def slot_name(k):
    return "D" if k == 0 else ("null" if k == NULL_SLOT else str(VALS[k - 1]))


class Chain2D(VGroup):
    """A linked list: ore blocks joined by wooden rods (next pointers), with a barrier as the null at the end.
    Labels "D" are the dummy (stone); `skip` leaves out the rods with those indices."""

    def __init__(self, values, y, size=0.9, step=1.3, x0=-3.0, null=True, skip=(), **kwargs):
        super().__init__(**kwargs)
        xs = [x0 + k * step for k in range(len(values) + 1)]
        self.xs = xs
        self.blocks = VGroup(*[Block(v, DUMMY_ORE if v == "D" else NODE_ORE, size).move_to([xs[k], y, 0])
                               for k, v in enumerate(values)])
        self.rods = VGroup(*[Line([xs[k] + size / 2, y, 0], [xs[k + 1] - size / 2, y, 0], color=WOOD, stroke_width=11 * size)
                             for k in range(len(values) - 1) if k not in skip])
        self.null = VGroup()
        if null:
            bar = pixel_art("barrier", size * 0.62).move_to([xs[-1], y, 0])
            rod = Line([xs[-2] + size / 2, y, 0], [xs[-1] - size * 0.31, y, 0], color=NULL_EDGE, stroke_width=8 * size)
            self.null = VGroup(rod, bar)
        # Rods first, so the blocks are drawn on top of them
        self.add(self.rods, self.null, self.blocks)


def veil(m):
    # Dims pixel art without touching it (set_opacity would turn a Block into a white square)
    return Rectangle(width=m.width, height=m.height, fill_color="#000000", fill_opacity=0.55, stroke_width=0).move_to(m)


def cross(m, color=MC_RED):
    a, b = m.get_corner(UL), m.get_corner(DR)
    c, d = m.get_corner(UR), m.get_corner(DL)
    return VGroup(Line(a, b, color=color, stroke_width=8), Line(c, d, color=color, stroke_width=8))


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("REMOVE NTH", width=7.6).move_to([0, 4.85, 0])
    t2 = stone_title("FROM END", width=7.6)
    t2.scale_to_fit_height(t1.height)
    t2.move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    chain = Chain2D(VALS, 1.25, size=0.8, step=1.15, x0=-3.0, skip=(2, 3))
    gone = chain.blocks[3]
    x_out = VGroup(veil(gone), cross(gone))
    b3, b5 = chain.blocks[2], chain.blocks[4]
    jump = ArcBetweenPoints(b3.get_bottom(), b5.get_bottom(), angle=1.6, color=WOOD, stroke_width=9)
    n_lab = chat("n = 2", MC_GOLD, 40).move_to([0, -0.75, 0])
    tags = VGroup(chat("LeetCode #19", MC_AQUA, 46), chat("Medium", MC_GOLD, 46), chat("Linked List", MC_GREEN, 46))
    tags.arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, jump, chain, x_out, n_lab, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, jump, chain, x_out, n_lab, tags = art
        self.add(art)

        self.seg(0)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        # The chain hops from the head to the end, then the removed block and the jump answer
        self.sfx("stone_dig1", 0.32, delay=0.2)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.3) for b in chain.blocks], lag_ratio=0.2),
                  rt=1.2)
        self.sfx("break", 0.3)
        self.beat(pulse(x_out, 1.2), rt=0.6)
        self.sfx("orb", 0.3)
        self.beat(pulse(chain.blocks[2], 1.15), pulse(chain.blocks[4], 1.15), rt=0.6)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        c = Chain2D(VALS, 3.0)
        nxt = MT("next", 30, MC_YELLOW).next_to(c.rods[0], DOWN, buff=0.12)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        blocks = list(c.blocks)
        for b in blocks:
            b.shift(UP * 8)
        self.add(*blocks)
        for k in range(len(blocks)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.3, delay=k * 0.12 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in blocks],
                              lag_ratio=0.12), rt=1.2)
        self.until(at(1, "only knows the next") - 0.2)
        # Rods behind the blocks: added first, then the blocks again on top
        self.add(c.rods, c.null, *blocks)
        self.sfx("wood_dig1", 0.35)
        self.beat(Create(c.rods), FadeIn(c.null), FadeIn(nxt, shift=UP * 0.1), rt=0.6)
        self.close_seg()

        counts = VGroup(MT("2nd", 34, MC_GOLD).next_to(c.blocks[3], DOWN, buff=0.25),
                        MT("1st", 34, MC_GRAY).next_to(c.blocks[4], DOWN, buff=0.25))
        n_lab = chat("n = 2", MC_GOLD, 48).move_to([0, 0.75, 0])
        mark = outline(c.blocks[3], MC_RED, 8)
        go = MT("must go", 36, MC_RED).move_to([c.blocks[3].get_x(), -0.25, 0])

        self.seg(2)
        self.beat(FadeOut(nxt), rt=0.3)
        self.until(at(2, "counting from the end") - 0.1)
        self.sfx("click", 0.3)
        self.beat(LaggedStart(FadeIn(counts[1], shift=UP * 0.1), FadeIn(counts[0], shift=UP * 0.1), lag_ratio=0.5), rt=0.8)
        self.until(at(2, "Here n is two") - 0.1)
        self.beat(FadeIn(n_lab, shift=UP * 0.15), rt=0.4)
        self.until(at(2, "the four must go") - 0.1)
        self.sfx("villager_no1", 0.35)
        self.beat(Create(mark), pulse(c.blocks[3], 1.2), FadeIn(go), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene3_TwoPass(Base):
    def construct(self):
        h = hdr("TWO PASSES", MC_RED)
        c = Chain2D(VALS, 3.0)
        cur = outline(c.blocks[0], MC_YELLOW, 8)
        length = chat("length = 5", MC_WHITE, 44).move_to([0, 1.6, 0])

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(c), rt=0.5)
        self.until(at(3, "walks") - 0.1)
        self.beat(Create(cur), rt=0.15)
        for k, b in enumerate(c.blocks[1:]):
            self.sfx("stone_step%d" % (k + 1), 0.28)
            self.beat(cur.animate.move_to(b), rt=0.2)
        self.until(at(3, "count it") - 0.1)
        self.sfx("pop", 0.3)
        self.beat(FadeIn(length, shift=UP * 0.15), rt=0.35)
        self.close_seg()

        cur2 = outline(c.blocks[0], MC_GREEN, 8)
        stop = MT("stop at 5 - 2 = 3", 38, MC_GREEN).move_to([0, 0.6, 0])
        mark = outline(c.blocks[3], MC_RED, 8)

        self.seg(4)
        self.until(at(4, "walks again") - 0.1)
        self.beat(FadeOut(cur), Create(cur2), rt=0.2)
        for k, b in enumerate(c.blocks[1:3]):
            self.sfx("stone_step%d" % (k + 5), 0.28)
            self.beat(cur2.animate.move_to(b), rt=0.3)
        self.until(at(4, "right before") - 0.1)
        self.beat(pulse(c.blocks[2], 1.2), FadeIn(stop, shift=UP * 0.1), rt=0.45)
        self.until(at(4, "the one we remove") - 0.1)
        self.beat(Create(mark), rt=0.3)
        self.close_seg()

        two = chat("2 passes", MC_RED, 48).move_to([0, -0.7, 0])
        one = chat("1 pass?", MC_GOLD, 48).move_to([0, -1.9, 0])

        self.seg(5)
        self.until(at(5, "two passes") - 0.3)
        self.sfx("villager_no2", 0.35)
        self.beat(FadeIn(two, shift=UP * 0.15), rt=0.4)
        self.until(at(5, "Can we") - 0.1)
        self.sfx("click", 0.3)
        self.beat(FadeIn(one, shift=UP * 0.15), rt=0.4)
        self.clear_all(rt=0.4)
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        c = Chain2D(["D"] + VALS, 3.0, size=0.8, step=1.15, x0=-3.45)
        xs = c.xs
        slow = outline(c.blocks[0], MC_AQUA, 8, buff=0.1)
        fast = outline(c.blocks[0], MC_GOLD, 8, buff=0.02)
        sl = MT("slow", 30, MC_AQUA).move_to([xs[0], 2.25, 0])
        fl = MT("fast", 30, MC_GOLD).move_to([xs[0], 1.85, 0])

        def hop(who, lab, k, rt=0.3):
            return [who.animate.move_to([xs[k], 3.0, 0]), lab.animate.move_to([xs[k], lab.get_y(), 0])]

        self.seg(6)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(c), rt=0.5)
        self.until(at(6, "two pointers") - 0.1)
        self.sfx("click", 0.3)
        self.beat(Create(slow), Create(fast), FadeIn(sl), FadeIn(fl), rt=0.4)
        self.until(at(6, "head start") - 0.1)
        for k in (1, 2, 3):
            self.sfx("stone_step%d" % k, 0.3)
            self.beat(*hop(fast, fl, k), rt=0.28)
        gap = MT("n + 1 = 3 steps ahead", 34, MC_GOLD).move_to([0, 0.95, 0])
        self.until(at(6, "n plus one") - 0.1)
        self.beat(FadeIn(gap, shift=UP * 0.1), rt=0.4)
        self.close_seg()

        mark = outline(c.blocks[4], MC_RED, 8, buff=0.06)
        tl = MT("target", 30, MC_RED).move_to([xs[4], 2.25, 0])

        self.seg(7)
        self.until(at(7, "move together") - 0.1)
        for s, f in ((1, 4), (2, 5)):
            self.sfx("stone_step%d" % (s + 3), 0.3)
            self.beat(*hop(slow, sl, s), *hop(fast, fl, f), rt=0.35)
        self.until(at(7, "falls off") - 0.1)
        self.sfx("villager_no3", 0.3)
        self.beat(*hop(slow, sl, 3), *hop(fast, fl, NULL_SLOT), rt=0.4)
        self.until(at(7, "slow one sits") - 0.1)
        self.beat(pulse(c.blocks[3], 1.2), pulse(slow, 1.1), rt=0.4)
        self.until(at(7, "the target") - 0.1)
        self.sfx("pop", 0.3)
        self.beat(Create(mark), FadeIn(tl), rt=0.4)
        self.close_seg()

        dl = MT("dummy", 30, MC_GRAY).move_to([xs[0], 3.75, 0])
        mini = Chain2D(["D", 1, 2], -1.4, size=0.8, step=1.3, x0=-1.55)
        mn = chat("n = 2", MC_GOLD, 36).move_to([-3.25, -1.4, 0])
        head_x = outline(mini.blocks[1], MC_RED, 8, buff=0.06)
        jump = ArcBetweenPoints(mini.blocks[0].get_bottom(), mini.blocks[2].get_bottom(), angle=1.6, color=WOOD, stroke_width=9)
        cap = MT("the head is removed", 34, MC_RED).move_to([0, -3.0, 0])

        self.seg(8)
        self.until(at(8, "dummy block") - 0.1)
        self.sfx("stone_dig2", 0.3)
        self.beat(pulse(c.blocks[0], 1.2), FadeIn(dl, shift=DOWN * 0.1), rt=0.45)
        self.until(at(8, "covers the case") - 0.1)
        self.beat(FadeIn(mini, shift=UP * 0.15), FadeIn(mn), rt=0.4)
        self.until(at(8, "the head itself") - 0.2)
        self.sfx("villager_no1", 0.3)
        self.beat(Create(head_x), FadeIn(cap), rt=0.3)
        self.until(at(8, "the head itself") + 0.3)
        self.sfx("wood_dig2", 0.32)
        self.beat(Create(jump), rt=0.35)
        self.clear_all(rt=0.4)
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("FAST & SLOW", MC_GREEN)
        code = code_panel(CODE, -4.4, max_h=2.9)
        bar = line_bar(code, 1, 2, MC_YELLOW)
        n_lab = chat("n = %d" % W["n"], MC_GOLD, 40).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)
        st = {"pos": None, "note": None, "slow": 0, "fast": 0}

        def pos_text():
            fast_c = MC_RED if st["fast"] == NULL_SLOT else MC_GOLD
            return eq_line([("slow =", MC_GRAY), (slot_name(st["slow"]), MC_AQUA), ("  fast =", MC_GRAY),
                            (slot_name(st["fast"]), fast_c)], 38, buff=0.25).move_to([0, -0.45, 0])

        def note(parts, size=34):
            return eq_line(parts, size, buff=0.25).move_to([0, -1.35, 0])

        def swap(key, new, rt=0.2):
            anims = [FadeIn(new)] if new is not None else []
            if st[key] is not None:
                anims.append(FadeOut(st[key]))
            st[key] = new
            self.beat(*anims, rt=rt)

        def move_bar(k0, k1=None, color=MC_YELLOW, rt=0.12):
            self.beat(Transform(bar, line_bar(code, k0, k1, color)), rt=rt)

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("start", "together", "sits", "before", "skip", "relink", "toast")]
        ev += [(seg_time(W["first"], spec) - 0.1, "read", k) for k, spec in enumerate(W["read"])]
        ev += [(seg_time(W["first"], m["t"]), "move", k) for k, m in enumerate(MOVES)]
        ev.sort(key=lambda e: e[0])
        heads = W["n"] + 1  # the head start: the first n + 1 moves are fast alone
        listing = VGroup()
        for k, v in enumerate(W["result"]):
            listing.add(MT(str(v), 56, MC_GREEN, PIXEL))
            if k < len(W["result"]) - 1:
                listing.add(MT("->", 44, MC_GRAY))
        listing.arrange(RIGHT, buff=0.22).move_to([0, -0.9, 0])

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(n_lab), rt=0.35)
            for i in range(6):
                self.sfx(f"stone_dig{i % 4 + 1}", 0.26, delay=0.1 + 0.08 * i)
            self.beat(FadeIn(code, shift=UP * 0.3), rt=0.5)

        def on(kind, k):
            if kind == "start":
                self.sfx("click", 0.3)
                self.beat(FadeIn(bar), rt=0.15)
                swap("pos", pos_text())
            elif kind == "move":
                m = MOVES[k]
                st[m["who"]] = m["to"]
                if k < heads:
                    self.sfx("stone_step%d" % (k + 1), 0.34)
                    move_bar(3, 4)
                    swap("pos", pos_text(), rt=0.15)
                    if k == heads - 1:
                        swap("note", note([("gap =", MC_GRAY), ("n + 1 = 3", MC_GOLD)]))
                elif m["to"] == NULL_SLOT:
                    self.sfx("villager_no2", 0.36)
                    move_bar(5, None, MC_RED, rt=0.15)
                    swap("pos", pos_text(), rt=0.15)
                    swap("note", note([("fast is null:", MC_RED), ("stop", MC_RED)]))
                else:
                    self.sfx("stone_step%d" % (k % 6 + 1), 0.32)
                    swap("pos", pos_text(), rt=0.15)
            elif kind == "together":
                move_bar(5, 6, MC_GREEN, rt=0.15)
            elif kind == "sits":
                self.beat(pulse(st["pos"], 1.08), rt=0.35)
            elif kind == "before":
                swap("note", note([("slow.next =", MC_GRAY), ("4", MC_RED)]))
            elif kind == "skip":
                self.sfx("break", 0.36)
                move_bar(7, None, MC_GREEN)
                swap("note", note([("slow.next =", MC_GRAY), ("slow.next.next", MC_WHITE)], 30))
            elif kind == "relink":
                self.sfx("wood_dig3", 0.3)
                swap("note", note([("3.next =", MC_GRAY), ("5", MC_GREEN)]))
            elif kind == "toast":
                t = toast("Advancement Made!", "Node removed", w=4.6)
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(n_lab), FadeOut(st["pos"]), FadeOut(st["note"]),
                          Transform(bar, line_bar(code, 8, 8, MC_GREEN)), rt=0.5)
                st["pos"], st["note"] = None, None
            elif kind == "read":
                self.sfx("click", 0.22)
                parts = [listing[2 * k]] + ([listing[2 * k - 1]] if k else [])
                self.beat(*[FadeIn(p, shift=UP * 0.15) for p in parts], rt=0.12)

        def on_last():
            # The chain leaves the 3D clip when the walk ends; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.3)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        c = Chain2D(VALS, 3.5, size=0.75, step=1.1, x0=-2.8)
        cur = outline(c.blocks[0], MC_GOLD, 8)
        once = MT("one pass", 40, MC_GREEN).move_to([0, 2.4, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, 1.2, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.25, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(14)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(c), rt=0.5)
        self.until(at(14, "only once") - 0.1)
        self.beat(Create(cur), rt=0.15)
        for k, b in enumerate(c.blocks[1:]):
            self.sfx("stone_step%d" % (k + 1), 0.25)
            self.beat(cur.animate.move_to(b), rt=0.2)
        self.until(at(14, "linear") - 0.4)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.35)
        self.add(xp)
        self.sfx("orb", 0.25)
        self.sfx("levelup", 0.3, delay=0.3)
        self.beat(Restore(xp), rt=0.45)
        self.until(at(14, "single pass") - 0.1)
        self.beat(FadeIn(once, shift=UP * 0.1), FadeOut(cur), rt=0.3)
        self.close_seg()

        ptrs = VGroup(chat("slow", MC_AQUA, 46), chat("fast", MC_GOLD, 46), chat("dummy", MC_GRAY, 46))
        ptrs.arrange(RIGHT, buff=0.3).move_to([0, -1.3, 0])
        sp = VGroup(MT("space", 56, MC_GRAY), level_text("O(1)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, -2.8, 0])

        self.seg(15)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(FadeIn(ptrs[0], scale=0.6), FadeIn(ptrs[1], scale=0.6), lag_ratio=0.3), rt=0.5)
        self.until(at(15, "dummy block") - 0.1)
        self.sfx("pop", 0.28)
        self.beat(FadeIn(ptrs[2], scale=0.6), rt=0.3)
        self.until(at(15, "Constant") - 0.3)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.4)
        self.clear_all(rt=0.4)
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.6, width=8.4)
        bar = line_bar(code, 1, 2, MC_YELLOW)

        self.seg(16)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.07), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(at(16, "head start") - 0.1)
        self.beat(Transform(bar, line_bar(code, 3, 4, MC_GOLD)), rt=0.35)
        self.until(at(16, "move both") - 0.1)
        self.beat(Transform(bar, line_bar(code, 5, 6, MC_GREEN)), rt=0.35)
        self.close_seg()

        self.seg(17)
        msg = chat("Keep a fixed gap", MC_GOLD, 58)
        msg.move_to([0, -2.6, 0])
        self.beat(FadeIn(msg, shift=UP * 0.2), Transform(bar, line_bar(code, 7, 7, MC_GOLD)), rt=0.4)
        self.until(1.5)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.4)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.8)
        self.close_seg()
