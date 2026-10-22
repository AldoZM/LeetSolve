WALK = json.load(open('walk.json', encoding='utf-8'))
NODES = WALK["nodes"]
EVENTS = WALK["events"]
SPEECH = WALK["speech"]
KEYS = WALK["keys"]
WORDS = WALK["words"]
WOOD = "#9C7A48"

CODE = """def letterCombinations(digits):
    keys = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
            "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    out = []
    def go(i, path):
        if i == len(digits):
            out.append(path)
            return
        for ch in keys[digits[i]]:
            go(i + 1, path + ch)
    go(0, "")
    return out if digits else []"""

LOOPS2 = """for a in "abc":
    for b in "def":
        out.append(a + b)"""

LOOPS4 = """for a in "abc":
    for b in "def":
        for c in "ghi":
            for d in "jkl":
                out.append(a + b + c + d)"""


def at(i, phrase, nth=0):
    # Seconds into line i where the nth `phrase` starts: even speaking rate between the measured start and end of speech
    text = SUBS[i]['text']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
    t0, t1 = SPEECH[i]
    return min(SUBS[i]['duration_s'] - 0.1, t0 + (t1 - t0) * k / len(text))


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def pulse(m, k=1.15):
    # Emphasis that keeps the pixel art's colors (Indicate would paint it one flat color)
    return m.animate(rate_func=there_and_back).scale(k)


def tex_of(n):
    return "stone" if n["ore"] == "stone" else f"{n['ore']}_ore"


class Tree2D(VGroup):
    """The letter tree as blocks joined by wooden rods; blocks[i] is node i (0 = the digits, 1-3 = a b c, 4-12 = leaves)."""

    def __init__(self, size, top, dy, sx, **kwargs):
        super().__init__(**kwargs)
        self.pos = [np.array([n["x"] * sx, top - n["lvl"] * dy, 0]) for n in NODES]
        self.rods = VGroup(*[Line(self.pos[n["parent"]], self.pos[i], color=WOOD, stroke_width=10 * size)
                             for i, n in enumerate(NODES) if n["parent"] is not None])
        self.blocks = VGroup(*[Block(n["label"], tex_of(n), size).move_to(self.pos[i]) for i, n in enumerate(NODES)])
        for b in self.blocks:
            # A dark backing under the letter: white on the speckled gold ore was hard to read
            back = Rectangle(width=b.num.width + 0.1 * size, height=b.num.height + 0.08 * size, fill_color="#000000",
                             fill_opacity=0.45, stroke_width=0).move_to(b.num)
            b.remove(b.num)
            b.add(back, b.num)
        # Rods first, so the blocks are drawn on top of them
        self.add(self.rods, self.blocks)

    def level(self, L):
        return VGroup(*[b for b, n in zip(self.blocks, NODES) if n["lvl"] == L])

    def rods_to(self, L):
        kids = [n for n in NODES if n["parent"] is not None]
        return VGroup(*[r for r, n in zip(self.rods, kids) if n["lvl"] == L])


def key_cap(d, w=1.9, h=1.15):
    # A phone key made of stone: the digit on top, its letters under it in yellow (key 1 has none)
    face = pixel_art("stone", w, h)
    edge = Rectangle(width=w, height=h, stroke_color="#000000", stroke_width=4, stroke_opacity=0.7, fill_opacity=0)
    num = MT(d, 40, MC_WHITE, PIXEL)
    num.scale_to_fit_height(h * 0.3)
    num.move_to(face.get_center() + UP * h * 0.18)
    letters = MT(KEYS.get(d, " "), 40, MC_YELLOW, PIXEL)
    letters.scale_to_fit_height(h * 0.22)
    letters.move_to(face.get_center() + DOWN * h * 0.24)
    cap = VGroup(face, edge, num, letters)
    cap.letters = letters
    return cap


def veil(m, op=0.55):
    # Darkens pixel art without touching its colors (set_opacity would fill the block's frame)
    return Rectangle(width=m.width, height=m.height, fill_color="#000000", fill_opacity=op, stroke_width=0).move_to(m)


