WALK = json.load(open('walk.json', encoding='utf-8'))
NAMES = {1: "one", 3: "three", 6: "six", 8: "eight", 10: "ten", 13: "thirteen", 14: "fourteen"}
CODE_X = -3.9  # code panels sit on the left half, drawings on the right
BFS = [v for lv in LEVELS for v in lv]  # 8, 3, 10, 1, 6, 14, 13

NODE_CODE = """class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None"""

BUILD_CODE = """root = Node(8)
root.left = Node(3)
root.right = Node(10)
root.left.left = Node(1)"""


def hotbar_tools():
    # The objects of this guide, in the game's hotbar
    bar = Hotbar(9, 7.4)
    icons = [pixel_art(n, 0.58) for n in ("oak_sapling", "shears", "lead", "chest_front", "hopper", "barrier", "writable_book")]
    for ic, s in zip(icons, bar.slots):
        ic.move_to(s)
    return VGroup(bar, *icons)


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("HOW TREES", width=7.2).move_to([-3.7, 2.9, 0])
    t2 = stone_title("REALLY WORK", width=7.8).move_to([-3.7, 1.55, 0])
    spl = splash("Minecraft edition!", 27).move_to([-0.7, 0.45, 0])
    tree = Tree2D(0.92, 3.3, 1.6, 0.95, x0=4.1, nulls=True)
    tags = VGroup(chat("Binary trees", MC_AQUA, 50), chat("DFS + BFS", MC_GOLD, 50), chat("Recursion", MC_GREEN, 50))
    tags.arrange(RIGHT, buff=0.25)
    tags.scale_to_fit_width(min(tags.width, 7.4)).move_to([-3.7, -0.7, 0])
    tools = hotbar_tools().move_to([-3.7, -2.25, 0])
    return VGroup(t1, t2, spl, tree, tags, tools)


def entry(key, desc, color, icon=None):
    # One line of the glossary: the word in color and what it means, in a chat box
    parts = [MT(key, 48, color)] + ([icon] if icon else []) + [MT(desc, 42, MC_WHITE)]
    row = VGroup(*parts).arrange(RIGHT, buff=0.28)
    box = Rectangle(width=row.width + 0.5, height=0.74, fill_color="#000000", fill_opacity=0.6, stroke_width=0)
    g = VGroup(box, row.move_to(box))
    if g.width > GLOSS_W:
        g.scale_to_fit_width(GLOSS_W)
    return g


GLOSS_W = 5.5


def boxed(row):
    # Same chat box as entry() around any row, so text stays readable over leaves and mobs
    box = Rectangle(width=row.width + 0.5, height=max(0.74, row.height + 0.24), fill_color="#000000", fill_opacity=0.6,
                    stroke_width=0)
    return VGroup(box, row.move_to(box))


def fit(m, w=GLOSS_W):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def glossary_at(k):
    # Right column of the sharp scenes (x from 2.3 to 7.8): entries stack down from y = 3.1
    return np.array([2.3, 3.1 - 0.86 * k, 0])


def place(m, k):
    m.move_to(glossary_at(k), aligned_edge=LEFT)
    return m


class Scene01_Hook(Base):
    def construct(self):
        art = cover()
        t1, t2, spl, tree, tags, tools = art
        self.add(art)
        code = code_panel(TREE_SUM, 0, width=7.4)
        code.move_to([-3.7, -2.1, 0])

        self.seg(0)
        self.beat(pulse(spl), rt=0.8)
        blocks = tree.block_list()
        self.sfx("stone_dig1", 0.3, delay=0.3)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.3) for b in blocks], lag_ratio=0.2), rt=1.6)
        self.until(at(0, "every tree") - 0.2)
        self.beat(*[pulse(b, 1.3) for b in tree.bars.values()], rt=0.6)
        self.until(at(0, "same five") - 0.3)
        self.sfx("book_flip1", 0.4)
        self.beat(FadeOut(tags), FadeOut(tools), FadeIn(code, shift=UP * 0.2), rt=0.45)
        self.clear_all(rt=0.45)
        self.close_seg()


