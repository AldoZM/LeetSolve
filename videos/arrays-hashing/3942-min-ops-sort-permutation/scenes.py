WALK = json.load(open('walk.json', encoding='utf-8'))
NUMS, P, ANSWER = WALK["nums"], WALK["p"], WALK["answer"]
ORE_OF.update(dict(zip(NUMS, WALK["ores"])))

SOLVE_CODE = """def minOperations(nums):
    n, p = len(nums), nums.index(0)
    ans = []
    if all(nums[(p + i) % n] == i for i in range(n)):
        ans += [p, (n - p) % n + 2]
    if all(nums[(p - i) % n] == i for i in range(n)):
        ans += [(p + 1) % n + 1, n - p]
    return min(ans) if ans else -1"""


def ph(i, phrase, shift=0.0):
    # Seconds into line i where `phrase` starts being spoken (even speaking rate inside a line)
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase)
    return max(0.0, min(dur - 0.25, dur * k / len(text) + shift))


def reachable(start):
    # Every row the two levers can reach, in breadth first order
    seen, order = {tuple(start)}, [list(start)]
    k = 0
    while k < len(order):
        t = order[k]
        k += 1
        for u in (t[::-1], t[1:] + t[:1]):
            if tuple(u) not in seen:
                seen.add(tuple(u))
                order.append(u)
    return order


def index_row(row, size=34, color=MC_GRAY, buff=0.14):
    return VGroup(*[MT(str(k), size, color).next_to(b, DOWN, buff=buff) for k, b in enumerate(row)])


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def pulse(m, s=1.15):
    # Pixel art is highlighted with a scale pulse; Indicate with a color paints it flat
    return m.animate(rate_func=there_and_back).scale(s)


def lever_icon(w=1.8, on=False):
    # The game's own lever model (cobblestone base, handle at 45 degrees), seen like in the inventory;
    # not re-centered, so the off and on states keep the base in the same place
    return model_icon("lever_on" if on else "lever", w, rot_y=45, center=False)


def pull(scene, lever_group, back_after=0.35):
    # Pulling a lever flips its handle (the lever_on model) and lets it go again
    off = lever_group[0]
    # Both states are built in block coordinates; the on state follows wherever the off one was moved
    on = lever_icon(on=True).shift(off.get_center() - lever_icon().get_center())
    scene.sfx("click", 0.4)
    scene.beat(FadeOut(off, run_time=0.01), FadeIn(on, run_time=0.01), rt=0.1)
    scene.hold(back_after)
    scene.beat(FadeOut(on, run_time=0.01), FadeIn(off, run_time=0.01), rt=0.1)


def lever(label, w=1.8):
    g = VGroup(lever_icon(w), MT(label, 34, MC_WHITE)).arrange(DOWN, buff=0.12)
    return g


def reverse_anims(blocks, slots):
    # Every block jumps to its mirror slot; returns the anims and the new order
    n = len(blocks)
    anims = [b.animate(path_arc=-150 * DEGREES).move_to(slots[n - 1 - k]) for k, b in enumerate(blocks)]
    return anims, blocks[::-1]