def word_item(inv, k, word):
    # A saved word in chest slot k: a book and quill, with the word where the game prints stack counts
    u = inv.u
    icon = pixel_art("writable_book", 15 * u)
    w = gui_text(word, MC_WHITE, u * 1.15)
    w.move_to(icon.get_corner(DR) + np.array([1.5 * u, -0.5 * u, 0]), aligned_edge=DR)
    item = VGroup(icon, w)
    item.move_to(inv.slots[k])
    return item


def path_badge(p):
    return chat(f'path = "{p}"', MC_YELLOW, 42).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("LETTER", width=4.6).move_to([0, 4.85, 0])
    t2 = stone_title("COMBINATIONS", width=8.2).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    tree = Tree2D(0.62, 2.0, 1.05, 0.8)
    words = chat(" ".join(WORDS), MC_GOLD, 36).move_to([0, -1.45, 0])
    tags = VGroup(chat("LeetCode #17", MC_AQUA, 40), chat("Medium", MC_GOLD, 40), chat("Backtracking", MC_GREEN, 40))
    tags.arrange(RIGHT, buff=0.2).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, tree, words, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, tree, words, tags = art
        self.add(art)

        self.seg(0)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.7)
        # The tree hops one level at a time, top to bottom
        self.sfx("stone_dig1", 0.3, delay=0.25)
        self.beat(LaggedStart(*[AnimationGroup(*[b.animate(rate_func=there_and_back).shift(UP * 0.3) for b in tree.level(L)])
                                for L in range(3)], lag_ratio=0.35), rt=1.4)
        self.sfx("orb", 0.3)
        self.beat(pulse(words, 1.08), rt=0.7)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.7)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        cap_list = [key_cap(str(d)) for d in range(1, 10)]
        caps = VGroup(*cap_list)
        caps.arrange_in_grid(rows=3, cols=3, buff=0.2)
        caps.move_to([0, 2.25, 0])
        # The letters come in later, on "maps to a few letters"
        letters = [c.letters for c in cap_list[1:]]
        for c in cap_list:
            c.remove(c.letters)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        for k in range(9):
            self.sfx("click", 0.22, delay=0.07 * k + 0.1)
        self.beat(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in caps], lag_ratio=0.1), rt=1.0)
        self.until(at(1, "two to nine") - 0.1)
        self.beat(LaggedStart(*[pulse(c, 1.08) for c in cap_list[1:]], lag_ratio=0.1), rt=0.9)
        self.until(at(1, "maps to") - 0.1)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(*[FadeIn(l, shift=DOWN * 0.1) for l in letters], lag_ratio=0.08), rt=0.8)
        self.close_seg()

        digits = chat('digits = "23"', MC_WHITE, 52).move_to([0, -0.45, 0])
        marks = VGroup(*[Rectangle(width=cap_list[k][0].width + 0.1, height=cap_list[k][0].height + 0.1, stroke_color=MC_YELLOW,
                                   stroke_width=8, fill_opacity=0).move_to(cap_list[k][0]) for k in (1, 2)])
        veils = VGroup(*[veil(cap_list[k][0]) for k in (0, 3, 4, 5, 6, 7, 8)])
        rows = VGroup(*[chat("  ".join(WORDS[3 * r:3 * r + 3]), MC_GOLD, 46) for r in range(3)])
        rows.arrange(DOWN, buff=0.2).move_to([0, -2.55, 0])
        nine = MT("= 9 words", 56, MC_GREEN, PIXEL).move_to([0, -4.45, 0])

        self.seg(2)
        self.until(at(2, "string of digits") - 0.2)
        self.sfx("click", 0.3)
        self.beat(FadeIn(digits, shift=UP * 0.2), Create(marks), FadeIn(veils), rt=0.5)
        self.until(at(2, "every word") - 0.1)
        for r in range(3):
            self.sfx("pop", 0.28, delay=0.2 * r)
        self.beat(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3), rt=0.8)
        self.until(at(2, "nine words") - 0.15)
        self.sfx("orb", 0.3)
        self.beat(FadeIn(nine, scale=1.3), rt=0.45)
        self.clear_all()
        self.close_seg()