class Scene02_Why(Base):
    def construct(self):
        h = hdr("WHY TREES?", MC_AQUA)
        blocks = [Block(v, f"{ORE_OF[v]}_ore", 1.35) for v in IN]
        row = VGroup(*blocks).arrange(RIGHT, buff=0.45)
        row.move_to([0, 1.3, 0])
        mid = blocks[3]
        cur = outline(mid, MC_YELLOW, 8)
        back = Arrow(mid.get_bottom() + DOWN * 0.4 + LEFT * 0.1, blocks[2].get_bottom() + DOWN * 0.4, color=MC_AQUA,
                     stroke_width=9, buff=0)
        fwd = Arrow(mid.get_bottom() + DOWN * 0.4 + RIGHT * 0.1, blocks[4].get_bottom() + DOWN * 0.4, color=MC_GOLD,
                    stroke_width=9, buff=0)
        lb = MT("before", 48, MC_AQUA).next_to(back, DOWN, buff=0.18)
        la = MT("after", 48, MC_GOLD).next_to(fwd, DOWN, buff=0.18)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        for k in range(len(blocks)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.28, delay=0.1 + k * 0.13)
        self.beat(LaggedStart(*[FadeIn(b, shift=DOWN * 0.5) for b in blocks], lag_ratio=0.15), rt=1.2)
        self.until(at(1, "Each block") - 0.1)
        self.beat(Create(cur), rt=0.3)
        self.until(at(1, "before") - 0.1)
        self.beat(GrowArrow(back), FadeIn(lb), rt=0.4)
        self.until(at(1, "after") - 0.1)
        self.beat(GrowArrow(fwd), FadeIn(la), rt=0.4)
        self.close_seg()

        # Real data branches: a folder holds folders, a choice opens choices
        q1 = chat("a folder holds more folders", MC_AQUA, 58).move_to([0, -2.0, 0])
        q2 = chat("one choice opens more choices", MC_GOLD, 58).move_to([0, -3.15, 0])

        self.seg(2)
        self.sfx("villager_no1", 0.35, delay=0.3)
        self.beat(FadeOut(VGroup(cur, back, fwd, lb, la)),
                  *[b.animate.shift(DOWN * (0.3 + 0.25 * (k % 3))).rotate((-1) ** k * 0.25) for k, b in enumerate(blocks)],
                  rt=0.7)
        self.until(at(2, "A folder") - 0.2)
        self.beat(FadeIn(q1, shift=UP * 0.2), rt=0.4)
        self.until(at(2, "One choice") - 0.2)
        self.beat(FadeIn(q2, shift=UP * 0.2), rt=0.4)
        self.finish(FadeOut(VGroup(*blocks, q1, q2)), rt=0.4)
        self.close_seg()

        # A project folder: every folder is a chest, joined by wooden rods
        spots = {"project/": [0, 2.75], "code/": [-3.6, 0.45], "assets/": [3.6, 0.45], "textures/": [1.6, -2.0],
                 "sounds/": [5.6, -2.0]}
        chests, names = {}, {}
        for name, (x, y) in spots.items():
            chests[name] = chest_icon(1.3).move_to([x, y, 0])
            names[name] = MT(name, 46, MC_WHITE).next_to(chests[name], DOWN, buff=0.14)

        def rod(a, b):
            return Line(chests[a].get_bottom() + DOWN * 0.6, chests[b].get_top(), color=WOOD, stroke_width=12)

        rods = {"code/": rod("project/", "code/"), "assets/": rod("project/", "assets/"),
                "textures/": rod("assets/", "textures/"), "sounds/": rod("assets/", "sounds/")}

        def show(name, rt=0.4):
            self.sfx("chestopen", 0.25)
            anims = [FadeIn(chests[name], shift=DOWN * 0.2), FadeIn(names[name])]
            if name in rods:
                self.add(rods[name], chests[name])
                anims.append(Create(rods[name]))
            self.beat(*anims, rt=rt)

        self.seg(3)
        self.until(at(3, "project") - 0.2)
        show("project/")
        self.until(at(3, "code") - 0.1)
        show("code/", 0.3)
        self.until(at(3, "assets.") - 0.1)
        show("assets/", 0.3)
        self.until(at(3, "textures") - 0.1)
        show("textures/", 0.3)
        self.until(at(3, "sounds") - 0.1)
        show("sounds/", 0.3)
        self.close_seg()

        tree_tag = chat("TREE", MC_GREEN, 72).move_to([-5.6, 2.75, 0])
        sap = pixel_art("oak_sapling", 2.2).move_to([-6.2, -1.6, 0])
        root_tag = chat("root on top", MC_GOLD, 50).next_to(chests["project/"], RIGHT, buff=0.5)
        leaf_tag = chat("leaves at the bottom", MC_GREEN, 50).move_to([-2.6, -3.4, 0])

        self.seg(4)
        self.beat(*[pulse(chests[n], 1.2) for n in ("assets/", "textures/", "sounds/")], rt=0.6)
        self.until(at(4, "That's a tree") - 0.1)
        self.sfx("orb", 0.35)
        self.beat(FadeIn(tree_tag, scale=1.3), rt=0.4)
        self.until(at(4, "upside down") - 0.4)
        self.beat(FadeIn(sap, shift=UP * 0.2), rt=0.3)
        self.beat(Rotate(sap, PI), rt=0.7)
        self.until(at(4, "root on top") - 0.1)
        self.beat(FadeIn(root_tag, shift=LEFT * 0.2), rt=0.35)
        self.until(at(4, "leaves") - 0.1)
        self.beat(FadeIn(leaf_tag, shift=UP * 0.2), *[pulse(chests[n], 1.15) for n in ("code/", "textures/", "sounds/")], rt=0.45)
        self.clear_all()
        self.close_seg()


class Scene03_Anatomy(Overlay):
    def construct(self):
        h = hdr("ANATOMY", MC_GOLD)
        rows = [
            entry("ROOT", "the only way in", MC_GOLD),
            entry("EDGE", "parent -> child", MC_WHITE),
            entry("BINARY", "2 children max", MC_AQUA),
            entry("RULE", "one parent, no loops", MC_RED),
            entry("LEAF", "no children", MC_GREEN),
            entry("None", "nothing there", MC_RED, pixel_art("barrier", 0.5)),
            entry("DEPTH", "rods from the root", MC_PINK),
            entry("HEIGHT", "longest way = 3", MC_YELLOW),
        ]
        for k, r in enumerate(rows):
            place(r, k)

        def add_row(k, rt=0.35):
            self.sfx("click", 0.25)
            self.beat(FadeIn(rows[k], shift=LEFT * 0.3), rt=rt)

        self.seg(5)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        # The 3D blocks drop one after another (three/mundo.html), each landing with a dig sound
        self.until(at(5, "Seven"))
        for k in range(7):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.3, delay=0.3 + 0.18 * k)
        self.until(at(5, "rods"))
        self.sfx("wood_dig1", 0.3, delay=0.2)
        self.close_seg()

        self.seg(6)
        self.until(at(6, "root"))
        self.sfx("orb", 0.35)
        add_row(0)
        self.until(at(6, "every block"))
        for k in range(7):
            self.sfx("orb", 0.18, delay=0.12 * k)
        self.close_seg()

        self.seg(7)
        self.until(at(7, "parent"))
        add_row(1)
        self.close_seg()

        self.seg(8)
        self.until(at(8, "binary"))
        add_row(2)
        self.close_seg()

        self.seg(9)
        self.until(at(9, "golden rule"))
        add_row(3)
        self.until(at(9, "loops"))
        self.sfx("villager_no1", 0.35)
        self.close_seg()

        self.seg(10)
        self.until(at(10, "exactly one"))
        for k in range(3):
            self.sfx("click", 0.25, delay=0.25 * k)
        self.close_seg()

        self.seg(11)
        self.until(at(11, "leaves"))
        add_row(4)
        for w in words_at(11, ["One", "six", "thirteen"]):
            self.sfx("pop", 0.3, delay=w - at(11, "leaves"))
        self.close_seg()

        self.seg(12)
        self.until(at(12, "In Python"))
        add_row(5)
        self.close_seg()

        self.seg(13)
        self.until(at(13, "barrier"))
        for k in range(8):
            self.sfx("click", 0.2, delay=0.12 * k)
        self.beat(pulse(rows[5], 1.08), rt=0.5)
        self.close_seg()

        self.seg(14)
        self.until(at(14, "depth"))
        add_row(6)
        self.close_seg()

        self.seg(15)
        self.until(at(15, "height"))
        add_row(7)
        self.sfx("levelup", 0.25, delay=at(15, "three") - self.scene_used + self.seg_begin)
        self.finish(FadeOut(Group(*self.mobjects)), rt=0.4)
        self.close_seg()


