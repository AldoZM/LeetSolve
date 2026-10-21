WALK = json.load(open('walk.json', encoding='utf-8'))
NODES = WALK["nodes"]
TRACE = WALK["trace"]
BEST = WALK["best_path"]
WOOD = "#9C7A48"
DROP = "#7A2020"

CODE = """def maxPathSum(root):
    best = -inf
    def gain(node):
        nonlocal best
        if not node: return 0
        left = max(gain(node.left), 0)
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)
        return node.val + max(left, right)
    gain(root)
    return best"""


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


class Tree2D(VGroup):
    """The tree as ore blocks joined by wooden rods; blocks[i] is node i, rods[i] joins node i to its parent."""

    def __init__(self, size, top, dy, sx, x0=0.0, **kwargs):
        super().__init__(**kwargs)
        self.pos = [np.array([x0 + n["x"] * sx, top - n["lvl"] * dy, 0]) for n in NODES]
        self.rods = {i: Line(self.pos[n["parent"]], self.pos[i], color=WOOD, stroke_width=11 * size)
                     for i, n in enumerate(NODES) if n["parent"] is not None}
        self.blocks = VGroup(*[Block(n["val"], f"{n['ore']}_ore", size).move_to(self.pos[i]) for i, n in enumerate(NODES)])
        # Rods first, so the blocks are drawn on top of them
        self.add(VGroup(*self.rods.values()), self.blocks)

    def path_marks(self, ids, color, width=8):
        # Outlines on the blocks of a path
        return VGroup(*[outline(self.blocks[i], color, width) for i in ids])


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("MAXIMUM", width=5.6).move_to([0, 4.85, 0])
    t2 = stone_title("PATH SUM", width=6.4).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    tree = Tree2D(0.75, 1.75, 0.95, 0.75)
    marks = tree.path_marks(BEST, MC_GOLD)
    best = chat("15 + 20 + 7 = 42", MC_GOLD, 46).move_to([0, -1.45, 0])
    tags = VGroup(chat("LeetCode #124", MC_AQUA, 46), chat("Hard", MC_RED, 46), chat("Tree DFS", MC_GOLD, 46))
    tags.arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, tree, marks, best, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, tree, marks, best, tags = art
        self.add(art)

        self.seg(0)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        # The leaves hop first, then the levels above them: the order the algorithm works in
        self.sfx("stone_dig1", 0.3, delay=0.3)
        order = [3, 4, 1, 5, 6, 2, 0]
        self.beat(LaggedStart(*[tree.blocks[i].animate(rate_func=there_and_back).shift(UP * 0.3) for i in order], lag_ratio=0.2),
                  rt=1.8)
        self.sfx("orb", 0.3)
        self.beat(*[pulse(tree.blocks[i], 1.2) for i in BEST], pulse(best, 1.1), rt=0.9)
        self.until(4.9)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        tree = Tree2D(0.9, 4.0, 1.25, 1.0)
        some = tree.path_marks([4, 1, 0, 2, 5], MC_AQUA)
        rule = MT("connected, each block once", 40, MC_WHITE).move_to([0, -0.4, 0])
        goal = MT("largest sum wins", 44, MC_GOLD).move_to([0, -1.3, 0])

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        blocks = list(tree.blocks)
        for b in blocks:
            b.shift(UP * 7)
        self.add(*blocks)
        for k in range(len(blocks)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.28, delay=k * 0.12 + 0.4)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 7) for b in blocks],
                              lag_ratio=0.12), rt=1.6)
        self.add(tree[0], *blocks)
        self.beat(Create(tree[0]), rt=0.4)
        self.until(at(1, "chain") - 0.2)
        self.beat(Create(some), FadeIn(rule, shift=UP * 0.1), rt=0.6)
        self.until(at(1, "largest") - 0.2)
        self.beat(FadeIn(goal, shift=UP * 0.1), rt=0.4)
        self.close_seg()

        best = tree.path_marks(BEST, MC_GOLD, 10)
        eq = chat("15 + 20 + 7 = 42", MC_GOLD, 56).move_to([0, -2.6, 0])
        nr = MT("not through the root", 38, MC_RED).next_to(tree.blocks[0], RIGHT, buff=0.35)

        self.seg(2)
        self.beat(FadeOut(some), FadeOut(rule), FadeOut(goal), rt=0.35)
        self.until(at(2, "root") - 0.3)
        self.beat(FadeIn(nr, shift=LEFT * 0.1), rt=0.4)
        self.until(at(2, "fifteen") - 0.2)
        self.sfx("pop", 0.35)
        self.beat(Create(best), *[pulse(tree.blocks[i], 1.15) for i in BEST], rt=0.6)
        self.until(at(2, "forty two") - 0.4)
        self.sfx("orb", 0.35)
        self.beat(FadeIn(eq, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("EVERY PAIR?", MC_RED)
        tree = Tree2D(0.8, 4.0, 1.1, 0.9)
        pairs = [(a, b) for a in range(len(NODES)) for b in range(a + 1, len(NODES))]
        line = Line(tree.pos[0], tree.pos[1], color=MC_RED, stroke_width=6)
        cnt = MT("pairs 0", 40, MC_WHITE, PIXEL).move_to([0, 0.1, 0])
        o = big_o_pow("n", 2, 64, MC_RED).move_to([0, -1.3, 0])
        cost = MT("pairs, times a walk for each", 36, MC_GRAY).move_to([0, -2.4, 0])

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(tree), rt=0.5)
        self.add(line, cnt)
        for k, (a, b) in enumerate(pairs[:14]):
            self.sfx("click", 0.15)
            self.beat(Transform(line, Line(tree.pos[a], tree.pos[b], color=MC_RED, stroke_width=6)),
                      Transform(cnt, MT(f"pairs {k + 1}", 40, MC_WHITE, PIXEL).move_to([0, 0.1, 0])), rt=0.1)
        self.beat(Transform(cnt, MT(f"pairs {len(pairs)}", 40, MC_WHITE, PIXEL).move_to([0, 0.1, 0])), rt=0.2)
        self.sfx("villager_no1", 0.35)
        self.beat(FadeIn(o, scale=0.5), FadeIn(cost), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        tree = Tree2D(0.9, 4.0, 1.25, 1.0)
        top = outline(tree.blocks[2], MC_GOLD, 10)
        crown = MT("top", 40, MC_GOLD).next_to(tree.blocks[2], UP, buff=0.2)
        lft = outline(tree.blocks[5], MC_AQUA, 8)
        rgt = outline(tree.blocks[6], MC_AQUA, 8)
        eq = eq_line([("top", MC_GOLD), ("+", MC_GRAY), ("best left", MC_AQUA), ("+", MC_GRAY), ("best right", MC_AQUA)], 34, TERM, 0.25)
        eq.move_to([0, -0.4, 0])

        self.seg(4)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(tree), rt=0.5)
        self.until(at(4, "top of a path") - 0.2)
        self.sfx("click", 0.3)
        self.beat(Create(top), FadeIn(crown, shift=DOWN * 0.1), rt=0.5)
        self.until(at(4, "best branch on the left") - 0.2)
        self.beat(Create(lft), FadeIn(eq[:3]), rt=0.5)
        self.until(at(4, "on the right") - 0.2)
        self.beat(Create(rgt), FadeIn(eq[3:]), rt=0.5)
        self.close_seg()

        up = Arrow(tree.pos[2] + UP * 0.5, tree.pos[0] + RIGHT * 0.5, color=MC_GREEN, stroke_width=8, buff=0.3)
        once = eq_line([("offer up", MC_GREEN), ("=", MC_GRAY), ("top + max(left, right)", MC_WHITE)], 34, TERM, 0.25)
        once.move_to([0, -1.5, 0])
        bend = MT("a path bends only once", 38, MC_RED).move_to([0, -2.5, 0])

        self.seg(5)
        self.until(at(5, "bend once") - 0.2)
        self.beat(FadeIn(bend, shift=UP * 0.1), rt=0.4)
        self.until(at(5, "reports up") - 0.2)
        self.sfx("orb", 0.3)
        self.beat(GrowArrow(up), FadeIn(once, shift=UP * 0.1), FadeOut(rgt), rt=0.6)
        self.close_seg()

        neg = tree.rods[3]
        bar = pixel_art("barrier", 0.55).move_to(neg.get_center())
        rule = eq_line([("gain", MC_WHITE), ("=", MC_GRAY), ("max(branch, 0)", MC_GOLD)], 40, TERM, 0.25).move_to([0, -3.6, 0])

        self.seg(6)
        self.beat(FadeOut(VGroup(top, crown, lft, eq, up, once, bend)), rt=0.35)
        self.until(at(6, "negative") - 0.2)
        self.sfx("villager_no2", 0.35)
        self.beat(neg.animate.set_stroke(DROP), FadeIn(bar, scale=1.5), pulse(tree.blocks[3], 1.2), rt=0.5)
        self.until(at(6, "zero") - 0.4)
        self.beat(FadeIn(rule, shift=UP * 0.15), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("POST ORDER", MC_GREEN)
        code = code_panel(CODE, -4.3, max_h=3.1)
        bar = line_bar(code, 4, 4, MC_YELLOW)
        st = {"badge": None, "path": None, "ret": None}

        def badge(v):
            return chat(f"best {v}", MC_GOLD, 42).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)

        def path_text(e):
            parts = [(str(e["val"]), MC_WHITE), ("+", MC_GRAY), (str(e["left"]), MC_AQUA), ("+", MC_GRAY), (str(e["right"]), MC_AQUA),
                     ("=", MC_GRAY), (str(e["path"]), MC_GOLD)]
            return VGroup(MT("path", 40, MC_GRAY), eq_line(parts, 40, buff=0.22)).arrange(RIGHT, buff=0.35).move_to([0, -0.6, 0])

        def ret_text(e):
            c = MC_GREEN if e["ret"] > 0 else MC_RED
            return VGroup(MT("offers", 40, MC_GRAY), eq_line([(str(e["ret"]), c)] + ([("dropped", MC_RED)] if e["ret"] <= 0 else []),
                                                              40, buff=0.3)).arrange(RIGHT, buff=0.35).move_to([0, -1.5, 0])

        def swap(key, new, rt=0.2):
            anims = [FadeIn(new)]
            if st[key] is not None:
                anims.append(FadeOut(st[key]))
            st[key] = new
            self.beat(*anims, rt=rt)

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("tree_in", "leaves", "stays", "toast", "show")]
        for k, e in enumerate(TRACE):
            for kind in ("visit", "path", "best", "ret"):
                if kind in e["t"] and not (kind == "path" and e["t"]["path"] == e["t"]["visit"]):
                    ev.append((seg_time(W["first"], e["t"][kind]), kind, k))
        ev.sort(key=lambda x: x[0])

        def move_bar(k0, k1=None, color=MC_YELLOW, rt=0.12):
            self.beat(Transform(bar, line_bar(code, k0, k1, color)), rt=rt)

        def on_first():
            st["badge"] = badge("-inf")
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(st["badge"]), rt=0.35)

        def on(kind, k):
            e = TRACE[k] if k is not None else None
            if kind == "tree_in":
                for i in range(len(NODES)):
                    self.sfx(f"stone_dig{i % 4 + 1}", 0.25, delay=0.12 * i + 0.4)
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.5)
            elif kind == "leaves":
                self.beat(FadeIn(bar), rt=0.2)
            elif kind == "visit":
                self.sfx("click", 0.25)
                move_bar(5, 6, MC_YELLOW, rt=0.15)
                if e["t"]["path"] == e["t"]["visit"]:
                    move_bar(7, None, MC_GOLD, rt=0.1)
                    swap("path", path_text(e), rt=0.15)
            elif kind == "path":
                move_bar(7, None, MC_GOLD, rt=0.15)
                swap("path", path_text(e), rt=0.2)
            elif kind == "best":
                self.sfx("orb", 0.3)
                self.beat(Transform(st["badge"], badge(e["best"])), rt=0.2)
            elif kind == "ret":
                self.sfx("pop" if e["ret"] > 0 else "villager_no2", 0.32)
                move_bar(8, None, MC_GREEN if e["ret"] > 0 else MC_RED, rt=0.12)
                swap("ret", ret_text(e), rt=0.18)
            elif kind == "stays":
                self.beat(pulse(st["badge"], 1.15), rt=0.4)
            elif kind == "toast":
                t = toast("Advancement Made!", "Best path: 42", w=4.6)
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(st["badge"]), Transform(bar, line_bar(code, 10, 10, MC_GREEN)), rt=0.5)
            elif kind == "show":
                swap("path", chat("15 + 20 + 7 = 42", MC_GOLD, 56).move_to([0, -0.9, 0]), rt=0.3)
                self.beat(FadeOut(st["ret"]), rt=0.2)
                st["ret"] = None

        def on_last():
            # The tree leaves the 3D clip when the walk ends; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        tree = Tree2D(0.75, 4.0, 0.95, 0.8)
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, 0.75, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, -0.15, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(14)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(tree), rt=0.4)
        self.sfx("click", 0.25)
        self.beat(LaggedStart(*[pulse(tree.blocks[e["node"]], 1.2) for e in TRACE], lag_ratio=0.18), rt=1.1)
        self.until(at(14, "linear") - 0.5)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.3)
        self.add(xp)
        self.sfx("orb", 0.25)
        self.sfx("levelup", 0.3, delay=0.4)
        self.beat(Restore(xp), rt=0.5)
        self.close_seg()

        stack = tree.path_marks([0, 2, 5], MC_YELLOW)
        sp = VGroup(MT("space", 56, MC_GRAY), level_text("O(h)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, -1.9, 0])
        hh = MT("h = height of the tree = 3", 36, MC_WHITE).move_to([0, -3.0, 0])

        self.seg(15)
        self.until(at(15, "deep") - 0.3)
        self.sfx("stone_step1", 0.3)
        self.beat(LaggedStart(*[Create(m) for m in stack], lag_ratio=0.3), rt=0.6)
        self.until(at(15, "height") - 0.6)
        self.beat(FadeIn(sp, shift=UP * 0.2), FadeIn(hh), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.6, width=8.4)
        bar = line_bar(code, 8, 8, MC_GREEN)

        self.seg(16)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.06), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(at(16, "score both") - 0.1)
        self.beat(Transform(bar, line_bar(code, 7, 7, MC_GOLD)), rt=0.35)
        self.close_seg()

        self.seg(17)
        msg = chat("Bend once at the top", MC_GOLD, 58)
        msg.move_to([0, -2.3, 0])
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.35)
        self.until(1.0)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.4)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.9)
        self.close_seg()
