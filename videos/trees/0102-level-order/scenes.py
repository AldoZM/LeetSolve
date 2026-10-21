WALK = json.load(open('walk.json', encoding='utf-8'))
NODES = WALK["nodes"]
LEVELS = WALK["levels"]
EVENTS = WALK["events"]
WOOD = "#9C7A48"
LEVEL_VALS = [[NODES[i]["val"] for i in ids] for ids in LEVELS]

CODE = """def levelOrder(root):
    res, queue = [], deque([root] if root else [])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            for kid in (node.left, node.right):
                if kid: queue.append(kid)
        res.append(level)
    return res"""


def at(i, phrase, nth=0):
    # Seconds into line i where the nth `phrase` starts (even speaking rate inside a line)
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
    return min(dur - 0.1, dur * k / len(text))


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def pulse(m, k=1.15):
    # Emphasis that keeps the pixel art's colors (Indicate would paint it one flat color)
    return m.animate(rate_func=there_and_back).scale(k)


def lvl_str(vals):
    return "[" + ", ".join(str(v) for v in vals) + "]"


class Tree2D(VGroup):
    """The tree as ore blocks joined by wooden rods; blocks[i] is node i."""

    def __init__(self, size, top, dy, sx, x0=0.0, **kwargs):
        super().__init__(**kwargs)
        self.pos = [np.array([x0 + n["x"] * sx, top - n["lvl"] * dy, 0]) for n in NODES]
        self.rods = VGroup(*[Line(self.pos[n["parent"]], self.pos[i], color=WOOD, stroke_width=11 * size)
                             for i, n in enumerate(NODES) if n["parent"] is not None])
        self.blocks = VGroup(*[Block(n["val"], f"{n['ore']}_ore", size).move_to(self.pos[i]) for i, n in enumerate(NODES)])
        # Rods first, so the blocks are drawn on top of them
        self.add(self.rods, self.blocks)

    def level(self, L):
        return VGroup(*[self.blocks[i] for i in LEVELS[L]])