def rotate_anims(blocks, slots):
    # The first block hops over the row to the end; the others slide one slot left
    first = blocks[0]
    anims = [first.animate(path_arc=-200 * DEGREES).move_to(slots[-1])]
    anims += [b.animate.move_to(slots[k]) for k, b in enumerate(blocks[1:])]
    return anims, blocks[1:] + blocks[:1]


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    title = stone_title("MIN OPERATIONS", 60, width=7.8).move_to([0, 4.0, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.25, 2.75, 0])
    row = block_row(NUMS, 0.95, size=1.05, gap=0.2)
    idx = index_row(row)
    pick = pickaxe(1.25).move_to([-1.3, -1.2, 0])
    lev = lever_icon(2.4).move_to([1.3, -1.2, 0])
    tags = VGroup(chat("LeetCode #3942", MC_AQUA, 46), chat("Medium", MC_GOLD, 46), chat("Rotation", MC_GREEN, 46))
    tags.arrange(RIGHT, buff=0.2)
    if tags.width > 8.4:
        tags.scale_to_fit_width(8.4)
    tags.move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, title, spl, row, idx, pick, lev, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, title, spl, row, idx, pick, lev, tags = art
        self.add(art)

        self.seg(0)
        self.beat(pulse(spl), rt=0.8)
        # Blocks hop one after another, like a wave
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.35) for b in row], lag_ratio=0.18), rt=1.6)
        self.sfx("stone_dig1", 0.35, delay=0.35)
        self.until(ph(0, "LeetCode"))
        self.sfx("click", 0.35)
        self.beat(pulse(lev, 1.15), pulse(row[P], 1.15), rt=0.8)
        self.until(ph(0, "with only"))
        self.beat(pulse(spl), Rotate(pick, angle=-30 * DEGREES, rate_func=there_and_back), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        row = block_row(NUMS, 2.6, size=1.05, gap=0.2)
        idx = index_row(row)
        lab = MT("nums", 40, MC_WHITE).next_to(row, UP, buff=0.2).align_to(row, LEFT)
        slots = [b.get_center() for b in row]
        rev, rot = lever("reverse"), lever("rotate left")
        VGroup(rev, rot).arrange(RIGHT, buff=2.2).move_to([0, -0.4, 0])

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
        self.until(ph(1, "two levers"))
        self.sfx("wood_dig1", 0.35)
        self.beat(FadeIn(rev, shift=UP * 0.2), FadeIn(rot, shift=UP * 0.2), rt=0.5)
        self.close_seg()

        # Each lever, shown on the row and then undone
        self.seg(2)
        blocks = list(row)
        self.until(ph(2, "reverses"))
        pull(self, rev, 0.1)
        anims, blocks = reverse_anims(blocks, slots)
        self.sfx("stone_step1", 0.3, delay=0.5)
        self.beat(*anims, rt=0.8)
        anims, blocks = reverse_anims(blocks, slots)
        self.until(ph(2, "The second", -0.7))
        self.beat(*anims, rt=0.5)
        self.until(ph(2, "rotates it left"))
        pull(self, rot, 0.1)
        anims, blocks = rotate_anims(blocks, slots)
        self.sfx("stone_step2", 0.3, delay=0.6)
        self.beat(*anims, rt=0.9)
        self.until(ph(2, "to the end", 0.2))
        # Rotating right puts it back
        last = blocks[-1]
        self.beat(last.animate(path_arc=200 * DEGREES).move_to(slots[0]), *[b.animate.move_to(slots[k + 1]) for k, b in enumerate(blocks[:-1])],
                  rt=0.5)
        self.close_seg()

        self.seg(3)
        ask = chat("fewest pulls ?   or  -1", MC_GOLD, 44)
        ask.move_to([0, -2.6, 0])
        self.until(ph(3, "fewest"))
        self.beat(FadeIn(ask, shift=UP * 0.2), rt=0.5)
        ans = chat(f"return {ANSWER}", MC_GREEN, 60)
        ans.move_to([0, -4.0, 0])
        self.until(ph(3, "Here"))
        self.sfx("orb", 0.3)
        self.beat(FadeIn(ans, shift=UP * 0.2), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("BRUTE FORCE", MC_RED)
        states = reachable(NUMS)
        minis = VGroup()
        for k, s in enumerate(states):
            r = block_row(s, 0, size=0.24, gap=0.03)
            r.move_to([(k % 3 - 1) * 2.9, 2.6 - (k // 3) * 0.75, 0])
            minis.add(r)
        pick = pickaxe(1.0).move_to([-2.9, -1.15, 0])

        def counter(c):
            m = chat(f"rows visited {c}", MC_WHITE, 30, PIXEL)
            m.move_to([1.1, -1.15, 0])
            return m

        cnt = counter(1)

        self.seg(4)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(ph(4, "breadth first"))
        self.sfx("pop", 0.3)
        self.beat(FadeIn(minis[0], scale=0.7), FadeIn(pick, scale=0.6), FadeIn(cnt), rt=0.5)
        self.until(ph(4, "every row"))
        # The first wave: what one pull of each lever gives
        self.sfx("pop", 0.3)
        self.beat(FadeIn(minis[1], shift=DOWN * 0.15), FadeIn(minis[2], shift=DOWN * 0.15), Transform(cnt, counter(3)), rt=0.5)
        self.close_seg()

        self.seg(5)
        self.until(ph(5, "copies the whole row"))
        self.beat(*[pulse(b, 1.25) for b in minis[2]], rt=0.6)
        self.until(ph(5, "up to two n"))
        rest = list(range(3, len(states)))
        for k in rest:
            if k % 2:
                self.sfx(f"stone_dig{k % 4 + 1}", 0.22)
            self.beat(FadeIn(minis[k], shift=DOWN * 0.15), Transform(cnt, counter(k + 1)), rt=0.12)
        two_n = chat(f"2n = {len(states)} rows", MC_GOLD, 40)
        two_n.move_to([0, -0.15, 0])
        self.beat(FadeIn(two_n, shift=UP * 0.15), rt=0.4)
        self.close_seg()

        self.seg(6)
        o = big_o_pow("n", 2, 72, MC_RED)
        o.move_to([0, -2.3, 0])
        self.until(ph(6, "n squared", -0.2))
        self.beat(FadeIn(o, scale=0.5), rt=0.5)
        big = MT("10,000,000,000", 40, MC_RED, PIXEL)
        big.move_to([0, -3.5, 0])
        self.until(ph(6, "ten billion", -0.2))
        self.beat(FadeIn(big, scale=1.3), rt=0.5)
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
        n = len(NUMS)
        C, R = np.array([0, 1.7, 0]), 2.0
        # Slot k of the circle, clockwise from the top
        pos = [C + R * np.array([np.sin(2 * np.pi * k / n), np.cos(2 * np.pi * k / n), 0]) for k in range(n)]
        ring = Circle(radius=R, color=MC_GOLD, stroke_width=8).move_to(C)
        blocks = [Block(v, f"{ORE_OF[v]}_ore", 0.9).move_to(pos[k]) for k, v in enumerate(NUMS)]

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        # The ring goes in before the blocks so it stays behind them
        self.add(ring, *blocks)
        self.beat(Create(ring), LaggedStart(*[FadeIn(b, scale=0.6) for b in blocks], lag_ratio=0.1), rt=0.9)
        self.until(ph(7, "never break"))
        # A rotation turns the circle one slot
        self.sfx("stone_step3", 0.3)
        self.beat(*[b.animate(path_arc=-60 * DEGREES).move_to(pos[(k - 1) % n]) for k, b in enumerate(blocks)], rt=0.8)
        blocks = blocks[1:] + blocks[:1]
        # A reversal mirrors it
        self.sfx("stone_step4", 0.3)
        self.beat(*[b.animate(path_arc=90 * DEGREES).move_to(pos[(n - k) % n]) for k, b in enumerate(blocks)], rt=0.8)
        blocks = [blocks[0]] + blocks[1:][::-1]
        self.until(ph(7, "Neighbors"))
        self.beat(pulse(ring, 1.06), rt=0.7)
        self.close_seg()

        self.seg(8)
        fw = chat("forwards  0 1 2 3 4 5", MC_GREEN, 40)
        bw = chat("backwards  0 5 4 3 2 1", MC_AQUA, 40)
        VGroup(fw, bw).arrange(DOWN, buff=0.2).move_to([0, -2.1, 0])
        self.until(ph(8, "forwards"))
        self.beat(FadeIn(fw, shift=UP * 0.15), rt=0.4)
        self.until(ph(8, "backwards"))
        self.beat(FadeIn(bw, shift=UP * 0.15), rt=0.4)
        no = chat("anything else  ->  -1", MC_RED, 40)
        no.move_to([0, -3.6, 0])
        self.until(ph(8, "If not"))
        self.sfx("villager_no1", 0.25)
        self.beat(FadeIn(no, shift=UP * 0.15), rt=0.4)
        self.close_seg()

        self.seg(9)
        self.beat(FadeOut(VGroup(ring, *blocks, fw, bw, no)), rt=0.4)
        plans = VGroup(chat("forwards", MC_GREEN, 40), chat("1  rotate p times", MC_WHITE, 36),
                       chat("2  reverse, rotate, reverse", MC_WHITE, 36), chat("backwards", MC_AQUA, 40),
                       chat("3  rotate, then reverse", MC_WHITE, 36), chat("4  reverse, then rotate", MC_WHITE, 36))
        plans.arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([0, 1.0, 0])
        self.until(ph(9, "four plans", -0.3))
        self.sfx("book_flip1", 0.3)
        self.beat(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in plans], lag_ratio=0.15), rt=1.2)
        self.until(ph(9, "count the cost"))
        self.beat(*[pulse(plans[k], 1.06) for k in (1, 2, 4, 5)], rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("COUNT PLANS", MC_GREEN)
        code = code_panel(SOLVE_CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 1, 1, MC_YELLOW)
        st = {"ro": None}

        def show(*lines):
            # The readout under the 3D row: one chat box per line, replaced as the walk goes
            g = VGroup(*[chat(s, c, 40) for s, c in lines]).arrange(DOWN, buff=0.15)
            g.move_to([0, -1.15, 0])
            old = st["ro"]
            st["ro"] = g
            if old is None:
                self.beat(FadeIn(g, shift=UP * 0.15), rt=0.3)
            else:
                self.beat(FadeOut(old), FadeIn(g, shift=UP * 0.15), rt=0.3)

        def move_bar(a, b=None, color=MC_YELLOW, rt=0.15):
            self.beat(Transform(bar, line_bar(code, a, a if b is None else b, color)), rt=rt)

        keys = ("find", "found", "holds", "compare", "plan1_cost", "sorted", "toast", "beat", "answer_t")
        ev = [(seg_time(W["first"], W[k]), k, None) for k in keys]
        ev += [(seg_time(W["first"], r), "read", v) for v, r in enumerate(W["reads"])]
        ev += [(seg_time(W["first"], m["t"]), "move", k) for k, m in enumerate(W["moves"])]
        ev.sort(key=lambda e: e[0])

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.35)

        def on(kind, k):
            if kind == "find":
                self.beat(FadeIn(code, shift=UP * 0.3), FadeIn(bar), rt=0.4)
            elif kind == "found":
                self.sfx("pop", 0.35)
                show((f"zero at p = {P}", MC_YELLOW))
            elif kind == "read":
                self.sfx("click", 0.3)
                if k == 0:
                    move_bar(3)
            elif kind == "holds":
                for d in (0.0, 0.2):
                    self.sfx("orb", 0.25, delay=d)
                move_bar(3, color=MC_GREEN)
                show(("circle: forwards", MC_GREEN))
            elif kind == "compare":
                self.sfx("wood_dig2", 0.35)
                move_bar(4)
            elif kind == "plan1_cost":
                show(("circle: forwards", MC_GREEN), (f"plan 1 = p = {W['plan1']}", MC_WHITE))
            elif kind == "move":
                self.sfx("click", 0.4)
                self.sfx("stone_step1" if W["moves"][k]["kind"] == "reverse" else "stone_step2", 0.3, delay=0.45)
            elif kind == "sorted":
                for d in (0.0, 0.2, 0.4):
                    self.sfx("orb", 0.28, delay=d)
            elif kind == "toast":
                t = toast("Advancement Made!", "Min Ops solved", w=4.6)
                t.move_to([0, 5.5, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                self.beat(t.animate.shift(LEFT * 7), rt=0.5)
            elif kind == "beat":
                move_bar(7, color=MC_GREEN)
                show((f"plan 1 = {W['plan1']}", MC_GRAY), (f"plan 2 = {W['plan2']}", MC_GOLD))
            elif kind == "answer_t":
                # The answer takes the place of the readout: higher up it would cover the 3D row
                ans = chat(f"return {ANSWER}", MC_GREEN, 60)
                ans.move_to([0, -1.15, 0])
                self.beat(FadeOut(st["ro"]), FadeIn(ans, shift=UP * 0.2), rt=0.4)

        def on_last():
            # The 3D clip fades to the roam at its end; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        per = VGroup(lever_icon(1.4), MT("one pass over the row", 44, MC_WHITE))
        per.arrange(RIGHT, buff=0.35).move_to([0, 3.4, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n)", 1.05)).arrange(RIGHT, buff=0.4)
        tm.move_to([0, 1.65, 0])
        # The game's experience bar fills up as the walk goes linear
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.6, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(ph(16, "read the row"))
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in per], lag_ratio=0.25), rt=0.6)
        self.until(ph(16, "That's"))
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.35)
        self.add(xp)
        for d in (0.0, 0.2, 0.4):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=0.6)
        self.beat(Restore(xp), rt=0.6)
        self.close_seg()

        self.seg(17)
        few = MT("p, n and four plans", 44, MC_WHITE)
        few.move_to([0, -1.4, 0])
        self.until(ph(17, "a few numbers", -0.3))
        self.sfx("click", 0.3)
        self.beat(FadeIn(few, shift=UP * 0.15), rt=0.4)
        sp = VGroup(MT("space", 56, MC_GRAY), MT("O(1)", 52, MC_GOLD, PIXEL)).arrange(RIGHT, buff=0.4)
        sp.move_to([0, -3.1, 0])
        self.until(ph(17, "constant", -0.6))
        self.sfx("pop", 0.35)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(SOLVE_CODE, 1.6, width=8.4)
        bar = line_bar(code, 1, 1, MC_YELLOW)

        self.seg(18)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(ph(18, "check both"))
        self.beat(Transform(bar, line_bar(code, 3, 6, MC_GOLD)), rt=0.3)
        self.until(ph(18, "take the cheapest"))
        self.beat(Transform(bar, line_bar(code, 7, 7, MC_GREEN)), rt=0.3)
        self.close_seg()

        self.seg(19)
        msg = chat("Don't search. Count.", MC_GOLD, 56)
        msg.move_to([0, -3.0, 0])
        self.until(ph(19, "you don't search", -0.2))
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.5)
        self.until(ph(19, "That's the big", -0.1))
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.4)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.9)
        self.close_seg()
