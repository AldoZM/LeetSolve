WALK = json.load(open('walk.json', encoding='utf-8'))
TOKS = WALK["tokens"]
TEXT = WALK["text"]
ORE_OF.update({t["value"]: t["ore"] for t in TOKS if t["tok"] != "#"})
VALUES = [t["tok"] for t in TOKS if t["tok"] != "#"]
WOOD = "#9C7A48"
NULL_EDGE = "#5A2A2A"

SER_CODE = """def serialize(root):
    out = []
    def write(node):
        if node is None:
            return out.append("#")
        out.append(str(node.val))
        write(node.left)
        write(node.right)
    write(root)
    return ",".join(out)"""

DES_CODE = """def deserialize(data):
    tokens = iter(data.split(","))
    def build():
        tok = next(tokens)
        if tok == "#":
            return None
        node = TreeNode(int(tok))
        node.left, node.right = build(), build()
        return node
    return build()"""

# The other two trees with the same values in preorder (5, 8, 2, 7): a chain to the right, and 8 holding 2 and 7
TREE_B = {"a": (5, None, "b"), "b": (8, None, "c"), "c": (2, None, "d"), "d": (7, None, None)}
TREE_C = {"a": (5, "b", None), "b": (8, "c", "d"), "c": (2, None, None), "d": (7, None, None)}


def make_tokens(tree, spread):
    # Preorder with "#" for empty children, each token with its spot (same layout as make_walk.py)
    out = []

    def walk(name, x, lvl, parent):
        tok = {"x": x, "lvl": lvl, "parent": parent}
        out.append(tok)
        if name is None:
            tok["tok"] = "#"
            return
        value, left, right = tree[name]
        tok.update({"tok": str(value), "value": value, "ore": ORE_OF[value]})
        me = len(out) - 1
        walk(left, x - spread[lvl], lvl + 1, me)
        walk(right, x + spread[lvl], lvl + 1, me)

    walk("a", 0.0, 0, None)
    return out


TOKS_B = make_tokens(TREE_B, [0.6, 0.6, 0.6, 0.6])
TOKS_C = make_tokens(TREE_C, [1.0, 0.7, 0.5])


def at(i, phrase, nth=0):
    # Seconds into line i where the nth `phrase` starts (even speaking rate inside a line)
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
    return min(dur - 0.1, dur * k / len(text))


class Tree2D(VGroup):
    """A tree of ore blocks joined by wooden rods; with nulls=True, barrier icons mark the empty children."""

    def __init__(self, toks, size, top, dy, sx, x0=0.0, nulls=False, **kwargs):
        super().__init__(**kwargs)
        self.pos = [np.array([x0 + t["x"] * sx, top - t["lvl"] * dy, 0]) for t in toks]
        self.blocks, self.edges, self.bars = {}, {}, {}
        for i, t in enumerate(toks):
            null = t["tok"] == "#"
            if t["parent"] is None or (null and not nulls):
                continue
            self.edges[i] = Line(self.pos[t["parent"]], self.pos[i], color=NULL_EDGE if null else WOOD,
                                 stroke_width=(7 if null else 11) * size, stroke_opacity=0.8 if null else 1)
        for i, t in enumerate(toks):
            if t["tok"] != "#":
                self.blocks[i] = Block(t["value"], f"{t['ore']}_ore", size).move_to(self.pos[i])
            elif nulls:
                self.bars[i] = pixel_art("barrier", size * 0.72).move_to(self.pos[i])
        self.add(VGroup(*self.edges.values()), VGroup(*self.blocks.values()), VGroup(*self.bars.values()))

    def block_list(self):
        return [self.blocks[i] for i in sorted(self.blocks)]


def glyphs(s, size, color):
    # Game-font text inside an invisible box of its full line height, so pieces placed side by side share a baseline
    img = text_image(s, color)
    u = _px_unit(size, TERM)
    span = Rectangle(width=img.width * u, height=img.height * u, stroke_width=0, fill_opacity=0)
    return VGroup(span, pixel_image(img, img.width * u, img.height * u))


