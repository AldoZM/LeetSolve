WALK = json.load(open('walk.json', encoding='utf-8'))
RAW, NUMS, TARGET, GROUPS = WALK["raw"], WALK["nums"], WALK["target"], WALK["groups"]
ORE_OF.update(dict(zip(NUMS, WALK["ores"])))

BRUTE_CODE = """def fourSum(nums, target):
    n, out = len(nums), set()
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                for d in range(c + 1, n):
                    q = (nums[a], nums[b], nums[c], nums[d])
                    if sum(q) == target:
                        out.add(tuple(sorted(q)))
    return [list(q) for q in out]"""

CODE = """def fourSum(nums, target):
    nums.sort()
    n, out = len(nums), []
    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i - 1]: continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j - 1]: continue
            l, r = j + 1, n - 1
            while l < r:
                s = nums[i] + nums[j] + nums[l] + nums[r]
                if s < target: l += 1
                elif s > target: r -= 1
                else:
                    out.append([nums[i], nums[j], nums[l], nums[r]])
                    l, r = l + 1, r - 1
                    while l < r and nums[l] == nums[l - 1]: l += 1
    return out"""

PTR_COLORS = {"i": MC_GOLD, "j": MC_YELLOW, "L": MC_AQUA, "R": MC_PINK}


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


def ptr_mark(name, block, size=36):
    # Pointer letter under its block, in the pointer's color
    m = MT(name, size, PTR_COLORS[name], PIXEL)
    m.next_to(block, DOWN, buff=0.2)
    return m