def queue_item(inv, k, i):
    # Node i in queue slot k: its ore block, with its value where the game prints stack counts
    n = NODES[i]
    u = inv.u
    icon = iso_block(f"{n['ore']}_ore", 16 * u)
    val = gui_text(str(n["val"]), MC_WHITE, u * 1.15)
    val.move_to(icon.get_corner(DR) + np.array([1 * u, 0.5 * u, 0]), aligned_edge=DR)
    return VGroup(icon, val).move_to(inv.slots[k])


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("LEVEL ORDER", width=7.2).move_to([0, 4.85, 0])
    t2 = stone_title("TRAVERSAL", width=6.6).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    tree = Tree2D(0.7, 1.95, 0.78, 0.62)
    rows = chat("  ".join(lvl_str(v) for v in LEVEL_VALS), MC_GOLD, 36).move_to([0, -1.55, 0])
    tags = VGroup(chat("LeetCode #102", MC_AQUA, 46), chat("Medium", MC_GOLD, 46), chat("BFS", MC_GREEN, 46))
    tags.arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, tree, rows, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, tree, rows, tags = art
        self.add(art)

        self.seg(0)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.7)
        # The tree hops one level at a time, top to bottom
        self.sfx("stone_dig1", 0.3, delay=0.25)
        self.beat(LaggedStart(*[AnimationGroup(*[b.animate(rate_func=there_and_back).shift(UP * 0.3) for b in tree.level(L)])
                                for L in range(len(LEVELS))], lag_ratio=0.35), rt=1.6)
        self.sfx("orb", 0.3)
        self.beat(pulse(rows, 1.08), rt=0.7)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.7)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        tree = Tree2D(0.85, 4.05, 1.0, 0.78)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        blocks = list(tree.blocks)
        for b in blocks:
            b.shift(UP * 7)
        self.add(*blocks)
        for k in range(len(blocks)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.28, delay=k * 0.1 + 0.4)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 7) for b in blocks],
                              lag_ratio=0.1), rt=1.7)
        # Rods go behind the blocks: added first, then the blocks re-added on top
        self.add(tree.rods, *blocks)
        self.beat(Create(tree.rods), rt=0.4)
        self.until(at(1, "level by level"))
        self.beat(*[pulse(tree.level(L), 1.06) for L in range(len(LEVELS))], rt=0.6)
        self.close_seg()

        rows = VGroup(*[chat(lvl_str(v), MC_GOLD, 48) for v in LEVEL_VALS]).arrange(DOWN, buff=0.22).move_to([0, -1.9, 0])
        cues = ["three", "nine and", "four, seven", "six and"]

        self.seg(2)
        for L, cue in enumerate(cues):
            self.until(at(2, cue) - (0.5 if L == 3 else 0.15))
            self.sfx("click", 0.3)
            self.beat(FadeIn(rows[L], shift=RIGHT * 0.2), *[pulse(b, 1.15) for b in tree.level(L)], rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene3_DFS(Base):
    def construct(self):
        h = hdr("DEPTH FIRST?", MC_RED)
        tree = Tree2D(0.85, 4.05, 1.0, 0.78)
        order = [0, 1, 3, 4, 7, 2, 5, 8, 6]
        cur = outline(tree.blocks[0], MC_YELLOW, 8)
        seq = chat(" ".join(str(NODES[i]["val"]) for i in order), MC_RED, 48).move_to([0, -0.4, 0])
        want = chat(" ".join(str(v) for vals in LEVEL_VALS for v in vals), MC_GREEN, 48).move_to([0, -1.6, 0])

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(tree), rt=0.5)
        self.until(at(3, "dives") - 0.2)
        self.beat(Create(cur), rt=0.2)
        # Straight down the left branch first
        for i in order[1:]:
            self.sfx("click", 0.22)
            self.beat(cur.animate.move_to(tree.blocks[i]), rt=0.22)
        self.beat(FadeIn(seq, shift=UP * 0.15), rt=0.35)
        self.until(at(3, "wrong order") - 0.2)
        self.sfx("villager_no1", 0.4)
        self.beat(FadeIn(want, shift=UP * 0.15), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene4_BFS(Base):
    def construct(self):
        h = hdr("BREADTH FIRST", MC_GOLD)
        tree = Tree2D(0.85, 4.05, 1.0, 0.78)

        def band(L):
            ys = tree.pos[LEVELS[L][0]][1]
            return Rectangle(width=8.4, height=1.0, stroke_color=MC_YELLOW, stroke_width=6, fill_color=MC_YELLOW,
                             fill_opacity=0.08).move_to([0, ys, 0])

        sweep = band(0)

        self.seg(4)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(tree), rt=0.5)
        self.until(at(4, "sweep") - 0.2)
        self.beat(Create(sweep), rt=0.3)
        for L in range(1, len(LEVELS)):
            self.sfx("stone_step%d" % L, 0.3)
            self.beat(Transform(sweep, band(L)), rt=0.45)
        self.close_seg()

        inv = Inventory(9, "Queue")
        inv.move_to([0, -0.9, 0])
        inn = MT("in", 40, MC_GREEN).next_to(inv, RIGHT, buff=0.1).shift(UP * 0.0)
        out = MT("out", 40, MC_GOLD).next_to(inv, DOWN, buff=0.15).align_to(inv, LEFT).shift(RIGHT * 0.2)
        items = [queue_item(inv, k, i) for k, i in enumerate([1, 2])]

        self.seg(5)
        self.beat(FadeOut(sweep), FadeIn(inv, shift=UP * 0.3), rt=0.5)
        self.until(at(5, "First in") - 0.2)
        self.sfx("pop", 0.3)
        self.beat(FadeIn(items[0], scale=1.5), FadeIn(inn), rt=0.35)
        self.sfx("pop", 0.3)
        self.beat(FadeIn(items[1], scale=1.5), rt=0.3)
        self.until(at(5, "first out") - 0.1)
        self.beat(FadeIn(out), items[0].animate.shift(UP * 0.5).set_opacity(0), items[1].animate.move_to(inv.slots[0]), rt=0.5)
        self.close_seg()

        # The snapshot: the queue holds level 1, and its length says how many nodes that level has
        snap = [queue_item(inv, k, i) for k, i in enumerate(LEVELS[1])]
        brace = Brace(VGroup(*[inv.slots[k] for k in range(2)]), DOWN, color=MC_YELLOW, buff=0.3)
        size = chat("size = 2", MC_YELLOW, 52).next_to(brace, DOWN, buff=0.2)

        self.seg(6)
        self.beat(FadeOut(items[1]), FadeOut(out), FadeOut(inn), rt=0.3)
        self.beat(*[FadeIn(s, scale=1.4) for s in snap], rt=0.4)
        self.until(at(6, "length") - 0.2)
        self.sfx("click", 0.3)
        self.beat(GrowFromCenter(brace), FadeIn(size, shift=UP * 0.15), rt=0.5)
        self.until(at(6, "Exactly") - 0.1)
        self.sfx("orb", 0.3)
        self.beat(pulse(tree.level(1), 1.15), rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        FLY = 0.35  # same as three/mundo.html: seconds an item flies between the tree and its slot
        h = hdr("BFS", MC_GREEN)
        inv = Inventory(9, "Queue")
        inv.move_to([0, -1.15, 0])
        code = code_panel(CODE, -4.35, max_h=3.0)
        bar = line_bar(code, 1, 1, MC_YELLOW)
        st = {"badge": None, "res": None, "q": [], "done": [], "cur": []}

        def badge(n):
            return chat(f"size {n}", MC_YELLOW, 42).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)

        def res_line():
            # Compact lists in at most two chat boxes, so all four levels fit across the frame
            compact = lambda v: "[" + ",".join(str(x) for x in v) + "]"
            parts = [chat("res = " + " ".join(compact(v) for v in st["done"]), MC_WHITE, 38)]
            if st["cur"]:
                parts.append(chat(compact(st["cur"]), MC_GOLD, 38))
            return VGroup(*parts).arrange(RIGHT, buff=0.12).move_to([0, -2.2, 0])

        def set_res(rt=0.15):
            new = res_line()
            if st["res"] is None:
                st["res"] = new
                self.beat(FadeIn(new), rt=rt)
            else:
                self.beat(Transform(st["res"], new), rt=rt)

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("tree_in", "init", "empty", "all", "toast", "rows")]
        for k, e in enumerate(EVENTS):
            # Pushes show in the slot when the flying item lands
            ev.append((seg_time(W["first"], e["t"]) + (FLY * 0.7 if e["kind"] == "push" else 0), e["kind"], k))
        ev.sort(key=lambda x: x[0])

        def move_bar(k0, color=MC_YELLOW, rt=0.12):
            self.beat(Transform(bar, line_bar(code, k0, k0, color)), rt=rt)

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.35)

        def on(kind, k):
            e = EVENTS[k] if k is not None else None
            if kind == "tree_in":
                for i in range(len(NODES)):
                    self.sfx(f"stone_dig{i % 4 + 1}", 0.25, delay=0.1 * i + 0.4)
                self.beat(FadeIn(code, shift=UP * 0.3), FadeIn(inv, shift=UP * 0.3), rt=0.5)
            elif kind == "init":
                it = queue_item(inv, 0, 0)
                st["q"].append(it)
                self.sfx("pop", 0.35, delay=0.35)
                self.beat(FadeIn(bar), rt=0.15)
                self.hold(0.3)
                self.beat(FadeIn(it, scale=1.5), rt=0.15)
                set_res()
            elif kind == "size":
                self.sfx("click", 0.3)
                move_bar(4)
                if st["badge"] is None:
                    st["badge"] = badge(e["n"])
                    self.beat(FadeIn(st["badge"], shift=LEFT * 0.2), rt=0.2)
                else:
                    self.beat(Transform(st["badge"], badge(e["n"])), rt=0.2)
            elif kind == "pop":
                self.sfx("stone_dig%d" % (k % 4 + 1), 0.32, delay=FLY)
                gone = st["q"].pop(0)
                st["cur"].append(NODES[e["node"]]["val"])
                # One beat: the bar, the item leaving slot 0, the rest sliding forward and the value recorded
                self.beat(Transform(bar, line_bar(code, 5, 6, MC_GOLD)), FadeOut(gone, shift=UP * 0.4),
                          *[it.animate.move_to(inv.slots[j]) for j, it in enumerate(st["q"])], Transform(st["res"], res_line()), rt=0.2)
            elif kind == "push":
                it = queue_item(inv, len(st["q"]), e["node"])
                st["q"].append(it)
                self.sfx("pop", 0.32)
                self.beat(Transform(bar, line_bar(code, 8, 8, MC_GREEN)), FadeIn(it, scale=1.5), rt=0.12)
            elif kind == "done":
                st["done"].append(st["cur"])
                st["cur"] = []
                self.sfx("book_put", 0.3)
                self.beat(Transform(bar, line_bar(code, 9, 9, MC_GREEN)), Transform(st["res"], res_line()), rt=0.15)
            elif kind == "empty":
                self.sfx("chestclosed", 0.3)
                move_bar(2, MC_GRAY, rt=0.2)
                self.beat(FadeOut(st["badge"]), rt=0.2)
            elif kind == "all":
                move_bar(10, MC_GREEN, rt=0.2)
                self.beat(pulse(st["res"], 1.08), rt=0.4)
            elif kind == "toast":
                t = toast("Advancement Made!", "Tree read in rows", w=4.6)
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                self.beat(t.animate.shift(LEFT * 7), rt=0.5)
            elif kind == "rows":
                self.beat(pulse(st["res"], 1.08), rt=0.4)

        def on_last():
            # The tree leaves the 3D clip when the walk ends; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        tree = Tree2D(0.7, 4.1, 0.8, 0.62)
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, 0.55, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, -0.35, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(14)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(tree), rt=0.5)
        self.until(at(14, "in and out") - 0.3)
        # Every block passes through the queue once, in level order
        self.sfx("click", 0.25)
        self.beat(LaggedStart(*[pulse(tree.blocks[i], 1.2) for ids in LEVELS for i in ids], lag_ratio=0.15), rt=1.3)
        self.until(at(14, "linear") - 0.6)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.35)
        self.add(xp)
        for d in (0.0, 0.25):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=0.5)
        self.beat(Restore(xp), rt=0.6)
        self.close_seg()

        widest = tree.level(2)
        frame = SurroundingRectangle(widest, color=MC_YELLOW, stroke_width=6, buff=0.12)
        sp = VGroup(MT("space", 56, MC_GRAY), level_text("O(w)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, -2.0, 0])
        ww = MT("w = widest level = 4", 38, MC_WHITE).move_to([0, -3.15, 0])

        self.seg(15)
        self.until(at(15, "one full level") - 0.2)
        self.sfx("pop", 0.3)
        self.beat(Create(frame), pulse(widest, 1.1), rt=0.5)
        self.until(at(15, "width") - 0.5)
        self.beat(FadeIn(sp, shift=UP * 0.2), FadeIn(ww), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.6, width=8.4)
        bar = line_bar(code, 1, 1, MC_YELLOW)

        self.seg(16)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(at(16, "snapshot") - 0.1)
        self.beat(Transform(bar, line_bar(code, 4, 4, MC_GOLD)), rt=0.35)
        self.close_seg()

        self.seg(17)
        msg = chat("Sweep level by level", MC_GOLD, 58)
        msg.move_to([0, -2.3, 0])
        self.beat(FadeIn(msg, shift=UP * 0.2), Transform(bar, line_bar(code, 0, 10, MC_GREEN)), rt=0.4)
        self.until(1.4)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.45)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.9)
        self.close_seg()
