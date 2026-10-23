WALK = json.load(open('walk.json', encoding='utf-8'))
A, B = WALK["a"], WALK["b"]
STEPS = WALK["steps"]
MERGED = sorted([(v, "A") for v in A] + [(v, "B") for v in B])
TEX = {"A": "gold_ore", "B": "diamond_ore"}
COL = {"A": MC_GOLD, "B": MC_AQUA}

CODE = """def findMedianSortedArrays(A, B):
    if len(A) > len(B): A, B = B, A
    m, n = len(A), len(B)
    half = (m + n + 1) // 2
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i
        L1 = A[i - 1] if i > 0 else -inf
        R1 = A[i] if i < m else inf
        L2 = B[j - 1] if j > 0 else -inf
        R2 = B[j] if j < n else inf
        if L1 <= R2 and L2 <= R1:
            if (m + n) % 2: return max(L1, L2)
            return (max(L1, L2) + min(R1, R2)) / 2
        if L1 > R2: hi = i - 1
        else: lo = i + 1"""

# The loop alone, for the walk (ends past the arrays read as -inf and inf)
WALK_CODE = """half = (m + n + 1) // 2
lo, hi = 0, m
while lo <= hi:
    i = (lo + hi) // 2
    j = half - i
    L1, R1 = A[i - 1], A[i]
    L2, R2 = B[j - 1], B[j]
    if L1 <= R2 and L2 <= R1:
        return max(L1, L2)
    if L1 > R2: hi = i - 1
    else: lo = i + 1"""


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


def arr(values, tex, y, size=0.95, step=1.15, x0=-2.875):
    row = VGroup(*[Block(v, tex, size).move_to([x0 + k * step, y, 0]) for k, v in enumerate(values)])
    return row


def rows(ya, yb, size=0.95, step=1.15, x0=-2.875):
    a = arr(A, TEX["A"], ya, size, step, x0)
    b = arr(B, TEX["B"], yb, size, step, x0)
    labs = VGroup(MT("A", 44, MC_GOLD, PIXEL).move_to([x0 - 0.95, ya, 0]), MT("B", 44, MC_AQUA, PIXEL).move_to([x0 - 0.95, yb, 0]))
    return a, b, labs


def cut_x(row, c):
    # x of a cut before index c (0 = before everything, len = after everything)
    if c <= 0:
        return row[0].get_left()[0] - 0.12
    if c >= len(row):
        return row[-1].get_right()[0] + 0.12
    return (row[c - 1].get_right()[0] + row[c].get_left()[0]) / 2


def cut_bar(row, c, color=MC_RED):
    h = row[0].height * 1.35
    return Rectangle(width=0.1, height=h, fill_color=color, fill_opacity=1, stroke_width=0).move_to([cut_x(row, c), row[0].get_y(), 0])


def veil(m, opacity=0.65):
    # Dark cover that dims pixel art (set_opacity would fill the blocks' invisible edge squares with white)
    return Rectangle(width=m.width + 0.1, height=m.height + 0.1, fill_color="#000000", fill_opacity=opacity,
                     stroke_width=0).move_to(m)