class Scene3_Loops(Base):
    def construct(self):
        h = hdr("NESTED LOOPS", MC_RED)
        digits = chat('digits = "23"', MC_WHITE, 50).move_to([0, 3.9, 0])
        code = code_panel(LOOPS2, 1.75, width=6.4)
        tags = VGroup(*[MT(f"digit {d}", 36, MC_YELLOW).next_to(code.code_lines[k], RIGHT, buff=0.35) for k, d in enumerate("23")])

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(digits, shift=DOWN * 0.2), rt=0.4)
        self.until(at(3, "we could") - 0.3)
        self.sfx("book_flip1", 0.35)
        self.beat(FadeIn(code, shift=UP * 0.2), rt=0.5)
        self.until(at(3, "one loop") - 0.1)
        bar = line_bar(code, 0, 0, MC_YELLOW)
        self.sfx("click", 0.28)
        self.beat(FadeIn(bar), FadeIn(tags[0]), rt=0.3)
        self.sfx("click", 0.28)
        self.beat(Transform(bar, line_bar(code, 1, 1, MC_YELLOW)), FadeIn(tags[1]), rt=0.3)
        self.close_seg()

        digits4 = chat('digits = "2345"', MC_WHITE, 50).move_to([0, 3.9, 0])
        code4 = code_panel(LOOPS4, 1.2, width=8.0)
        loops = line_bar(code4, 0, 3, MC_RED)
        four = MT("4 loops", 48, MC_RED).next_to(code4, DOWN, buff=0.3)
        many = MT("how many loops?", 60, MC_RED).move_to([0, -2.3, 0])
        lens = MT("1 digit? 7 digits?", 44, MC_GRAY).move_to([0, -3.4, 0])

        self.seg(4)
        self.until(at(4, "input length") - 0.1)
        self.sfx("click", 0.3)
        self.beat(Transform(digits, digits4), rt=0.4)
        self.until(at(4, "Four digits") - 0.1)
        self.sfx("book_flip2", 0.35)
        self.beat(FadeOut(bar), FadeOut(tags), FadeOut(code), FadeIn(code4, shift=DOWN * 0.2), rt=0.5)
        self.until(at(4, "four nested") - 0.1)
        self.beat(FadeIn(loops), FadeIn(four), rt=0.4)
        self.until(at(4, "the code can't") - 0.1)
        self.sfx("villager_no1", 0.4)
        self.beat(FadeIn(many, scale=1.3), rt=0.45)
        self.beat(FadeIn(lens, shift=UP * 0.15), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("BACKTRACKING", MC_GOLD)
        tree = Tree2D(0.75, 3.7, 1.55, 0.88)
        lv1 = chat("level 1: digit 2 = a b c", MC_WHITE, 38)
        lv2 = chat("level 2: digit 3 = d e f", MC_WHITE, 38)
        VGroup(lv1, lv2).arrange(DOWN, buff=0.18).move_to([0, -0.75, 0])
        root = tree.blocks[0]
        l1, l2 = list(tree.level(1)), list(tree.level(2))

        self.seg(5)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(root, shift=DOWN * 0.3), rt=0.45)
        self.until(at(5, "one letter") - 0.2)
        # Rods go behind the blocks: added first, then the blocks re-added on top
        for b in l1:
            b.shift(UP * 6)
        self.add(tree.rods_to(1), root, *l1)
        for k in range(3):
            self.sfx(f"stone_dig{k + 1}", 0.28, delay=0.12 * k + 0.35)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 6) for b in l1], lag_ratio=0.15),
                  Create(tree.rods_to(1)), rt=0.8)
        self.beat(FadeIn(lv1, shift=UP * 0.1), rt=0.3)
        self.until(at(5, "one digit per level") - 0.1)
        for b in l2:
            b.shift(UP * 7)
        self.add(tree.rods_to(2), *l2)
        for k in range(9):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.24, delay=0.06 * k + 0.35)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 7) for b in l2], lag_ratio=0.08),
                  Create(tree.rods_to(2)), rt=0.9)
        self.beat(FadeIn(lv2, shift=UP * 0.1), rt=0.3)
        self.close_seg()

        a, ad, ae = tree.blocks[1], tree.blocks[4], tree.blocks[5]
        cur = outline(a, MC_YELLOW, 9)
        st = {"path": chat('path = ""', MC_YELLOW, 48).move_to([0, -2.75, 0])}
        step = {"m": None}

        def set_path(p, rt=0.2):
            self.beat(Transform(st["path"], chat(f'path = "{p}"', MC_YELLOW, 48).move_to([0, -2.75, 0])), rt=rt)

        def set_step(text, color):
            new = chat(text, color, 46).move_to([0, -4.0, 0])
            if step["m"] is None:
                step["m"] = new
                self.beat(FadeIn(new, shift=UP * 0.15), rt=0.2)
            else:
                self.beat(Transform(step["m"], new), rt=0.2)

        self.seg(6)
        self.beat(FadeIn(st["path"]), rt=0.3)
        self.until(at(6, "try every letter") - 0.1)
        self.sfx("click", 0.28)
        self.beat(LaggedStart(*[pulse(b, 1.15) for b in l1], lag_ratio=0.25), rt=0.7)
        self.sfx("click", 0.3)
        self.beat(Create(cur), rt=0.2)
        set_path("a")
        set_step("choose a letter", MC_YELLOW)
        self.until(at(6, "go one level deeper"))
        self.sfx("stone_step1", 0.32)
        self.beat(cur.animate.move_to(ad), rt=0.3)
        set_path("ad")
        set_step("go one level deeper", MC_GREEN)
        self.until(at(6, "undo the choice") - 0.1)
        self.sfx("stone_step2", 0.32)
        self.beat(cur.animate.move_to(a), rt=0.3)
        set_path("a")
        set_step("undo: back up", MC_AQUA)
        self.until(at(6, "try the next") - 0.1)
        self.sfx("stone_step3", 0.32)
        self.beat(cur.animate.move_to(ae), rt=0.3)
        set_path("ae")
        set_step("next letter: e", MC_YELLOW)
        self.close_seg()

        done = outline(ae, MC_GREEN, 9)
        rule = chat("len(path) == len(digits)", MC_GREEN, 44).move_to([0, -4.0, 0])
        chest = chest_icon(1.0).move_to([3.3, -2.75, 0])
        book = pixel_art("writable_book", 0.6).move_to(st["path"])

        self.seg(7)
        self.until(at(7, "as long as") - 0.2)
        self.sfx("click", 0.3)
        self.beat(Transform(step["m"], rule), rt=0.35)
        self.until(at(7, "complete") - 0.1)
        self.sfx("orb", 0.3)
        self.sfx("chestopen", 0.28, delay=0.25)
        self.beat(Transform(cur, done), pulse(ae, 1.2), FadeIn(chest, scale=0.6), rt=0.4)
        self.until(at(7, "Save it") - 0.1)
        self.add(book)
        self.sfx("pop", 0.35, delay=0.3)
        self.beat(book.animate.move_to(chest).scale(0.5), rt=0.35)
        self.beat(FadeOut(book), rt=0.15)
        self.clear_all(rt=0.4)
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        FLY = 0.35  # same as three/mundo.html: seconds a word flies from its leaf to its slot
        h = hdr("BACKTRACK", MC_GREEN)
        inv = Inventory(9, "Chest")
        inv.move_to([0, -1.15, 0])
        code = code_panel(CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 10, 10, MC_YELLOW)
        items = [word_item(inv, k, w) for k, w in enumerate(WORDS)]
        st = {"badge": None}

        def T(spec):
            return seg_time(W["first"], spec)

        ev = [(T(W[key]), key, None) for key in ("inv_in", "keys_bar", "complete", "toast", "nine", "full")]
        ev += [(T(spec), "recap", k + 1) for k, spec in enumerate(W["recap"])]
        ev += [(T(spec), "drop", ch) for ch, spec in W["drop"].items()]
        times = [T(e["t"]) for e in EVENTS]
        for k, (e, t) in enumerate(zip(EVENTS, times)):
            nxt = times[k + 1] if k + 1 < len(times) else 1e9
            leaf = NODES[e["node"]]["lvl"] == 2
            if e["kind"] == "save":
                ev += [(t, "save", k), (t + FLY * 0.7, "land", k)]
            elif e["kind"] == "push" and not (leaf and nxt - t < 0.2):
                ev.append((t, "push", k))
            elif e["kind"] == "pop" and nxt - t > 0.2:
                # Quick pops between two leaves are drawn by the next push; slow ones get their own beat
                ev.append((t, "pop", k))
        ev.sort(key=lambda e: e[0])

        def move_bar(k0, k1, color, rt=0.1):
            self.beat(Transform(bar, line_bar(code, k0, k1, color)), rt=rt)

        def badge(p, rt=0.1):
            new = path_badge(p)
            if st["badge"] is None:
                st["badge"] = new
                self.beat(FadeIn(new, shift=LEFT * 0.2), rt=0.2)
            else:
                self.beat(Transform(st["badge"], new), rt=rt)

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(code, shift=UP * 0.3), rt=0.45)
            self.beat(FadeIn(bar), rt=0.15)

        def on(kind, k):
            e = EVENTS[k] if kind in ("push", "pop", "save", "land") else None
            if kind == "inv_in":
                self.sfx("chestopen", 0.35)
                self.beat(FadeIn(inv, shift=UP * 0.3), rt=0.4)
            elif kind == "keys_bar":
                move_bar(1, 2, MC_AQUA, rt=0.25)
            elif kind == "drop":
                # The letter blocks land about 0.35 s after they start falling in the 3D clip
                self.sfx("stone_dig%d" % ("abcdef".index(k) % 4 + 1), 0.3, delay=0.35)
            elif kind == "push":
                self.sfx("click", 0.22)
                move_bar(9, 9, MC_YELLOW, rt=0.08)
                badge(e["path"], rt=0.08)
            elif kind == "complete":
                self.sfx("orb", 0.25)
                move_bar(5, 5, MC_GOLD, rt=0.15)
            elif kind == "save":
                move_bar(6, 6, MC_GREEN, rt=0.08)
                badge(e["path"], rt=0.06)
            elif kind == "land":
                self.sfx("pop", 0.32)
                self.beat(FadeIn(items[e["slot"]], scale=1.6), rt=0.1)
            elif kind == "pop":
                leaf = NODES[e["node"]]["lvl"] == 2
                parent = NODES[NODES[e["node"]]["parent"]]["path"]
                self.sfx("stone_step%d" % (k % 6 + 1), 0.28)
                if leaf:
                    move_bar(7, 7, MC_GRAY, rt=0.1)
                else:
                    move_bar(8, 8, MC_AQUA, rt=0.1)
                badge(parent, rt=0.1)
            elif kind == "recap":
                self.beat(pulse(items[k], 1.3), rt=0.3)
            elif kind == "toast":
                t = toast("Advancement Made!", "Every word found", w=4.6)
                t.move_to([0, 5.5, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                self.beat(FadeOut(st["badge"]), rt=0.15)
                self.beat(t.animate.shift(LEFT * 7), Transform(bar, line_bar(code, 11, 11, MC_GREEN)), rt=0.5)
            elif kind == "nine":
                self.sfx("book_put", 0.3)
                self.beat(Transform(inv.title, inv.title_for("Chest: 9 words")),
                          LaggedStart(*[pulse(it, 1.25) for it in items], lag_ratio=0.08), rt=0.8)
            elif kind == "full":
                self.sfx("chestclosed", 0.3)
                self.beat(pulse(inv, 1.04), rt=0.4)

        def on_last():
            # The tree leaves the 3D clip when the walk ends; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        k7, k9 = key_cap("7"), key_cap("9")
        caps = VGroup(k7, k9).arrange(RIGHT, buff=0.5).move_to([0, 3.4, 0])
        upto = MT("up to 4 letters", 44, MC_GRAY).move_to([0, 2.25, 0])
        words = MT("4^n words", 64, MC_GOLD, PIXEL).move_to([0, 1.05, 0])
        each = MT("n letters each", 46, MC_WHITE).move_to([0, 0.05, 0])

        self.seg(14)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(at(14, "up to four") - 0.2)
        self.sfx("click", 0.28)
        self.beat(FadeIn(caps, shift=DOWN * 0.2), rt=0.4)
        self.beat(pulse(k7.letters, 1.25), pulse(k9.letters, 1.25), FadeIn(upto), rt=0.5)
        self.until(at(14, "four to the n") - 0.1)
        self.sfx("pop", 0.3)
        self.beat(FadeIn(words, scale=1.3), rt=0.45)
        self.until(at(14, "n letters") - 0.15)
        self.sfx("click", 0.28)
        self.beat(FadeIn(each, shift=UP * 0.15), rt=0.4)
        self.close_seg()

        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n x 4^n)", 0.95)).arrange(RIGHT, buff=0.4).move_to([0, -1.45, 0])
        sp = VGroup(MT("space", 56, MC_GRAY), level_text("O(n)", 0.95)).arrange(RIGHT, buff=0.4).move_to([0, -3.0, 0])
        deep = MT("n levels deep", 40, MC_WHITE).move_to([0, -4.1, 0])

        self.seg(15)
        self.until(at(15, "n times") - 0.25)
        for d in (0.0, 0.25):
            self.sfx("orb", 0.25, delay=d)
        self.beat(FadeIn(tm, shift=UP * 0.2), rt=0.45)
        self.until(at(15, "The recursion") - 0.1)
        self.sfx("stone_step2", 0.3)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.45)
        self.until(at(15, "n levels") - 0.1)
        self.beat(FadeIn(deep, shift=UP * 0.15), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.6, width=8.4)
        bar = line_bar(code, 8, 8, MC_GOLD)
        steps = VGroup(chat("choose", MC_GOLD, 44), chat("go deeper", MC_YELLOW, 44), chat("undo", MC_AQUA, 44))
        steps.arrange(RIGHT, buff=0.3).move_to([0, -0.85, 0])

        self.seg(16)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.06), FadeIn(code.line_numbers),
                  rt=0.6)
        self.until(at(16, "Choose") - 0.05)
        self.beat(FadeIn(bar), FadeIn(steps[0], shift=UP * 0.1), rt=0.25)
        self.until(at(16, "go deeper") - 0.05)
        self.beat(Transform(bar, line_bar(code, 9, 9, MC_YELLOW)), FadeIn(steps[1], shift=UP * 0.1), rt=0.25)
        self.until(at(16, "undo") - 0.05)
        self.beat(Transform(bar, line_bar(code, 8, 8, MC_AQUA)), FadeIn(steps[2], shift=UP * 0.1), rt=0.25)
        self.until(at(16, "whole template") - 0.1)
        self.beat(Transform(bar, line_bar(code, 4, 9, MC_GREEN)), rt=0.3)
        self.close_seg()

        self.seg(17)
        msg = chat("One choice at a time", MC_GOLD, 58)
        msg.move_to([0, -2.3, 0])
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.4)
        self.until(1.5)
        self.beat(FadeOut(Group(code, bar, msg, steps)), rt=0.45)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.9)
        self.close_seg()