def group_chat(g, color=MC_GREEN, size=40):
    return chat("[" + ", ".join(str(v) for v in g) + "]", color, size)


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    title = stone_title("4SUM", 60, width=5.2).move_to([0, 4.3, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.35, 3.0, 0])
    row = block_row(NUMS, 1.55, size=1.0, gap=0.2)
    zero = MT("= 0", 56, MC_GOLD, PIXEL).move_to([0, 0.35, 0])
    groups = VGroup(*[group_chat(g, MC_GREEN, 36) for g in GROUPS]).arrange(RIGHT, buff=0.18)
    groups.move_to([0, -0.75, 0])
    tags = VGroup(chat("LeetCode #18", MC_AQUA, 40), chat("Medium", MC_GOLD, 40), chat("Two Pointers", MC_GREEN, 40))
    tags.arrange(RIGHT, buff=0.22).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, title, spl, row, zero, groups, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, title, spl, row, zero, groups, tags = art
        self.add(art)

        self.seg(0)
        self.beat(pulse(spl), rt=0.8)
        # Blocks hop one after another, like a wave
        self.sfx("stone_dig1", 0.35, delay=0.35)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.there_and_back).shift(UP * 0.35) for b in row],
                              lag_ratio=0.18), rt=1.6)
        # The three groups light up one by one
        for d in (0.2, 0.5, 0.8):
            self.sfx("orb", 0.28, delay=d)
        self.beat(LaggedStart(*[pulse(g, 1.12) for g in groups], lag_ratio=0.3), rt=1.2)
        self.beat(pulse(spl), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        tsign = target_sign().move_to([0, 3.55, 0])
        row = block_row(RAW, 1.15, size=1.0, gap=0.2)
        idx = index_row(row, 32)
        lab = MT("nums", 40, MC_WHITE).next_to(row, UP, buff=0.2).align_to(row, LEFT)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.35)
        # Blocks fall from the sky and bounce into place
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(len(row)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.3, delay=k * 0.1 + 0.3)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.1), rt=1.3)
        self.beat(FadeIn(idx, shift=UP * 0.1), FadeIn(lab), rt=0.3)
        self.until(at(1, "a target") - 0.1)
        self.sfx("wood_dig1", 0.4)
        self.beat(FadeIn(tsign, scale=0.6), rt=0.4)
        self.close_seg()

        chats = [group_chat(g, MC_GREEN, 44) for g in GROUPS]
        for k, c in enumerate(chats):
            c.move_to([0, -0.85 - 0.85 * k, 0])
        once = MT("each group only once", 40, MC_GRAY)
        once.move_to([0, -3.6, 0])

        self.seg(2)
        self.until(at(2, "every group") - 0.1)
        for k, c in enumerate(chats):
            self.sfx("pop", 0.32)
            self.beat(FadeIn(c, shift=UP * 0.15), rt=0.35)
        self.until(at(2, "without") - 0.1)
        self.sfx("book_put", 0.35)
        self.beat(FadeIn(once, shift=UP * 0.1), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("BRUTE FORCE", MC_RED)
        row = block_row(RAW, 3.0, size=0.92, gap=0.2)
        idx = index_row(row, 30)
        code = code_panel(BRUTE_CODE, -3.7, max_h=2.9)
        pick = pickaxe(1.05).move_to([-2.4, 1.1, 0])
        dbg = Rectangle(width=1.2, height=0.16, fill_color="#000000", fill_opacity=1, stroke_width=0)
        dbg.next_to(pick, DOWN, buff=0.15)
        quads = [(a, b, c, d) for a in range(6) for b in range(a + 1, 6) for c in range(b + 1, 6) for d in range(c + 1, 6)]

        def dfill(frac):
            # Durability bar: shrinks and turns from green to red
            r = Rectangle(width=max(1.16 * frac, 0.02), height=0.1, stroke_width=0, fill_opacity=1,
                          fill_color=interpolate_color(ManimColor(MC_RED), ManimColor(MC_GREEN), frac))
            r.move_to(dbg.get_left() + RIGHT * (0.02 + max(1.16 * frac, 0.02) / 2))
            return r

        def counter(k):
            c = MT(f"groups {k}", 30, MC_WHITE, PIXEL)
            c.move_to([1.0, 1.1, 0])
            return c

        fill = dfill(1.0)
        st = {"cnt": counter(0)}
        frames = [outline(row[k], c, 6) for k, c in zip(range(4), (MC_YELLOW, MC_WHITE, MC_AQUA, MC_PINK))]
        bar = line_bar(code, 2, 5, MC_YELLOW)

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in row], lag_ratio=0.1), rt=0.8)
        self.beat(FadeIn(idx), rt=0.3)
        self.until(at(3, "every group") - 0.2)
        self.beat(FadeIn(code, shift=UP * 0.3), FadeIn(pick, scale=0.6), FadeIn(dbg), FadeIn(fill), FadeIn(st["cnt"]), rt=0.5)
        self.until(at(3, "four nested") - 0.1)
        self.beat(FadeIn(bar), *[Create(f) for f in frames], rt=0.4)
        self.close_seg()

        def check(n, rt):
            nc = counter(n + 1)
            anims = [f.animate.move_to(row[k]) for f, k in zip(frames, quads[n])]
            anims += [Transform(fill, dfill(1 - (n + 1) / 17)), FadeTransform(st["cnt"], nc),
                      Rotate(pick, angle=-25 * DEGREES, rate_func=there_and_back)]
            self.sfx(f"stone_dig{n % 4 + 1}", 0.2, delay=rt * 0.5)
            self.beat(*anims, rt=rt)
            st["cnt"] = nc

        self.seg(4)
        for n in range(len(quads)):
            check(n, 0.12)
        # Two different picks of indices, the same group of values: 1, 0, -1, -2 with either zero
        one, two = (0, 1, 2, 4), (0, 2, 3, 4)
        c1 = group_chat([RAW[k] for k in one], MC_WHITE, 38)
        c2 = group_chat([RAW[k] for k in two], MC_WHITE, 38)
        c1.move_to([0.0, 0.0, 0])
        c2.move_to([0.0, -0.75, 0])
        same = MT("same group!", 36, MC_GOLD)
        same.move_to([2.95, -0.37, 0])
        self.until(at(4, "a repeated") - 0.1)
        self.beat(*[f.animate.move_to(row[k]) for f, k in zip(frames, one)], FadeIn(c1, shift=UP * 0.1), rt=0.4)
        self.until(at(4, "the same group") - 0.3)
        self.sfx("villager_no1", 0.35)
        self.beat(*[f.animate.move_to(row[k]) for f, k in zip(frames, two)], FadeIn(c2, shift=UP * 0.1), rt=0.4)
        self.beat(FadeIn(same, shift=LEFT * 0.1), Transform(bar, line_bar(code, 8, 8, MC_GOLD)), rt=0.3)
        self.close_seg()

        self.seg(5)
        self.beat(FadeOut(Group(row, idx, *frames, code, bar, c1, c2, same, st["cnt"])),
                  VGroup(pick, dbg, fill).animate.move_to([0, -3.1, 0]), rt=0.4)
        o = big_o_pow("n", 4, 72, MC_RED)
        o.move_to([0, 3.0, 0])
        self.until(at(5, "n to the fourth") - 0.2)
        self.beat(FadeIn(o, scale=0.5), rt=0.4)
        n = eq_line([("n =", MC_GRAY), ("1,000", MC_WHITE)], 32)
        n.move_to([0, 1.5, 0])
        self.until(at(5, "A thousand") - 0.1)
        self.beat(FadeIn(n, shift=UP * 0.2), rt=0.4)
        big = MT("41,417,124,750", 38, MC_RED, PIXEL)
        big.move_to([0, 0.2, 0])
        pl = MT("groups", 52, MC_GRAY)
        pl.next_to(big, DOWN, buff=0.25)
        self.until(at(5, "forty billion") - 0.3)
        self.beat(FadeIn(big, scale=1.4), FadeIn(pl), rt=0.5)
        self.until(at(5, "The pickaxe") + 0.05)
        self.beat(Wiggle(pick), rt=0.35)
        self.sfx("break", 0.45)
        self.beat(FadeOut(pick, scale=0.3), FadeOut(fill), FadeOut(dbg), rt=0.25)
        self.clear_all(rt=0.4)
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        row = block_row(RAW, 2.6, size=1.0, gap=0.2)
        srt = block_row(NUMS, 2.6, size=1.0, gap=0.2)
        # Sorted place of each raw block; the two zeros keep their order
        order = sorted(range(len(RAW)), key=lambda q: (RAW[q], q))
        place = [order.index(k) for k in range(len(RAW))]

        self.seg(6)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(row, shift=DOWN * 0.2), rt=0.3)
        self.sfx("stone_step2", 0.3)
        self.sfx("stone_step4", 0.3, delay=0.35)
        self.beat(*[row[k].animate(path_arc=-PI / 3).move_to(srt[place[k]]) for k in range(len(RAW))], rt=0.6)
        blocks = [row[k] for k in order]
        fi, fj = outline(blocks[0], MC_GOLD, 8), outline(blocks[1], MC_YELLOW, 8)
        im, jm = ptr_mark("i", blocks[0]), ptr_mark("j", blocks[1])
        self.until(at(6, "Fix two") - 0.1)
        self.sfx("click", 0.3)
        self.beat(Create(fi), Create(fj), FadeIn(im, shift=UP * 0.2), FadeIn(jm, shift=UP * 0.2), rt=0.4)
        fl, fr = outline(blocks[2], MC_AQUA, 7), outline(blocks[5], MC_PINK, 7)
        lm, rm = ptr_mark("L", blocks[2]), ptr_mark("R", blocks[5])
        self.until(at(6, "two pointers") - 0.1)
        self.sfx("click", 0.3)
        self.beat(Create(fl), Create(fr), FadeIn(lm, shift=UP * 0.2), FadeIn(rm, shift=UP * 0.2), rt=0.4)
        self.close_seg()

        small = eq_line([("too small", MC_AQUA), ("->", MC_GRAY), ("L moves right", MC_AQUA)], 42, TERM, 0.3)
        small.move_to([0, 0.4, 0])
        bigg = eq_line([("too big", MC_PINK), ("->", MC_GRAY), ("R moves left", MC_PINK)], 42, TERM, 0.3)
        bigg.move_to([0, -0.6, 0])
        eq = eq_line([("equal value", MC_RED), ("->", MC_GRAY), ("skip it", MC_RED)], 42, TERM, 0.3)
        eq.move_to([0, -1.6, 0])
        bar = pixel_art("barrier", 0.62)
        bar.move_to(blocks[3].get_top() + UP * 0.45)

        self.seg(7)
        self.sfx("stone_step1", 0.3)
        self.beat(FadeIn(small, shift=UP * 0.15), lm.animate.next_to(blocks[3], DOWN, buff=0.2), fl.animate.move_to(blocks[3]), rt=0.5)
        self.until(at(7, "Too big") - 0.1)
        self.sfx("stone_step3", 0.3)
        self.beat(FadeIn(bigg, shift=UP * 0.15), rm.animate.next_to(blocks[4], DOWN, buff=0.2), fr.animate.move_to(blocks[4]), rt=0.5)
        self.until(at(7, "Equal") - 0.1)
        self.sfx("villager_no2", 0.32)
        self.beat(FadeIn(eq, shift=UP * 0.15), FadeIn(bar, scale=0.5), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("SQUEEZE", MC_GREEN)
        tsign = target_sign(0.6)
        tsign.move_to([0, TOP_Y - 0.05, 0]).to_edge(RIGHT, buff=0.4)
        code = code_panel(CODE, -3.95, max_h=3.5)
        bar = line_bar(code, 1, 1, MC_YELLOW)
        st = {"sum": None}
        found = []

        def sum_line(e):
            vals = [NUMS[e[k]] for k in ("i", "j", "l", "r")]
            cols = [MC_GOLD, MC_YELLOW, MC_AQUA, MC_PINK]
            parts = []
            for v, c in zip(vals, cols):
                if parts:
                    parts.append(("+", MC_GRAY))
                parts.append((str(v), c))
            s = e["sum"]
            parts.append(("=", MC_GRAY))
            parts.append((str(s), MC_GREEN if s == TARGET else MC_WHITE))
            if s < TARGET:
                parts.append(("< 0", MC_AQUA))
            elif s > TARGET:
                parts.append(("> 0", MC_PINK))
            line = eq_line(parts, 30, buff=0.2)
            line.move_to([0, -0.45, 0])
            return line

        def swap_sum(new, rt=0.12):
            anims = [FadeIn(new)]
            if st["sum"] is not None:
                anims.append(FadeOut(st["sum"]))
            st["sum"] = new
            self.beat(*anims, rt=rt)

        def move_bar(k0, k1=None, color=MC_YELLOW, rt=0.12):
            self.beat(Transform(bar, line_bar(code, k0, k1, color)), rt=rt)

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("row_in", "target_t", "ends", "toast", "answer_t")]
        for k, e in enumerate(W["checks"]):
            for kind in ("fix", "sum_t", "found", "move_t"):
                if kind in e:
                    ev.append((seg_time(W["first"], e[kind]), kind, k))
        ev.append((seg_time(W["first"], W["skip"]["fix"]), "skip_fix", None))
        ev.append((seg_time(W["first"], W["skip"]["skip_t"]), "skip", None))
        ev.sort(key=lambda x: x[0])

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(tsign), rt=0.35)

        def on(kind, k):
            e = W["checks"][k] if k is not None else None
            if kind == "row_in":
                for i in range(6):
                    self.sfx(f"stone_dig{i % 4 + 1}", 0.26, delay=0.12 * i + 0.35)
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.5)
            elif kind == "target_t":
                self.sfx("wood_dig2", 0.35)
                self.beat(FadeIn(bar), pulse(tsign, 1.12), rt=0.4)
            elif kind == "fix":
                self.sfx("click", 0.3)
                # A new i lights its loop too; a new j only its own loop
                move_bar(3 if e["i"] != st.get("i") else 5, 7, MC_GOLD, rt=0.2)
                st["i"] = e["i"]
                if st["sum"] is not None:
                    self.beat(FadeOut(st["sum"]), rt=0.1)
                    st["sum"] = None
            elif kind == "sum_t":
                self.sfx(f"stone_step{k % 6 + 1}", 0.3)
                move_bar(9, rt=0.08)
                swap_sum(sum_line(e))
            elif kind == "move_t":
                self.sfx("stone_step2", 0.28)
                if e["verdict"] == "small":
                    move_bar(10, None, MC_AQUA)
                else:
                    move_bar(11, None, MC_PINK)
            elif kind == "found":
                g = group_chat([NUMS[e[q]] for q in ("i", "j", "l", "r")], MC_GREEN, 36)
                g.move_to([-2.85 + 2.85 * len(found), -1.25, 0])
                found.append(g)
                for d in (0.0, 0.18, 0.36):
                    self.sfx("orb", 0.28, delay=d)
                self.sfx("chestclosed", 0.22, delay=0.5)
                self.beat(Transform(bar, line_bar(code, 13, 15, MC_GREEN)), FadeIn(g, shift=UP * 0.15), rt=0.3)
            elif kind == "skip_fix":
                self.sfx("click", 0.3)
                move_bar(5, None, MC_GOLD, rt=0.2)
                if st["sum"] is not None:
                    self.beat(FadeOut(st["sum"]), rt=0.1)
                    st["sum"] = None
            elif kind == "skip":
                self.sfx("villager_no2", 0.35)
                move_bar(6, None, MC_RED, rt=0.2)
            elif kind == "ends":
                self.beat(FadeOut(st["sum"]), Transform(bar, line_bar(code, 8, 8, MC_GRAY)), rt=0.3)
                st["sum"] = None
            elif kind == "toast":
                t = toast("Advancement Made!", "4Sum solved", w=4.6)
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(tsign), Transform(bar, line_bar(code, 16, 16, MC_GREEN)), rt=0.5)
            elif kind == "answer_t":
                self.beat(LaggedStart(*[pulse(g, 1.1) for g in found], lag_ratio=0.25), rt=0.8)

        def on_last():
            # The 3D clip fades to sky at its end; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        loops = MT("2 fixed loops x 1 sweep", 46, MC_GRAY)
        loops.move_to([0, 3.4, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n^3)", 1.05)).arrange(RIGHT, buff=0.4)
        tm.move_to([0, 2.1, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 1.0, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(loops, shift=UP * 0.15), rt=0.5)
        self.until(at(16, "That's"))
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.4)
        self.add(xp)
        for d in (0.0, 0.3):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=0.6)
        self.beat(Restore(xp), rt=0.8)
        self.close_seg()

        old = big_o_pow("n", 4, 44, MC_RED)
        arrow = MT("->", 70, MC_GRAY)
        new = big_o_pow("n", 3, 44, MC_GREEN)
        cmp = VGroup(old, arrow, new).arrange(RIGHT, buff=0.45)
        cmp.move_to([0, -0.6, 0])
        strike = Line(old.get_left() + LEFT * 0.1, old.get_right() + RIGHT * 0.1, color=MC_RED, stroke_width=8)
        ptrs = VGroup(*[chat(s, PTR_COLORS[s], 46) for s in ("i", "j", "L", "R")]).arrange(RIGHT, buff=0.3)
        ptrs.move_to([0, -2.1, 0])
        sp = VGroup(MT("space", 56, MC_GRAY), level_text("O(1)", 1.05)).arrange(RIGHT, buff=0.4)
        sp.move_to([0, -3.4, 0])
        note = MT("besides the answer", 36, MC_GRAY)
        note.next_to(sp, DOWN, buff=0.25)

        self.seg(17)
        self.beat(FadeIn(old, shift=UP * 0.15), rt=0.4)
        self.until(at(17, "fourth") - 0.1)
        self.beat(Create(strike), FadeIn(arrow), FadeIn(new, shift=LEFT * 0.2), rt=0.5)
        self.until(at(17, "Besides") - 0.1)
        self.beat(FadeIn(note, shift=UP * 0.1), rt=0.35)
        self.until(at(17, "a few pointers") - 0.2)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(*[FadeIn(p, scale=0.6) for p in ptrs], lag_ratio=0.15), FadeIn(sp, shift=UP * 0.2), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.75, width=8.4, max_h=6.6)
        bar = line_bar(code, 3, 5, MC_GOLD)

        self.seg(18)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.04), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.2)
        self.until(at(18, "squeeze") - 0.1)
        self.beat(Transform(bar, line_bar(code, 8, 11, MC_AQUA)), rt=0.3)
        self.until(at(18, "skip duplicates") - 0.1)
        self.sfx("villager_no3", 0.3)
        skips = VGroup(*[line_bar(code, k, k, MC_RED) for k in (4, 6, 15)])
        self.beat(FadeTransform(bar, skips), rt=0.3)
        self.close_seg()

        self.seg(19)
        msg = chat("Works for any k sum", MC_GOLD, 56)
        msg.move_to([0, -2.75, 0])
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.4)
        self.until(DUR[19] - 1.45)
        self.beat(FadeOut(Group(code, skips, msg)), rt=0.4)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.9)
        self.close_seg()