class Scene04_Subtree(Base):
    def construct(self):
        h = hdr("SUBTREES", MC_GREEN)
        tree = Tree2D(1.1, 3.2, 1.75, 1.25, x0=-2.6)
        blocks = tree.block_list()
        cut = tree.edges[3]
        mid = cut.get_center()
        shears = pixel_art("shears", 1.3).move_to(mid + np.array([1.8, 1.4, 0]))
        # Rods first: .animate redraws the group in this order, and rods listed last covered the numbers
        sub = VGroup(tree.edges[1], tree.edges[6], tree.blocks[3], tree.blocks[1], tree.blocks[6])
        drop = np.array([4.6, 1.0, 0]) - tree.blocks[3].get_center()

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.add(tree.rods, *blocks)
        self.beat(FadeIn(VGroup(*blocks)), Create(tree.rods), rt=0.8)
        self.until(at(16, "shears") - 0.3)
        self.sfx("wood_dig2", 0.3)
        self.beat(FadeIn(shears, scale=1.6), rt=0.4)
        self.until(at(16, "cut") - 0.2)
        self.beat(shears.animate.move_to(mid), rt=0.5)
        self.sfx("shear", 0.5)
        self.beat(Rotate(shears, -0.5, rate_func=there_and_back), cut.animate.set_stroke(MC_RED), rt=0.4)
        self.close_seg()

        frame3 = None
        self.seg(17)
        self.sfx("break", 0.35)
        self.beat(FadeOut(cut), FadeOut(shears), sub.animate.shift(drop), rt=0.8)
        box = SurroundingRectangle(sub, color=MC_GOLD, buff=0.3, stroke_width=6)
        frame3 = VGroup(box, chat("a whole tree", MC_GOLD, 50).next_to(box, UP, buff=0.2))
        self.until(at(17, "complete tree") - 0.2)
        self.sfx("orb", 0.35)
        self.beat(Create(box), FadeIn(frame3[1], shift=UP * 0.2), rt=0.5)
        self.until(at(17, "three is its root") - 0.1)
        crown = chat("root", MC_GOLD, 42).next_to(tree.blocks[3], LEFT, buff=0.2)
        self.beat(FadeIn(crown, shift=RIGHT * 0.15), pulse(tree.blocks[3], 1.25), rt=0.5)
        self.close_seg()

        # Cut again: 1 alone, with its two barriers
        one = Tree2D(1.1, 0, 1.4, 1.25, nulls=True, only=[1])
        one.shift(np.array([3.4, -2.3, 0]) - one.blocks[1].get_center())
        self.seg(18)
        self.beat(FadeOut(crown), rt=0.2)
        self.sfx("shear", 0.45)
        self.beat(FadeOut(tree.edges[1]), tree.blocks[1].animate.move_to(one.blocks[1]), rt=0.6)
        self.until(at(18, "barriers") - 0.2)
        self.sfx("click", 0.3)
        self.add(one.null_rods, one.blocks[1])
        self.beat(Create(one.null_rods), LaggedStart(*[FadeIn(b, scale=1.6) for b in one.bars.values()], lag_ratio=0.3), rt=0.6)
        tiny = chat("a tiny tree", MC_GREEN, 50).next_to(one, RIGHT, buff=0.4)
        self.until(at(18, "Just") - 0.2)
        self.beat(FadeIn(tiny, shift=UP * 0.2), rt=0.4)
        self.finish(FadeOut(Group(*self.mobjects[1:])), rt=0.45)
        self.close_seg()

        # A tree is a block, plus a left tree, plus a right tree
        big = Tree2D(1.1, 3.3, 1.65, 1.25, x0=0)
        left = SurroundingRectangle(VGroup(big.blocks[3], big.blocks[1], big.blocks[6]), color=MC_AQUA, buff=0.22,
                                    stroke_width=6)
        right = SurroundingRectangle(VGroup(big.blocks[10], big.blocks[14], big.blocks[13]), color=MC_GOLD, buff=0.22,
                                     stroke_width=6)
        me = outline(big.blocks[8], MC_GREEN, 7, buff=0.1)
        eq = VGroup(MT("tree", 60, MC_WHITE), MT("=", 60, MC_GRAY), MT("block", 60, MC_GREEN), MT("+", 60, MC_GRAY),
                    MT("left tree", 60, MC_AQUA), MT("+", 60, MC_GRAY), MT("right tree", 60, MC_GOLD))
        eq.arrange(RIGHT, buff=0.26).move_to([0, -3.75, 0])
        eq_box = Rectangle(width=eq.width + 0.6, height=eq.height + 0.4, fill_color="#000000", fill_opacity=0.6,
                           stroke_width=0).move_to(eq)

        self.seg(19)
        self.add(big.rods, *big.block_list())
        self.beat(FadeIn(big), FadeIn(h), rt=0.5)
        self.until(at(19, "root of its own") - 0.2)
        self.beat(Create(left), Create(right), rt=0.6)
        self.until(at(19, "A tree is") - 0.2)
        self.beat(FadeIn(eq_box), FadeIn(eq[0:2]), rt=0.3)
        self.until(at(19, "a block") - 0.1)
        self.beat(FadeIn(eq[2]), Create(me), rt=0.3)
        self.until(at(19, "plus a left") - 0.1)
        self.beat(FadeIn(eq[3:5]), pulse(left, 1.05), rt=0.35)
        self.until(at(19, "plus a right") - 0.2)
        self.beat(FadeIn(eq[5:7]), pulse(right, 1.05), rt=0.35)
        self.clear_all()
        self.close_seg()