def merged_row(y, size=0.62, step=0.7):
    x0 = -step * (len(MERGED) - 1) / 2
    return VGroup(*[Block(v, TEX[s], size).move_to([x0 + k * step, y, 0]) for k, (v, s) in enumerate(MERGED)])


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("MEDIAN OF TWO", width=7.4).move_to([0, 4.85, 0])
    t2 = stone_title("SORTED ARRAYS", width=7.8).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    a, b, labs = rows(1.55, 0.35, size=0.8, step=1.0, x0=-2.3)
    cuts = VGroup(cut_bar(a, 4), cut_bar(b, 2))
    med = outline(b[1], MC_GOLD, 8)
    tags = VGroup(chat("LeetCode #4", MC_AQUA, 42), chat("Hard", MC_RED, 42), chat("Binary Search", MC_GOLD, 42))
    tags.arrange(RIGHT, buff=0.2).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, a, b, labs, cuts, med, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, a, b, labs, cuts, med, tags = art
        self.add(art)

        self.seg(0)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        # Both rows hop like a wave, then the cut and the median flash
        self.sfx("stone_dig1", 0.35, delay=0.35)
        self.beat(LaggedStart(*[x.animate(rate_func=there_and_back).shift(UP * 0.3) for x in [*a, *b]], lag_ratio=0.1), rt=1.7)
        self.sfx("orb", 0.3, delay=0.2)
        self.beat(*[pulse(c, 1.3) for c in cuts], pulse(b[1], 1.25), ShowPassingFlash(med.copy().set_stroke(MC_YELLOW, 12),
                                                                                       time_width=0.6), rt=1.0)
        self.until(4.6)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        a, b, labs = rows(3.0, 1.7)
        goal = MT("median of all of them", 42, MC_WHITE).move_to([0, 0.55, 0])

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        # Blocks fall from the sky and bounce into place, A first
        blocks = [*a, *b]
        for x in blocks:
            x.shift(UP * 8)
        self.add(*blocks)
        for k in range(len(blocks)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.28, delay=k * 0.1 + 0.36)
        self.beat(LaggedStart(*[x.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for x in blocks],
                              lag_ratio=0.1), rt=1.9)
        self.beat(FadeIn(labs), rt=0.3)
        self.until(at(1, "median"))
        self.beat(FadeIn(goal, shift=UP * 0.15), rt=0.4)
        self.close_seg()

        mr = merged_row(-0.6)
        sixth = outline(mr[5], MC_GOLD, 8)
        lab6 = MT("6th", 36, MC_GOLD).next_to(mr[5], DOWN, buff=0.2)
        ans = chat("median = 11", MC_GOLD, 60).move_to([0, -2.4, 0])

        self.seg(2)
        self.beat(FadeOut(goal), rt=0.3)
        self.until(at(2, "eleven blocks") - 0.2)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(*[FadeIn(x, scale=0.5) for x in mr], lag_ratio=0.08), rt=1.0)
        self.until(at(2, "sixth"))
        self.sfx("click", 0.3)
        self.beat(Create(sixth), FadeIn(lab6), pulse(mr[5], 1.2), rt=0.5)
        self.until(at(2, "That's eleven"))
        self.sfx("orb", 0.3)
        self.beat(FadeIn(ans, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene3_Merge(Base):
    def construct(self):
        h = hdr("MERGE?", MC_RED)
        a, b, labs = rows(3.0, 1.7)
        mr = merged_row(-0.4)
        cost = VGroup(MT("time", 44, MC_GRAY), MT("O(m + n)", 44, MC_RED, PIXEL)).arrange(RIGHT, buff=0.35).move_to([0, -1.8, 0])

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(a), FadeIn(b), FadeIn(labs), rt=0.5)
        self.until(at(3, "merges") - 0.2)
        # Every block is copied into one sorted row, in order
        src = {("A", v): x for v, x in zip(A, a)}
        src.update({("B", v): x for v, x in zip(B, b)})
        flies = [src[(s, v)].copy() for v, s in MERGED]
        for k in range(0, len(MERGED), 2):
            self.sfx(f"stone_step{k % 6 + 1}", 0.25, delay=0.12 * k)
        self.beat(LaggedStart(*[Transform(f, mr[k]) for k, f in enumerate(flies)], lag_ratio=0.12), rt=1.6)
        self.until(at(3, "picks the middle"))
        self.beat(Create(outline(flies[5], MC_GOLD, 8)), rt=0.4)
        self.until(at(3, "linear") - 0.2)
        self.beat(FadeIn(cost, shift=UP * 0.15), rt=0.4)
        self.close_seg()

        need = VGroup(MT("asked for", 44, MC_GRAY), MT("O(log(m + n))", 44, MC_GOLD, PIXEL)).arrange(RIGHT, buff=0.35)
        need.move_to([0, -2.9, 0])
        cant = MT("no time to look at every block", 38, MC_RED).move_to([0, -4.0, 0])

        self.seg(4)
        self.until(at(4, "log time") - 0.3)
        self.beat(FadeIn(need, shift=UP * 0.15), rt=0.4)
        self.until(at(4, "can't") - 0.1)
        self.sfx("villager_no1", 0.4)
        self.beat(FadeIn(veil(VGroup(*flies[:5])), veil(VGroup(*flies[6:]))), FadeIn(cant, shift=UP * 0.1), rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        mr = merged_row(3.6)
        mid = Rectangle(width=0.08, height=0.85, fill_color=MC_RED, fill_opacity=1, stroke_width=0)
        mid.move_to([(mr[5].get_right()[0] + mr[6].get_left()[0]) / 2, 3.6, 0])
        ll = MT("left half", 38, MC_GOLD).move_to([-1.9, 2.75, 0])
        rl = MT("right half", 38, MC_AQUA).move_to([2.1, 2.75, 0])

        self.seg(5)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(mr), rt=0.5)
        self.until(at(5, "splits") - 0.1)
        self.sfx("stone_step2", 0.35)
        self.beat(GrowFromCenter(mid), rt=0.4)
        self.until(at(5, "left half"))
        self.beat(FadeIn(ll, shift=UP * 0.1), rt=0.35)
        self.until(at(5, "right half"))
        self.beat(FadeIn(rl, shift=UP * 0.1), rt=0.35)
        self.close_seg()

        a, b, labs = rows(1.15, -0.25)
        ca, cb = cut_bar(a, 1), cut_bar(b, 5)
        il = MT("i", 40, MC_RED, PIXEL).next_to(ca, UP, buff=0.12)
        jl = MT("j", 40, MC_RED, PIXEL).next_to(cb, DOWN, buff=0.12)
        rule = eq_line([("i", MC_GOLD), ("+", MC_GRAY), ("j", MC_AQUA), ("=", MC_GRAY), ("6", MC_WHITE)], 50, buff=0.3)
        rule.move_to([0, -1.75, 0])

        def move_cut(i, rt=0.4):
            na, nb = cut_bar(a, i), cut_bar(b, 6 - i)
            self.sfx("stone_step3", 0.3)
            self.beat(Transform(ca, na), Transform(cb, nb), il.animate.next_to(na, UP, buff=0.12),
                      jl.animate.next_to(nb, DOWN, buff=0.12), rt=rt)

        self.seg(6)
        self.beat(FadeIn(a), FadeIn(b), FadeIn(labs), rt=0.5)
        self.until(at(6, "cut row A"))
        self.sfx("stone_step1", 0.35)
        self.beat(GrowFromCenter(ca), FadeIn(il), rt=0.4)
        self.until(at(6, "the cut in B"))
        self.beat(GrowFromCenter(cb), FadeIn(jl), rt=0.4)
        self.until(at(6, "left side") - 0.2)
        self.beat(FadeIn(rule, shift=UP * 0.15), rt=0.4)
        for i in (2, 3):
            move_cut(i, rt=0.45)
            self.hold(0.25)
        self.close_seg()

        short = MT("A is shorter: search i from 0 to 5", 38, MC_GOLD).move_to([0, -2.9, 0])

        self.seg(7)
        dim = veil(b)
        self.beat(FadeIn(dim), pulse(a, 1.06), rt=0.6)
        self.beat(FadeIn(short, shift=UP * 0.15), rt=0.4)
        self.close_seg()

        self.seg(8)
        self.beat(FadeOut(dim), FadeOut(short), FadeOut(rule), FadeOut(mr), FadeOut(mid), FadeOut(ll),
                  FadeOut(rl), rt=0.4)
        move_cut(4, rt=0.5)
        names = VGroup(MT("L1", 34, MC_WHITE, PIXEL).next_to(a[3], UP, buff=0.15), MT("R1", 34, MC_WHITE, PIXEL).next_to(a[4], UP, buff=0.15),
                       MT("L2", 34, MC_WHITE, PIXEL).next_to(b[1], DOWN, buff=0.15),
                       MT("R2", 34, MC_WHITE, PIXEL).next_to(b[2], DOWN, buff=0.15))
        conds = VGroup(eq_line([("L1", MC_GOLD), ("≤", MC_GRAY), ("R2", MC_AQUA)], 46, buff=0.25),
                       eq_line([("L2", MC_AQUA), ("≤", MC_GRAY), ("R1", MC_GOLD)], 46, buff=0.25)).arrange(RIGHT, buff=1.2)
        conds.move_to([0, -2.4, 0])
        x1 = Arrow(a[3].get_bottom(), b[2].get_top(), buff=0.05, color=MC_GREEN, stroke_width=7)
        x2 = Arrow(b[1].get_top(), a[4].get_bottom(), buff=0.05, color=MC_GREEN, stroke_width=7)
        sorted_note = MT("inside each row it is already sorted", 34, MC_GRAY).move_to([0, -3.5, 0])
        self.until(at(8, "everything on the left") - 0.3)
        self.beat(FadeIn(names), rt=0.4)
        self.until(at(8, "at most") - 0.1)
        self.beat(FadeIn(conds, shift=UP * 0.15), rt=0.5)
        self.until(at(8, "Since") - 0.1)
        self.beat(FadeIn(sorted_note), rt=0.4)
        self.until(at(8, "across the cut") - 0.3)
        self.sfx("orb", 0.3)
        self.beat(GrowArrow(x1), GrowArrow(x2), rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("CUT SEARCH", MC_GREEN)
        code = code_panel(WALK_CODE, -4.35, max_h=3.25)
        bar = line_bar(code, 1, 1, MC_YELLOW)
        st = {"badge": None, "ij": None, "c1": None, "c2": None}

        def badge(lo, hi):
            return chat(f"lo {lo}  hi {hi}", MC_YELLOW, 42).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)

        def ij_text(i, j=None):
            parts = [("i =", MC_GOLD), (str(i), MC_WHITE)] + ([("j =", MC_AQUA), (str(j), MC_WHITE)] if j is not None else [])
            return eq_line(parts, 46, buff=0.3).move_to([0, -0.35, 0])

        def check_text(name_l, vl, name_r, vr, ok, y):
            mark = "ok" if ok else "no!"
            return eq_line([(f"{name_l} {vl}", MC_WHITE), ("≤" if ok else ">", MC_GREEN if ok else MC_RED), (f"{name_r} {vr}", MC_WHITE),
                            (mark, MC_GREEN if ok else MC_RED)], 40, buff=0.35).move_to([0, y, 0])

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("row_in", "range", "toast", "odd", "largest", "answer")]
        for k, s in enumerate(STEPS):
            for kind in ("cutA", "cutB", "sides", "chk1", "chk2", "move", "valid"):
                if kind in s:
                    ev.append((seg_time(W["first"], s[kind]), kind, k))
        ev.sort(key=lambda e: e[0])

        def move_bar(k0, color=MC_YELLOW, rt=0.15):
            self.beat(Transform(bar, line_bar(code, k0, k0, color)), rt=rt)

        def swap(key, new, rt=0.25):
            anims = [FadeIn(new, shift=UP * 0.1)]
            if st[key] is not None:
                anims.append(FadeOut(st[key]))
            st[key] = new
            self.beat(*anims, rt=rt)

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.35)

        def on(kind, k):
            s = STEPS[k] if k is not None else None
            if kind == "row_in":
                for q in range(len(A) + len(B)):
                    self.sfx(f"stone_dig{q % 4 + 1}", 0.26, delay=0.35 + 0.1 * (q % 6) + (0.6 if q >= len(A) else 0))
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
            elif kind == "range":
                st["badge"] = badge(0, 5)
                self.beat(FadeIn(st["badge"], shift=LEFT * 0.2), FadeIn(bar), rt=0.4)
            elif kind == "cutA":
                self.sfx("stone_step1", 0.4)
                move_bar(3)
                if k:
                    for key in ("c1", "c2"):
                        if st[key] is not None:
                            self.beat(FadeOut(st[key]), rt=0.15)
                            st[key] = None
                swap("ij", ij_text(s["i"]))
            elif kind == "cutB":
                self.sfx("stone_step2", 0.4)
                move_bar(4)
                swap("ij", ij_text(s["i"], s["j"]))
            elif kind == "sides":
                self.sfx("pop", 0.3)
                move_bar(5, rt=0.15)
                move_bar(6, rt=0.15)
            elif kind == "chk1":
                self.sfx("click", 0.3)
                move_bar(7, rt=0.12)
                swap("c1", check_text("L1", s["L1"], "R2", s["R2"], s["ok1"], -1.15))
            elif kind == "chk2":
                self.sfx("click" if s["ok2"] else "villager_no2", 0.3 if s["ok2"] else 0.35)
                swap("c2", check_text("L2", s["L2"], "R1", s["R1"], s["ok2"], -1.95))
                if not s["ok2"]:
                    move_bar(7, MC_RED, rt=0.12)
            elif kind == "move":
                self.sfx("stone_step4", 0.4)
                move_bar(10, MC_YELLOW)
                self.beat(Transform(st["badge"], badge(s["i"] + 1, s["hi"])), rt=0.3)
            elif kind == "valid":
                for d in (0.0, 0.2):
                    self.sfx("orb", 0.3, delay=d)
                move_bar(7, MC_GREEN, rt=0.2)
            elif kind == "toast":
                t = toast("Advancement Made!", "Median found", w=4.6)
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(st["badge"]), rt=0.5)
            elif kind == "odd":
                move_bar(8, MC_GREEN, rt=0.2)
                for key in ("c1", "c2"):
                    self.beat(FadeOut(st[key]), rt=0.12)
                    st[key] = None
                swap("ij", eq_line([("max(9, 11)", MC_WHITE), ("=", MC_GRAY), ("?", MC_GOLD)], 46).move_to([0, -0.8, 0]))
            elif kind == "largest":
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                swap("ij", eq_line([("max(9, 11)", MC_WHITE), ("=", MC_GRAY), ("11", MC_GOLD)], 46).move_to([0, -0.8, 0]))
            elif kind == "answer":
                swap("ij", chat("return 11", MC_GREEN, 60).move_to([0, -0.9, 0]), rt=0.3)

        def on_last():
            # The rows leave the 3D clip when the walk ends; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        a = arr(A, TEX["A"], 3.5, size=0.8, step=1.0, x0=-2.0)
        rng = Rectangle(width=a.width + 0.3, height=1.1, stroke_color=MC_YELLOW, stroke_width=6).move_to(a)
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(log min(m, n))", 0.75)).arrange(RIGHT, buff=0.4).move_to([0, 1.85, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.95, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        def span(i0, i1):
            g = VGroup(*a[i0:i1 + 1])
            return Rectangle(width=g.width + 0.3, height=1.1, stroke_color=MC_YELLOW, stroke_width=6).move_to(g)

        self.seg(15)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(a), Create(rng), rt=0.6)
        # The search range halves each step: 0..4, then 3..4, then 4
        self.sfx("click", 0.25)
        self.beat(Transform(rng, span(3, 4)), rt=0.4)
        self.sfx("click", 0.25)
        self.beat(Transform(rng, span(4, 4)), rt=0.4)
        self.until(at(15, "log") - 0.3)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.4)
        self.add(xp)
        self.sfx("orb", 0.25)
        self.sfx("levelup", 0.3, delay=0.5)
        # Only a short fill: log time is tiny
        self.beat(Restore(xp), rt=0.6)
        self.close_seg()

        ptrs = VGroup(*[chat(s, MC_WHITE, 46) for s in ("lo", "hi", "i", "j")]).arrange(RIGHT, buff=0.3).move_to([0, -1.1, 0])
        sp = VGroup(MT("space", 56, MC_GRAY), level_text("O(1)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, -2.6, 0])

        self.seg(16)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(*[FadeIn(p, scale=0.6) for p in ptrs], lag_ratio=0.2), rt=0.7)
        self.until(at(16, "constant") - 0.4)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.3, width=8.4, max_h=7.4)
        bar = line_bar(code, 6, 7, MC_GOLD)

        self.seg(17)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.04), FadeIn(code.line_numbers),
                  rt=0.7)
        self.until(at(17, "one cut") - 0.1)
        self.beat(FadeIn(bar), rt=0.3)
        self.until(at(17, "checked") - 0.1)
        self.beat(Transform(bar, line_bar(code, 12, 12, MC_GREEN)), rt=0.35)
        self.close_seg()

        self.seg(18)
        msg = chat("Find the right cut", MC_GOLD, 60)
        msg.move_to([0, -3.6, 0])
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.4)
        self.until(0.85)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.45)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.9)
        self.close_seg()