def pulse(m, k=1.15):
    # Emphasis that keeps the pixel art's colors (Indicate would paint it one flat color)
    return m.animate(rate_func=there_and_back).scale(k)


class TokenLine(VGroup):
    """A serialized string in a chat box, one mobject per token (toks) plus the commas; '#' in red."""

    def __init__(self, tokens, size=44, color=MC_WHITE, opacity=0.55, **kwargs):
        super().__init__(**kwargs)
        parts, self.toks, self.commas = [], [], []
        for k, t in enumerate(tokens):
            if k:
                c = glyphs(",", size, MC_GRAY)
                parts.append(c)
                self.commas.append(c)
            m = glyphs(t, size, MC_RED if t == "#" else color)
            parts.append(m)
            self.toks.append(m)
        self.row = VGroup(*parts).arrange(RIGHT, buff=0)
        self.box = Rectangle(width=self.row.width + 0.56, height=self.row.height + 0.28, fill_color="#000000",
                             fill_opacity=opacity, stroke_width=0)
        self.row.move_to(self.box)
        self.add(self.box, self.row)

    def upto(self, k):
        # Token k plus the comma before it
        return VGroup(self.toks[k], *([self.commas[k - 1]] if k else []))


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def slot_item(inv, k):
    # What token k looks like in an inventory slot: the ore block with its value, or the barrier item
    t = TOKS[k]
    if t["tok"] == "#":
        icon = pixel_art("barrier", 15 * inv.u)
        icon.move_to(inv.slots[k])
        return icon
    icon = iso_block(f"{t['ore']}_ore", 16 * inv.u)
    # Value in the corner where the game prints stack counts: on top of the block it hid the top face and looked flat
    val = gui_text(t["tok"], MC_WHITE, inv.u * 1.15)
    val.move_to(icon.get_corner(DR) + np.array([1 * inv.u, 0.5 * inv.u, 0]), aligned_edge=DR)
    item = VGroup(icon, val)
    item.move_to(inv.slots[k])
    return item


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("SERIALIZE", width=6.6).move_to([0, 4.85, 0])
    t2 = stone_title("& DESERIALIZE", width=8.2).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    tree = Tree2D(TOKS, 0.8, 1.75, 0.95, 0.8)
    book = pixel_art("writable_book", 0.95).move_to([-3.1, 1.0, 0])
    line = TokenLine(TEXT.split(","), 44, MC_WHITE)
    line.move_to([0, -1.45, 0])
    tags = VGroup(chat("LeetCode #297", MC_AQUA, 46), chat("Hard", MC_RED, 46), chat("Tree DFS", MC_GOLD, 46))
    tags.arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, tree, book, line, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, tree, book, line, tags = art
        self.add(art)

        self.seg(0)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        # Blocks hop from the root down, like a preorder wave
        blocks = tree.block_list()
        self.sfx("stone_dig1", 0.3, delay=0.3)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.3) for b in blocks], lag_ratio=0.22), rt=1.4)
        self.sfx("book_flip1", 0.4)
        self.beat(Rotate(book, angle=-12 * DEGREES, rate_func=there_and_back),
                  LaggedStart(*[Indicate(m, color=MC_YELLOW, scale_factor=1.3) for m in line.toks], lag_ratio=0.12), rt=1.6)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        top = Tree2D(TOKS, 0.75, 4.1, 0.85, 0.75)
        a1 = Arrow([0, 1.85, 0], [0, 1.05, 0], color=MC_YELLOW, stroke_width=8, buff=0)
        l1 = MT("serialize", 36, MC_YELLOW).next_to(a1, RIGHT, buff=0.25)
        book = pixel_art("writable_book", 0.7)
        text = chat('"  ? ? ?  "', MC_WHITE, 48)
        mid = VGroup(book, text).arrange(RIGHT, buff=0.3).move_to([0, 0.45, 0])
        a2 = Arrow([0, -0.15, 0], [0, -0.95, 0], color=MC_AQUA, stroke_width=8, buff=0)
        l2 = MT("deserialize", 36, MC_AQUA).next_to(a2, RIGHT, buff=0.25)
        bottom = Tree2D(TOKS, 0.75, -1.6, 0.85, 0.75)
        same = MT("same values, same shape", 40, MC_GREEN).move_to([0, -4.45, 0])

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        # The tree is built block by block, rods first
        blocks = top.block_list()
        for b in blocks:
            b.shift(UP * 7)
        self.add(*blocks)
        for k in range(len(blocks)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.32, delay=k * 0.15 + 0.4)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 7) for b in blocks],
                              lag_ratio=0.15), rt=1.5)
        # Rods go behind the blocks: added first, then the blocks re-added on top (Create keeps that order)
        self.add(top[0], *blocks)
        self.beat(Create(top[0]), rt=0.4)
        self.until(at(1, "save") - 0.1)
        self.sfx("book_flip1", 0.4)
        self.beat(GrowArrow(a1), FadeIn(l1), rt=0.4)
        self.beat(FadeIn(mid, shift=DOWN * 0.2), rt=0.4)
        self.close_seg()

        self.seg(2)
        self.until(0.2)
        self.beat(GrowArrow(a2), FadeIn(l2), rt=0.4)
        self.sfx("stone_dig2", 0.3, delay=0.3)
        self.beat(FadeIn(bottom, shift=DOWN * 0.3), rt=0.6)
        self.until(at(2, "exact"))
        self.sfx("orb", 0.35)
        self.beat(FadeIn(same, shift=UP * 0.2), *[pulse(b) for b in bottom.block_list()],
                  rt=0.6)
        self.clear_all(rt=0.45)
        self.close_seg()