class Scene05_DFS(Overlay):
    def construct(self):
        h = VGroup(hdr("DEPTH FIRST", MC_AQUA))
        lead = pixel_art("lead", 0.62).next_to(h, RIGHT, buff=0.25)
        rule = entry("LEFT FIRST", "as deep as you can", MC_AQUA)
        place(rule, 0)
        back = entry("DEAD END", "back up the lead", MC_RED)
        place(back, 1)
        moments = VGroup(chat("down", MC_AQUA, 46), chat("underneath", MC_GOLD, 46), chat("back up", MC_PINK, 46))
        moments.arrange(RIGHT, buff=0.18)
        fit(moments).move_to(glossary_at(0), aligned_edge=LEFT)
        lines = [TokenLine(o, 50, MC_WHITE, label=n, label_color=c)
                 for o, n, c in ((PRE, "PRE ", MC_AQUA), (IN, "IN  ", MC_GOLD), (POST, "POST", MC_PINK))]
        for k, ln in enumerate(lines):
            fit(ln).move_to(glossary_at(1.25 + 1.1 * k), aligned_edge=LEFT)
        note1 = fit(chat("PRE acts before the children", MC_AQUA, 44)).move_to(glossary_at(5.0), aligned_edge=LEFT)
        note3 = fit(chat("POST waits for their answers", MC_PINK, 44)).move_to(glossary_at(6.0), aligned_edge=LEFT)

        self.seg(20)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(at(20, "splits"))
        self.sfx("click", 0.3)
        self.close_seg()

        self.seg(21)
        self.until(at(21, "lead") - 0.2)
        self.sfx("lead_tie", 0.45)
        self.beat(FadeIn(lead, scale=1.5), rt=0.35)
        self.until(at(21, "always go left") - 0.1)
        self.beat(FadeIn(rule, shift=LEFT * 0.3), rt=0.35)
        self.close_seg()

        self.seg(22)
        for w in words_at(22, ["Eight", "three", "one"]):
            self.sfx("click", 0.28, delay=w)
        self.until(at(22, "only barriers"))
        self.beat(FadeIn(back, shift=LEFT * 0.3), rt=0.35)
        self.until(at(22, "six"))
        self.sfx("click", 0.28)
        self.close_seg()

        self.seg(23)
        for w in words_at(23, ["Ten", "fourteen", "thirteen"]):
            self.sfx("click", 0.28, delay=w)
        self.finish(FadeOut(rule), FadeOut(back), rt=0.35)
        self.close_seg()

        self.seg(24)
        self.until(at(24, "three times") - 0.1)
        self.sfx("orb", 0.3)
        for k, w in enumerate(words_at(24, ["down", "underneath", "back up"])):
            self.until(w - 0.1)
            self.beat(FadeIn(moments[k], shift=UP * 0.2), rt=0.3)
        self.close_seg()

        for i, (ln, order) in enumerate(zip(lines, (PRE, IN, POST))):
            self.seg(25 + i)
            start = ("preorder", "inorder", "postorder")[i]
            self.until(at(25 + i, start) - 0.3)
            self.beat(FadeIn(ln.box), FadeIn(ln.label), pulse(moments[i], 1.15), rt=0.35)
            names = [NAMES[v] if k else NAMES[v].capitalize() for k, v in enumerate(order)]
            for k, w in enumerate(words_at(25 + i, names, start)):
                self.until(w - 0.05)
                self.sfx("pop", 0.22)
                self.beat(FadeIn(ln.upto(k), shift=DOWN * 0.1), rt=0.12)
            self.close_seg()

        self.seg(28)
        self.until(at(28, "Preorder") - 0.1)
        self.beat(FadeIn(note1, shift=UP * 0.15), rt=0.35)
        self.until(at(28, "Postorder") - 0.1)
        self.beat(FadeIn(note3, shift=UP * 0.15), rt=0.35)
        self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)
        self.close_seg()


def queue_item(inv, k, v):
    # Ore block in slot k with its value in the corner, like a stack count
    icon = iso_block(f"{ORE_OF[v]}_ore", 16 * inv.u)
    val = gui_text(str(v), MC_WHITE, inv.u * 1.15)
    val.move_to(icon.get_corner(DR) + np.array([1 * inv.u, 0.5 * inv.u, 0]), aligned_edge=DR)
    return VGroup(icon, val).move_to(inv.slots[k])


class Scene06_BFS(Base):
    def construct(self):
        h = hdr("BREADTH FIRST", MC_GOLD)
        tree = Tree2D(1.0, 3.1, 1.75, 0.95, x0=-4.45)
        ys = [3.1 - 1.75 * k for k in range(4)]
        bands = [Rectangle(width=6.9, height=1.3, fill_color=MC_GOLD, fill_opacity=0.16, stroke_color=MC_GOLD,
                           stroke_width=2).move_to([-4.45, y, 0]) for y in ys]
        tags = [MT(f"level {k}", 40, MC_GOLD).next_to(bands[k], RIGHT, buff=0.12) for k in range(4)]

        self.seg(29)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.add(tree.rods, *tree.block_list())
        self.beat(FadeIn(tree), rt=0.6)
        self.until(at(29, "one level") - 0.2)
        self.beat(FadeIn(bands[0]), FadeIn(tags[0]), rt=0.3)
        self.close_seg()

        self.seg(30)
        for k, w in enumerate(words_at(30, ["Eight", "three", "one", "thirteen"])):
            self.until(w - 0.15)
            self.sfx("orb", 0.25)
            anims = [pulse(tree.blocks[v], 1.2) for v in LEVELS[k]]
            if k:
                anims += [FadeIn(bands[k]), FadeIn(tags[k]), bands[k - 1].animate.set_fill(opacity=0.06)]
            self.beat(*anims, rt=0.35)
        self.close_seg()

        inv = Inventory(9, "Queue", width=6.6)
        inv.move_to([4.5, 1.3, 0])
        out_line = TokenLine(BFS, 60, MC_WHITE, label="OUT", label_color=MC_GREEN)
        out_line.move_to([4.5, -1.3, 0])
        front = MT("front", 40, MC_GREEN).next_to(inv.slots[0], DOWN, buff=0.4)
        q = []  # (value, mobject) waiting in the chest, front first

        def enqueue(vals, rt=0.35):
            anims = []
            for v in vals:
                m = queue_item(inv, len(q), v)
                q.append((v, m))
                anims.append(FadeIn(m, shift=DOWN * 0.2, scale=1.4))
            self.sfx("pop", 0.3)
            self.beat(LaggedStart(*anims, lag_ratio=0.3), rt=rt)

        def dequeue(k, rt=0.35):
            v, m = q.pop(0)
            self.sfx("click", 0.3)
            self.beat(FadeOut(m, shift=DOWN * 0.6), FadeIn(out_line.upto(k), shift=DOWN * 0.15),
                      *[mm.animate.move_to(inv.slots[j]) for j, (_, mm) in enumerate(q)],
                      pulse(tree.blocks[v], 1.25),
                      rt=rt)

        self.seg(31)
        self.until(at(31, "different branches") - 0.2)
        self.beat(pulse(tree.blocks[3], 1.2), pulse(tree.blocks[10], 1.2), rt=0.5)
        self.until(at(31, "queue") - 0.2)
        self.sfx("chestopen", 0.35)
        self.beat(FadeIn(inv, shift=UP * 0.3), FadeIn(front), *[b.animate.set_fill(opacity=0.03) for b in bands],
                  FadeOut(VGroup(*tags)), rt=0.5)
        self.close_seg()

        self.seg(32)
        self.beat(FadeIn(out_line.box), FadeIn(out_line.label), rt=0.3)
        self.until(at(32, "goes in") - 0.2)
        enqueue([8])
        self.until(at(32, "comes out") - 0.1)
        dequeue(0)
        self.until(at(32, "three and ten") - 0.1)
        enqueue([3, 10])
        self.close_seg()

        self.seg(33)
        self.until(at(33, "Three comes out") - 0.05)
        dequeue(1)
        self.until(at(33, "adds one") - 0.05)
        enqueue([1, 6])
        self.until(at(33, "Ten comes out") - 0.05)
        dequeue(2)
        self.until(at(33, "adds fourteen") - 0.05)
        enqueue([14])
        self.close_seg()

        self.seg(34)
        ws = words_at(34, ["one", "six", "fourteen", "thirteen"], "Then")
        for k, w in enumerate(ws):
            self.until(w - 0.1)
            dequeue(3 + k, rt=0.25)
            if k == 2:
                enqueue([13], rt=0.2)
        self.until(at(34, "level by level") - 0.2)
        self.sfx("levelup", 0.25)
        groups = [VGroup(*[out_line.toks[BFS.index(v)] for v in lv]) for lv in LEVELS]
        self.beat(*[g.animate.set_color(c) for g, c in zip(groups, (MC_GOLD, MC_AQUA, MC_GREEN, MC_PINK))], rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene07_BST(Overlay):
    def construct(self):
        h = hdr("SEARCH TREE", MC_PINK)
        rule = entry("RULE", "left < block < right", MC_PINK)
        place(rule, 0)
        name = chat("binary search tree", MC_GOLD, 44)
        place(name, 1)
        checks = [entry("checks", str(k), MC_WHITE) for k in (1, 2, 3)]
        for c in checks:
            place(c, 2.4)
        logn = boxed(VGroup(MT("balanced:", 44, MC_WHITE), level_text("O(log n)", 0.62)).arrange(RIGHT, buff=0.3))
        place(logn, 3.6)
        on = boxed(VGroup(MT("staircase:", 44, MC_WHITE), MT("O(n)", 52, MC_RED, PIXEL)).arrange(RIGHT, buff=0.3))
        place(on, 4.8)
        hop = pixel_art("hopper", 0.62)

        self.seg(35)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(at(35, "one rule") - 0.1)
        self.beat(FadeIn(rule, shift=LEFT * 0.3), rt=0.35)
        self.until(at(35, "smaller"))
        self.sfx("click", 0.28)
        self.until(at(35, "bigger"))
        self.sfx("click", 0.28)
        self.close_seg()

        self.seg(36)
        self.until(at(36, "binary search") - 0.2)
        self.sfx("orb", 0.3)
        self.beat(FadeIn(name, scale=1.2), rt=0.4)
        self.close_seg()

        self.seg(37)
        self.until(at(37, "hopper") - 0.2)
        self.sfx("chestopen", 0.3)
        self.until(at(37, "Drop") - 0.1)
        self.sfx("pop", 0.3)
        self.close_seg()

        self.seg(38)
        self.until(at(38, "smaller") - 0.1)
        self.sfx("click", 0.3)
        self.beat(FadeIn(checks[0], shift=LEFT * 0.2), rt=0.3)
        self.until(at(38, "goes dark") - 0.1)
        self.sfx("break", 0.25)
        self.close_seg()

        self.seg(39)
        self.until(at(39, "bigger") - 0.1)
        self.sfx("click", 0.3)
        self.beat(Transform(checks[0], checks[1]), rt=0.3)
        self.until(at(39, "there it is") - 0.1)
        self.sfx("challenge", 0.3)
        self.beat(Transform(checks[0], checks[2]), rt=0.3)
        self.until(at(39, "instead of seven") - 0.1)
        self.beat(pulse(checks[0], 1.12), rt=0.4)
        self.close_seg()

        self.seg(40)
        self.until(at(40, "half") - 0.2)
        self.sfx("orb", 0.3)
        self.until(at(40, "log n") - 0.3)
        self.beat(FadeIn(logn, shift=UP * 0.2), rt=0.4)
        self.close_seg()

        self.seg(41)
        self.until(at(41, "sorted") - 0.1)
        for k in range(7):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.25, delay=0.6 + 0.2 * k)
        self.close_seg()

        self.seg(42)
        self.until(at(42, "staircase") - 0.1)
        self.sfx("villager_no1", 0.35)
        self.until(at(42, "It's a row") - 0.1)
        self.beat(FadeIn(on, shift=UP * 0.2), rt=0.4)
        self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)
        self.close_seg()