class Scene3_Trap(Base):
    def construct(self):
        h = hdr("FIRST TRY", MC_RED)
        big = Tree2D(TOKS, 0.9, 3.9, 1.05, 0.85)
        rule = MT("node, then left, then right", 40, MC_GRAY).move_to([0, 0.85, 0])
        line = TokenLine(VALUES, 54, MC_WHITE)
        line.move_to([0, -0.6, 0])
        order = big.block_list()
        cur = outline(order[0], MC_YELLOW, 9)

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(big), rt=0.6)
        self.until(at(3, "preorder"))
        self.beat(FadeIn(rule, shift=UP * 0.15), FadeIn(line.box), rt=0.4)
        # Preorder: the node, its left side, its right side; each visit writes its value
        visits = [at(3, "The node"), at(3, "left side"), at(3, "right side"), at(3, "right side") + 0.35]
        for k, b in enumerate(order):
            self.until(visits[k])
            self.sfx("click", 0.3)
            anims = [Create(cur)] if k == 0 else [cur.animate.move_to(b)]
            self.beat(*anims, FadeIn(line.upto(k), shift=DOWN * 0.15), rt=0.25)
        self.close_seg()

        self.seg(4)
        self.beat(FadeOut(cur), FadeOut(rule), rt=0.3)
        words = [at(4, "five"), at(4, "eight"), at(4, "two"), at(4, "seven")]
        for k, m in enumerate(line.toks):
            self.until(words[k])
            self.beat(Indicate(m, color=MC_YELLOW, scale_factor=1.35), rt=0.35)
        self.close_seg()

        # Three columns: our tree, a chain to the right, and 8 holding 2 and 7. All read 5,8,2,7
        cols = [-2.95, 0.0, 2.95]
        trees = [Tree2D(TOKS, 0.5, 3.7, 0.62, 0.5, cols[0]), Tree2D(TOKS_B, 0.5, 3.7, 0.58, 0.75, cols[1] - 0.65),
                 Tree2D(TOKS_C, 0.5, 3.7, 0.62, 0.62, cols[2] + 0.35)]
        lines = [TokenLine(VALUES, 38, MC_WHITE) for _ in cols]
        for ln, x in zip(lines, cols):
            ln.move_to([x, 0.75, 0])

        self.seg(5)
        self.beat(Transform(big, trees[0]), Transform(line, lines[0]), rt=0.6)
        self.sfx("stone_dig3", 0.3, delay=0.3)
        self.beat(FadeIn(trees[1], shift=DOWN * 0.3), rt=0.5)
        self.beat(FadeIn(lines[1], shift=DOWN * 0.15), rt=0.35)
        self.until(at(5, "And so"))
        self.sfx("stone_dig4", 0.3, delay=0.3)
        self.beat(FadeIn(trees[2], shift=DOWN * 0.3), rt=0.5)
        self.beat(FadeIn(lines[2], shift=DOWN * 0.15), rt=0.35)
        self.close_seg()

        eqs = VGroup(*[MT("=", 54, MC_YELLOW).move_to([x, 0.75, 0]) for x in (-1.475, 1.475)])
        lost = MT("shape lost!", 64, MC_RED).move_to([0, -1.4, 0])
        which = MT("which tree do we load?", 38, MC_GRAY).move_to([0, -2.6, 0])

        self.seg(6)
        self.beat(*[pulse(ln, 1.1) for ln in [line] + lines[1:]], FadeIn(eqs), rt=0.6)
        self.until(at(6, "different"))
        self.beat(*[pulse(t, 1.08) for t in [big] + trees[1:]], rt=0.6)
        self.until(at(6, "The shape"))
        self.sfx("villager_no1", 0.4)
        self.beat(FadeIn(lost, scale=1.4), FadeIn(which, shift=UP * 0.1), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        tree = Tree2D(TOKS, 0.85, 4.0, 1.0, 0.95, nulls=True)
        legend = VGroup(pixel_art("barrier", 0.62), MT("= #", 52, MC_WHITE, PIXEL)).arrange(RIGHT, buff=0.25)
        legend.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.45)
        line = TokenLine(TEXT.split(","), 50, MC_WHITE)
        line.move_to([0, -0.75, 0])
        ok = VGroup(MT("1 text", 52, MC_WHITE), MT("=", 52, MC_GRAY), MT("1 tree", 52, MC_GREEN)).arrange(RIGHT, buff=0.3)
        ok.move_to([0, -2.3, 0])
        bars = [tree.bars[i] for i in sorted(tree.bars)]
        null_edges = [tree.edges[i] for i in sorted(tree.bars)]
        wood = VGroup(*[tree.edges[i] for i in sorted(tree.edges) if i not in tree.bars])

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(wood), FadeIn(VGroup(*tree.block_list())), rt=0.6)
        self.until(at(7, "missing") - 0.2)
        # Every empty child gets its marker, in preorder
        for k, (b, e) in enumerate(zip(bars, null_edges)):
            self.sfx("pop", 0.3)
            self.add(e, *tree.block_list())
            self.beat(Create(e), FadeIn(b, scale=1.6), rt=0.3)
        self.until(at(7, "barrier block") - 0.3)
        self.sfx("wood_dig1", 0.35)
        self.beat(FadeIn(legend, scale=0.6), *[pulse(b, 1.3) for b in bars], rt=0.6)
        self.close_seg()

        self.seg(8)
        self.beat(FadeIn(line.box), rt=0.3)
        self.beat(LaggedStart(*[FadeIn(line.upto(k), shift=DOWN * 0.1) for k in range(len(line.toks))], lag_ratio=0.25),
                  rt=1.4)
        self.until(at(8, "one text"))
        self.sfx("orb", 0.35)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in ok], lag_ratio=0.25), rt=0.7)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        FLY = 0.35  # same as three/mundo.html: seconds an item flies between the tree and its slot
        h = hdr("SAVE", MC_GREEN)
        h2 = hdr("LOAD", MC_AQUA)
        inv = Inventory(9, "Saved tree")
        inv.move_to([0, -1.15, 0])
        code = code_panel(SER_CODE, -4.3, max_h=3.3)
        des = code_panel(DES_CODE, -4.3, max_h=3.3)
        st = {"bar": line_bar(code, 2, 2, MC_YELLOW), "code": code, "cur": None}
        items = [slot_item(inv, k) for k in range(len(TOKS))]

        def T(spec):
            return seg_time(W["first"], spec)

        ev = [(T(W[key]), key, None) for key in ("inv_in", "cursor", "slot_demo", "saved", "clear", "load", "read_demo",
                                                 "toast", "back")]
        for k, t in enumerate(TOKS):
            ev += [(T(t["save"]), "write", k), (T(t["save"]) + FLY, "land", k), (T(t["say"]), "say", k),
                   (T(t["load"]), "take", k), (T(t["load"]) + FLY, "place", k)]
        ev.sort(key=lambda e: e[0])

        def move_bar(line, color=MC_YELLOW, rt=0.12):
            self.beat(Transform(st["bar"], line_bar(st["code"], line, line, color)), rt=rt)

        def mark(k, color, rt=0.12):
            # Outline on slot k (moves if it is already showing)
            box = outline(inv.slots[k], color, 7, buff=0.03)
            if st["cur"] is None:
                st["cur"] = box
                self.beat(Create(box), rt=rt)
            else:
                self.beat(Transform(st["cur"], box), rt=rt)

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(code, shift=UP * 0.3), rt=0.5)
            # The 3D blocks drop in one after another and land about 0.5 s later
            for i in range(4):
                self.sfx(f"stone_dig{i + 1}", 0.3, delay=0.15 + 0.12 * i + 0.4 - 0.5)

        def on(kind, k):
            if kind == "inv_in":
                self.sfx("wood_dig2", 0.4)
                self.beat(FadeIn(inv, shift=UP * 0.3), rt=0.4)
            elif kind == "cursor":
                self.beat(FadeIn(st["bar"]), rt=0.25)
            elif kind == "slot_demo":
                mark(0, MC_WHITE, rt=0.3)
            elif kind == "write":
                move_bar(4 if TOKS[k]["tok"] == "#" else 5)
            elif kind == "land":
                self.sfx("click" if TOKS[k]["tok"] == "#" else "pop", 0.35)
                mark(k, MC_WHITE, rt=0.1)
                self.beat(FadeIn(items[k], scale=1.6), rt=0.15)
            elif kind == "saved":
                self.sfx("book_put", 0.4)
                move_bar(9, MC_GREEN, rt=0.2)
                self.beat(Transform(inv.title, inv.title_for(TEXT)), FadeOut(st["cur"]), rt=0.35)
                st["cur"] = None
            elif kind == "say":
                self.sfx("click", 0.18)
                mark(k, MC_YELLOW, rt=0.1)
                self.beat(pulse(items[k], 1.25), rt=0.17)
            elif kind == "clear":
                self.beat(FadeOut(st["cur"]), rt=0.15)
                st["cur"] = None
                for i, t in enumerate(TOKS):
                    if t["tok"] != "#":
                        self.sfx(f"stone_dig{i % 4 + 1}", 0.35, delay=0.06 * i + 0.15)
            elif kind == "load":
                self.sfx("book_flip2", 0.4)
                self.beat(Transform(h, h2), FadeOut(st["bar"]), FadeOut(code), FadeIn(des), rt=0.4)
                st["code"] = des
                st["bar"] = line_bar(des, 2, 2, MC_YELLOW)
                self.beat(FadeIn(st["bar"]), rt=0.15)
            elif kind == "read_demo":
                mark(0, MC_AQUA, rt=0.3)
            elif kind == "take":
                mark(k, MC_AQUA, rt=0.08)
                move_bar(3, MC_AQUA, rt=0.08)
                self.beat(FadeOut(items[k], shift=UP * 0.35, scale=0.6), rt=0.12)
            elif kind == "place":
                null = TOKS[k]["tok"] == "#"
                self.sfx("click" if null else f"stone_dig{k % 4 + 1}", 0.3 if null else 0.38)
                if k == len(TOKS) - 1:
                    move_bar(9, MC_GREEN, rt=0.15)
                else:
                    move_bar(5 if null else 6, MC_RED if null else MC_GREEN, rt=0.1)
            elif kind == "toast":
                # Small and high: the root block sits just below this corner
                t = toast("Advancement Made!", "Tree loaded", w=4.6)
                t.move_to([0, 5.5, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(st["cur"]), rt=0.5)
                st["cur"] = None
            elif kind == "back":
                self.beat(Transform(inv.title, inv.title_for("Empty")), rt=0.3)

        def on_last():
            # The tree leaves the 3D clip when the walk ends; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        save = VGroup(MT("save", 56, MC_WHITE), level_text("O(n)", 0.9)).arrange(RIGHT, buff=0.4)
        load = VGroup(MT("load", 56, MC_WHITE), level_text("O(n)", 0.9)).arrange(RIGHT, buff=0.4)
        VGroup(save, load).arrange(RIGHT, buff=1.0).move_to([0, 3.55, 0])
        sub = MT("each node: written once, read once", 36, MC_WHITE).move_to([0, 2.45, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 1.55, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(18)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(at(18, "written"))
        self.beat(FadeIn(save, shift=UP * 0.15), FadeIn(sub), rt=0.5)
        self.until(at(18, "read once"))
        self.beat(FadeIn(load, shift=UP * 0.15), FadeIn(bg), rt=0.5)
        self.until(at(18, "linear") - 0.9)
        self.add(xp)
        for d in (0.0, 0.3, 0.6):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=0.9)
        self.beat(Restore(xp), rt=1.0)
        self.close_seg()

        vals = VGroup(*[iso_block(f"{ORE_OF[int(v)]}_ore", 0.62) for v in VALUES]).arrange(RIGHT, buff=0.18)
        nv = MT("n = 4", 46, MC_WHITE, PIXEL)
        row1 = VGroup(vals, nv).arrange(RIGHT, buff=0.5).move_to([0, -0.2, 0])
        nulls = VGroup(*[pixel_art("barrier", 0.55) for _ in range(len(VALUES) + 1)]).arrange(RIGHT, buff=0.2)
        nn = MT("n + 1 = 5", 46, MC_RED, PIXEL)
        row2 = VGroup(nulls, nn).arrange(RIGHT, buff=0.5).move_to([0, -1.5, 0])
        space = VGroup(MT("space", 56, MC_GRAY), level_text("O(n)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, -3.2, 0])

        self.seg(19)
        self.until(at(19, "n values") - 0.2)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(*[FadeIn(b, scale=0.6) for b in vals], lag_ratio=0.2), FadeIn(nv), rt=0.6)
        self.until(at(19, "n plus") - 0.1)
        self.sfx("click", 0.3)
        self.beat(LaggedStart(*[FadeIn(b, scale=0.6) for b in nulls], lag_ratio=0.2), FadeIn(nn), rt=0.6)
        self.until(at(19, "Linear"))
        self.sfx("orb", 0.3)
        self.beat(FadeIn(space, shift=UP * 0.2), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(SER_CODE + "\n\n" + DES_CODE, 1.0, width=8.4, max_h=7.9)
        bar = line_bar(code, 0, 0, MC_YELLOW)

        self.seg(20)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.04), FadeIn(code.line_numbers),
                  rt=0.9)
        self.until(at(20, "walks") - 0.1)
        self.beat(FadeIn(bar), Transform(bar, line_bar(code, 5, 7, MC_GOLD)), rt=0.35)
        self.until(at(20, "reads") - 0.1)
        self.beat(Transform(bar, line_bar(code, 14, 18, MC_AQUA)), rt=0.35)
        self.until(at(20, "same order"))
        self.beat(Transform(bar, line_bar(code, 0, 20, MC_GREEN)), rt=0.4)
        self.close_seg()

        self.seg(21)
        msg = chat("Mark the empty spots", MC_GOLD, 58)
        msg.move_to([0, -4.3, 0])
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.4)
        self.until(1.9)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.45)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.9)
        self.close_seg()