class NodeBox(VGroup):
    """A block with its two links hanging down; each link ends in a barrier (None) until a child is plugged in."""

    def __init__(self, v, size=0.95, **kwargs):
        super().__init__(**kwargs)
        self.block = Block(v, f"{ORE_OF[v]}_ore", size)
        ends = [self.block.get_bottom() + np.array([dx * size, -0.95 * size, 0]) for dx in (-0.85, 0.85)]
        self.links = [Line(self.block.get_bottom() + np.array([dx * size * 0.3, 0, 0]), e, color=NULL_EDGE,
                           stroke_width=8) for dx, e in zip((-1, 1), ends)]
        self.bars = [pixel_art("barrier", size * 0.55).move_to(e) for e in ends]
        self.add(*self.links, self.block, *self.bars)

    def end(self, side):
        # Where link `side` (0 left, 1 right) ends: the barrier's spot
        return self.bars[side].get_center()

    def put(self, p):
        # Moves the whole node so its block sits at p
        self.shift(np.array(p) - self.block.get_center())
        return self


class Scene08_Node(Base):
    def construct(self):
        h = hdr("NODE IN CODE", MC_GREEN)
        code = code_panel(NODE_CODE, 0, width=7.4)
        code.move_to([CODE_X, 1.85, 0])
        build = code_panel(BUILD_CODE, 0, width=6.8)
        build.move_to([CODE_X, -2.15, 0])
        n8 = NodeBox(8, 1.4).put([3.8, 2.6, 0])
        val = MT("val = 8", 52, MC_WHITE).next_to(n8.block, RIGHT, buff=0.45)
        ln = MT("left", 46, MC_AQUA).next_to(n8.bars[0], LEFT, buff=0.18)
        rn = MT("right", 46, MC_GOLD).next_to(n8.bars[1], RIGHT, buff=0.18)
        bar = line_bar(code, 0, 0)

        self.seg(43)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(code.background), FadeIn(code.line_numbers),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.1), rt=0.9)
        self.until(at(43, "small class") - 0.1)
        self.beat(FadeIn(bar), rt=0.3)
        self.close_seg()

        self.seg(44)
        self.until(at(44, "a value") - 0.1)
        self.beat(Transform(bar, line_bar(code, 2, 2)), FadeIn(n8.block, scale=1.3), FadeIn(val), rt=0.4)
        self.sfx("stone_dig1", 0.3)
        self.until(at(44, "two links") - 0.1)
        self.beat(Transform(bar, line_bar(code, 3, 4)), Create(n8.links[0]), Create(n8.links[1]), FadeIn(ln), FadeIn(rn),
                  rt=0.5)
        self.until(at(44, "None") - 0.2)
        self.sfx("click", 0.3)
        self.beat(LaggedStart(*[FadeIn(b, scale=1.6) for b in n8.bars], lag_ratio=0.3), rt=0.5)
        self.close_seg()

        self.seg(45)
        self.until(at(45, "two barriers") - 0.1)
        self.beat(*[pulse(b, 1.3) for b in n8.bars], rt=0.5)
        self.until(at(45, "doesn't know") - 0.1)
        alone = chat("no tree yet", MC_GRAY, 50).next_to(n8, DOWN, buff=0.5)
        self.beat(FadeIn(alone, shift=UP * 0.2), rt=0.35)
        self.close_seg()

        # The tree grows as the links get connected
        n3 = NodeBox(3, 1.15).put(n8.end(0) + np.array([-0.7, -0.6, 0]))
        n10 = NodeBox(10, 1.15).put(n8.end(1) + np.array([0.7, -0.6, 0]))
        n1 = NodeBox(1, 1.0).put(n3.end(0) + np.array([-0.2, -0.55, 0]))
        root_tag = chat("root", MC_GOLD, 46).next_to(n8.block, LEFT, buff=0.3)
        bbar = line_bar(build, 0, 0, MC_GREEN)

        def plug(parent, side, child, rt=0.5):
            # The barrier pops and the link reaches the new block
            link = Line(parent.links[side].get_start(), child.block.get_top(), color=WOOD, stroke_width=10)
            self.sfx("pop", 0.3)
            self.add(link, parent.block)
            self.beat(FadeOut(parent.bars[side], scale=0.3), FadeOut(parent.links[side]), Create(link),
                      FadeIn(child, shift=DOWN * 0.3), rt=rt)
            return link

        self.seg(46)
        self.beat(FadeOut(alone), FadeOut(val), FadeOut(ln), FadeOut(rn), FadeOut(bar),
                  FadeIn(build.background), FadeIn(build.line_numbers),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in build.code_lines], lag_ratio=0.1), rt=0.6)
        self.until(at(46, "The root") - 0.1)
        self.beat(FadeIn(bbar), FadeIn(root_tag, shift=DOWN * 0.2), rt=0.35)
        self.close_seg()

        self.seg(47)
        self.beat(Transform(bbar, line_bar(build, 1, 1, MC_GREEN)), rt=0.2)
        plug(n8, 0, n3)
        self.until(at(47, "root dot right") - 0.1)
        self.beat(Transform(bbar, line_bar(build, 2, 2, MC_GREEN)), rt=0.2)
        plug(n8, 1, n10)
        self.close_seg()

        # Root, .left, .left: a cursor slides down the rods
        hand = outline(n8.block, MC_YELLOW, 8)
        self.seg(48)
        self.beat(Transform(bbar, line_bar(build, 3, 3, MC_GREEN)), Create(hand), rt=0.3)
        steps = words_at(48, ["left", "left"])
        self.until(steps[0] - 0.1)
        self.sfx("click", 0.3)
        self.beat(hand.animate.move_to(n3.block).scale(1.15 / 1.4), rt=0.35)
        self.until(steps[1] - 0.1)
        self.sfx("click", 0.3)
        self.beat(hand.animate.move_to(n3.end(0)).scale(1.0 / 1.15), rt=0.35)
        plug(n3, 0, n1, rt=0.4)
        self.until(at(48, "Every dot") - 0.1)
        dot = chat(".left = one step down a rod", MC_YELLOW, 44).move_to([5.0, -3.1, 0])
        self.beat(FadeIn(dot, shift=UP * 0.2), FadeOut(hand), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene09_Recursion(Base):
    def construct(self):
        h = hdr("RECURSION", MC_PINK)
        code = code_panel(TREE_SUM, 0, width=7.6)
        code.move_to([CODE_X, 1.55, 0])
        tree = Tree2D(0.95, 3.35, 1.62, 0.95, x0=3.85, nulls=True)
        bar = line_bar(code, 0, 0)
        rules = [chat(t, c, 50) for t, c in (("1. barrier -> 0", MC_RED), ("2. trust your two links", MC_AQUA),
                                               ("3. combine, send it up", MC_GREEN))]
        VGroup(*rules).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([CODE_X, -2.35, 0])
        others = [b for v, b in tree.blocks.items() if v != 3]
        veil = VGroup(*[Square(b.width, fill_color="#000000", fill_opacity=0.6, stroke_width=0).move_to(b) for b in others])
        me = outline(tree.blocks[3], MC_YELLOW, 8, buff=0.08)

        self.seg(49)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(code.background), FadeIn(code.line_numbers),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.1), rt=0.8)
        self.add(tree.rods, tree.null_rods, *tree.block_list(), *tree.bars.values())
        self.beat(FadeIn(tree), rt=0.6)
        self.until(at(49, "adds up") - 0.1)
        self.beat(FadeIn(bar), Transform(bar, line_bar(code, 5, 5)), rt=0.4)
        self.close_seg()

        self.seg(50)
        self.until(at(50, "every branch") - 0.1)
        self.beat(*[pulse(b, 1.12) for b in tree.block_list()], rt=0.6)
        self.until(at(50, "Stand on one") - 0.1)
        self.beat(FadeIn(veil), Create(me), rt=0.5)
        self.close_seg()

        # Rule 1: every barrier sends back a zero
        zeros = [orb_num(0, MC_RED).move_to(b.get_center() + UP * 0.05) for b in tree.bars.values()]

        self.seg(51)
        self.beat(Transform(bar, line_bar(code, 1, 2, MC_RED)), FadeIn(rules[0], shift=UP * 0.2), rt=0.4)
        self.until(at(51, "Every barrier") - 0.1)
        self.sfx("click", 0.3)
        self.beat(*[pulse(b, 1.35) for b in tree.bars.values()], rt=0.4)
        self.beat(LaggedStart(*[FadeIn(z, shift=UP * 0.35) for z in zeros], lag_ratio=0.08), rt=0.6)
        self.finish(*[FadeOut(z, shift=UP * 0.3) for z in zeros], rt=0.35)
        self.close_seg()

        # Rule 2: 3 asks its two links
        ask_l = Arrow(tree.at[3], tree.at[1], color=MC_YELLOW, stroke_width=7, buff=0.42)
        ask_r = Arrow(tree.at[3], tree.at[6], color=MC_YELLOW, stroke_width=7, buff=0.42)
        got1 = orb_num(1, MC_GREEN).move_to(tree.at[1])
        got6 = orb_num(6, MC_GREEN).move_to(tree.at[6])

        self.seg(52)
        self.beat(Transform(bar, line_bar(code, 3, 4, MC_AQUA)), FadeIn(rules[1], shift=UP * 0.2), rt=0.4)
        self.until(at(52, "left subtree") - 0.1)
        self.beat(GrowArrow(ask_l), rt=0.35)
        self.until(at(52, "right one") - 0.1)
        self.beat(GrowArrow(ask_r), rt=0.35)
        self.close_seg()

        self.seg(53)
        self.until(at(53, "gets one") - 0.2)
        self.sfx("orb", 0.3)
        self.beat(FadeOut(ask_l), FadeIn(got1, scale=0.5), rt=0.2)
        self.beat(got1.animate.move_to(tree.at[3] + np.array([-1.2, -0.55, 0])), rt=0.5)
        self.until(at(53, "gets six") - 0.2)
        self.sfx("orb", 0.3)
        self.beat(FadeOut(ask_r), FadeIn(got6, scale=0.5), rt=0.2)
        self.beat(got6.animate.move_to(tree.at[3] + np.array([1.2, -0.55, 0])), rt=0.5)
        self.close_seg()

        # Rule 3: 3 + 1 + 6 = 10 goes up to the root
        total = VGroup(MT("3 + 1 + 6 =", 52, MC_WHITE), MT("10", 60, MC_GREEN, PIXEL)).arrange(RIGHT, buff=0.2)
        total_box = Rectangle(width=total.width + 0.5, height=total.height + 0.35, fill_color="#000000", fill_opacity=0.65,
                              stroke_width=0)
        sum3 = VGroup(total_box, total.move_to(total_box)).move_to([1.3, -3.95, 0])
        up10 = orb_num(10, MC_GREEN).move_to(tree.at[3])

        self.seg(54)
        self.beat(Transform(bar, line_bar(code, 5, 5, MC_GREEN)), FadeIn(rules[2], shift=UP * 0.2), rt=0.4)
        self.until(at(54, "Three plus") - 0.1)
        # Values sink into the block and vanish; parked on its center they covered the number
        self.beat(FadeIn(sum3, shift=UP * 0.2), FadeOut(got1, target_position=tree.at[3], scale=0.3),
                  FadeOut(got6, target_position=tree.at[3], scale=0.3), rt=0.5)
        self.until(at(54, "ten goes up") - 0.2)
        self.sfx("orb", 0.35)
        self.beat(FadeIn(up10, scale=0.5), FadeOut(me), rt=0.3)
        self.beat(up10.animate.move_to(tree.at[8] + np.array([-1.2, 0.15, 0])), rt=0.7)
        self.close_seg()

        up37 = orb_num(37, MC_GREEN).move_to(tree.at[10])
        fin = VGroup(MT("8 + 10 + 37 =", 52, MC_WHITE), MT("55", 64, MC_GOLD, PIXEL)).arrange(RIGHT, buff=0.2)
        fin_box = Rectangle(width=fin.width + 0.5, height=fin.height + 0.35, fill_color="#000000", fill_opacity=0.65,
                            stroke_width=0)
        sum8 = VGroup(fin_box, fin.move_to(fin_box)).move_to([1.3, -3.95, 0])
        t = toast("Advancement Made!", "The tree adds up to 55", w=6.6)
        t.move_to([CODE_X, -2.0, 0]).shift(LEFT * 8)

        self.seg(55)
        self.beat(FadeOut(veil), FadeOut(VGroup(*rules)), rt=0.3)
        self.until(at(55, "thirty seven") - 0.3)
        self.sfx("orb", 0.35)
        self.beat(FadeIn(up37, scale=0.5), rt=0.2)
        self.beat(up37.animate.move_to(tree.at[8] + np.array([1.2, 0.15, 0])), rt=0.7)
        self.until(at(55, "Eight adds") - 0.1)
        self.beat(Transform(sum3, sum8), rt=0.4)
        self.until(at(55, "and the whole") - 0.1)
        self.sfx("challenge", 0.32)
        for d in (0.1, 0.3, 0.5):
            self.sfx("orb", 0.25, delay=d)
        self.beat(t.animate.shift(RIGHT * 8), FadeOut(up10, target_position=tree.at[8], scale=0.3),
                  FadeOut(up37, target_position=tree.at[8], scale=0.3),
                  pulse(tree.blocks[8], 1.3), rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene10_Secret(Base):
    def construct(self):
        h = hdr("THE SECRET", MC_GOLD)
        code = code_panel(TREE_SUM, 0, width=7.8)
        code.move_to([CODE_X, 0.6, 0])
        last = code.code_lines[5]

        def swap(src, color):
            # The last line rewritten, in the same spot and size as the original one
            alt = MCCode(TREE_SUM.rsplit("\n", 1)[0] + "\n    " + src)
            alt.scale(code.code_lines[0].height / alt.code_lines[0].height)
            line = alt.code_lines[5]
            line.move_to(last, aligned_edge=LEFT)
            return line

        cards = []

        def card(lines, tag, color, icon):
            body = VGroup(icon, VGroup(*[MT(s, 50, MC_WHITE) for s in lines]).arrange(DOWN, buff=0.08, aligned_edge=LEFT))
            body.arrange(RIGHT, buff=0.35)
            badge = chat(tag, color, 52)
            g = VGroup(body, badge).arrange(RIGHT, buff=0.4)
            box = Rectangle(width=7.2, height=1.6, fill_color="#000000", fill_opacity=0.6, stroke_width=0)
            if g.width > 6.8:
                g.scale_to_fit_width(6.8)
            g.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
            m = VGroup(box, g)
            m.move_to([4.2, 2.85 - 1.85 * len(cards), 0])
            cards.append(m)
            return m

        c1 = card(["count the blocks", "answer: 7"], "count", MC_GREEN, iso_block("emerald_ore", 0.8))
        c2 = card(["maximum depth", "answer: 4"], "#104", MC_AQUA, iso_block("diamond_ore", 0.8))
        c3 = card(["levels, with", "a queue"], "#102", MC_GOLD, chest_icon(0.8))
        c4 = card(["save the tree", "with barriers"], "#297", MC_RED, pixel_art("barrier", 0.8))

        self.seg(56)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(code), rt=0.6)
        self.until(at(56, "last line") - 0.1)
        bar = line_bar(code, 5, 5, MC_GOLD)
        self.beat(FadeIn(bar), pulse(last, 1.08), rt=0.5)
        self.close_seg()

        self.seg(57)
        l1 = swap("return 1 + left + right", MC_GREEN)
        self.until(at(57, "one plus") - 0.2)
        self.sfx("book_flip1", 0.35)
        self.beat(FadeOut(last, shift=UP * 0.2), FadeIn(l1, shift=UP * 0.2), rt=0.4)
        self.until(at(57, "count") - 0.1)
        self.sfx("pop", 0.3)
        self.beat(FadeIn(c1, shift=LEFT * 0.3), rt=0.4)
        self.close_seg()

        self.seg(58)
        l2 = swap("return 1 + max(left, right)", MC_AQUA)
        self.until(at(58, "bigger side") - 0.4)
        self.sfx("book_flip2", 0.35)
        self.beat(FadeOut(l1, shift=UP * 0.2), FadeIn(l2, shift=UP * 0.2), rt=0.4)
        self.until(at(58, "maximum depth") - 0.1)
        self.sfx("pop", 0.3)
        self.beat(FadeIn(c2, shift=LEFT * 0.3), rt=0.4)
        self.close_seg()

        self.seg(59)
        self.until(at(59, "queue") - 0.2)
        self.sfx("chestopen", 0.3)
        self.beat(FadeIn(c3, shift=LEFT * 0.3), rt=0.4)
        self.close_seg()

        self.seg(60)
        self.until(at(60, "barriers") - 0.2)
        self.sfx("pop", 0.3)
        self.beat(FadeIn(c4, shift=LEFT * 0.3), rt=0.4)
        self.until(at(60, "two ninety") - 0.2)
        self.beat(*[pulse(c, 1.04) for c in cards], rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene11_Outro(Base):
    def construct(self):
        tree = Tree2D(1.2, 3.35, 1.85, 1.35, x0=0)
        others = [b for v, b in tree.blocks.items() if v != 3]
        msg = chat("one block, two rods down", MC_GOLD, 66).move_to([0, -3.75, 0])
        me = outline(tree.blocks[3], MC_YELLOW, 9, buff=0.08)

        self.seg(61)
        self.add(tree.rods, *tree.block_list())
        self.beat(FadeIn(tree), rt=0.6)
        self.until(at(61, "every block") - 0.2)
        self.beat(*[pulse(b, 1.12) for b in tree.block_list()], rt=0.6)
        self.close_seg()

        self.seg(62)
        veil = VGroup(*[Square(b.width, fill_color="#000000", fill_opacity=0.65, stroke_width=0).move_to(b) for b in others])
        # The two rods under 3 light up over the dimmed tree
        lit = VGroup(*[tree.edges[v].copy().set_stroke(MC_YELLOW, width=16) for v in (1, 6)])
        self.beat(FadeIn(veil), tree.rods.animate.set_opacity(0.3), Create(me), rt=0.5)
        self.until(at(62, "standing") - 0.1)
        self.add(lit, tree.blocks[3], me)
        self.beat(Create(lit), FadeIn(msg, shift=UP * 0.2), rt=0.4)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeOut(Group(tree, msg, me, veil, lit)), FadeIn(cover()), rt=1.0)
        self.close_seg()
