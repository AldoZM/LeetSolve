# Vertical teaser of the full guide (../largo): the subtree cut, recursion on the tree, and the last-line trick.


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("HOW TREES", width=6.6).move_to([0, 4.85, 0])
    t2 = stone_title("REALLY WORK", width=7.6).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    tree = Tree2D(0.66, 1.9, 1.05, 0.78, nulls=True)
    tags = VGroup(chat("Binary trees", MC_AQUA, 44), chat("Recursion", MC_GREEN, 44)).arrange(RIGHT, buff=0.25)
    tags.move_to([0, -3.6, 0])
    sub = chat("Full guide on the channel", MC_GOLD, 44).move_to([0, -4.6, 0])
    return VGroup(t1, t2, spl, tree, tags, sub)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        t1, t2, spl, tree, tags, sub = art
        self.add(art)
        code = code_panel(TREE_SUM, -4.1, width=8.4)

        self.seg(0)
        self.beat(pulse(spl), rt=0.8)
        self.sfx("stone_dig1", 0.3, delay=0.3)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.3) for b in tree.block_list()],
                              lag_ratio=0.2), rt=1.5)
        self.until(at(0, "five lines") - 0.3)
        self.sfx("book_flip1", 0.4)
        self.beat(FadeOut(tags), FadeOut(sub), FadeIn(code, shift=UP * 0.2), rt=0.45)
        self.until(at(0, "picture") - 0.2)
        self.beat(*[pulse(b, 1.3) for b in tree.bars.values()], pulse(code, 1.03), rt=0.6)
        self.clear_all(rt=0.45)
        self.close_seg()


class Scene2_Cut(Base):
    def construct(self):
        h = hdr("SUBTREES", MC_GREEN)
        tree = Tree2D(0.8, 3.9, 1.3, 0.92)
        cut = tree.edges[3]
        mid = cut.get_center()
        shears = pixel_art("shears", 1.0).move_to(mid + np.array([1.4, 1.2, 0]))
        sub = VGroup(tree.blocks[3], tree.blocks[1], tree.blocks[6], tree.edges[1], tree.edges[6])
        drop = np.array([-1.9, -2.6, 0]) - tree.blocks[3].get_center()

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.add(tree.rods, *tree.block_list())
        self.beat(FadeIn(VGroup(*tree.block_list())), Create(tree.rods), rt=0.7)
        self.sfx("wood_dig2", 0.3)
        self.beat(FadeIn(shears, scale=1.6), rt=0.35)
        self.until(at(1, "cut") - 0.2)
        self.beat(shears.animate.move_to(mid), rt=0.45)
        self.sfx("shear", 0.5)
        self.beat(Rotate(shears, -0.5, rate_func=there_and_back), cut.animate.set_stroke(MC_RED), rt=0.4)
        self.close_seg()

        self.seg(2)
        self.sfx("break", 0.35)
        self.beat(FadeOut(cut), FadeOut(shears), sub.animate.shift(drop), rt=0.8)
        box = SurroundingRectangle(sub, color=MC_GOLD, buff=0.3, stroke_width=6)
        label = chat("a whole tree", MC_GOLD, 40).next_to(box, DOWN, buff=0.2)
        self.until(at(2, "complete tree") - 0.2)
        self.sfx("orb", 0.35)
        self.beat(Create(box), FadeIn(label, shift=UP * 0.2), rt=0.5)
        self.until(at(2, "three is its root") - 0.1)
        crown = MT("root", 34, MC_GOLD).next_to(tree.blocks[3], UP, buff=0.12)
        self.beat(FadeIn(crown, shift=DOWN * 0.15), pulse(tree.blocks[3], 1.25), rt=0.5)
        self.finish(FadeOut(Group(*self.mobjects[1:])), rt=0.45)
        self.close_seg()

        big = Tree2D(0.8, 3.9, 1.3, 0.92)
        left = SurroundingRectangle(VGroup(big.blocks[3], big.blocks[1], big.blocks[6]), color=MC_AQUA, buff=0.2,
                                    stroke_width=6)
        right = SurroundingRectangle(VGroup(big.blocks[10], big.blocks[14], big.blocks[13]), color=MC_GOLD, buff=0.2,
                                     stroke_width=6)
        me = outline(big.blocks[8], MC_GREEN, 7, buff=0.1)
        eq = VGroup(MT("tree =", 50, MC_WHITE), MT("block", 50, MC_GREEN), MT("+ left tree", 50, MC_AQUA),
                    MT("+ right tree", 50, MC_GOLD)).arrange(DOWN, buff=0.18)
        eq.move_to([0, -2.9, 0])
        eq_box = Rectangle(width=eq.width + 0.7, height=eq.height + 0.45, fill_color="#000000", fill_opacity=0.6,
                           stroke_width=0).move_to(eq)

        self.seg(3)
        self.add(big.rods, *big.block_list())
        self.beat(FadeIn(big), FadeIn(h), rt=0.5)
        self.until(at(3, "root of its own") - 0.2)
        self.beat(Create(left), Create(right), rt=0.6)
        self.until(at(3, "A tree is") - 0.2)
        self.beat(FadeIn(eq_box), FadeIn(eq[0]), rt=0.3)
        self.until(at(3, "a block") - 0.1)
        self.beat(FadeIn(eq[1]), Create(me), rt=0.3)
        self.until(at(3, "left tree") - 0.1)
        self.beat(FadeIn(eq[2]), pulse(left, 1.05), rt=0.35)
        self.until(at(3, "right tree") - 0.1)
        self.beat(FadeIn(eq[3]), pulse(right, 1.05), rt=0.35)
        self.clear_all()
        self.close_seg()


class Scene3_Recursion(Base):
    def construct(self):
        h = hdr("RECURSION", MC_PINK)
        tree = Tree2D(0.66, 4.15, 1.12, 0.74, nulls=True)
        code = code_panel(TREE_SUM, -3.55, width=8.4)
        bar = line_bar(code, 0, 0)
        rule = [chat(t, c, 40).move_to([0, -1.25, 0]) for t, c in
                (("1. barrier -> 0", MC_RED), ("2. trust your two links", MC_AQUA), ("3. combine, send it up", MC_GREEN))]
        others = [b for v, b in tree.blocks.items() if v != 3]
        veil = VGroup(*[Square(b.width, fill_color="#000000", fill_opacity=0.6, stroke_width=0).move_to(b) for b in others])
        me = outline(tree.blocks[3], MC_YELLOW, 8, buff=0.08)

        self.seg(4)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.add(tree.rods, tree.null_rods, *tree.block_list(), *tree.bars.values())
        self.beat(FadeIn(tree), rt=0.5)
        self.until(at(4, "This function") - 0.2)
        self.beat(FadeIn(code, shift=UP * 0.2), rt=0.5)
        self.beat(FadeIn(bar), rt=0.2)
        self.close_seg()

        self.seg(5)
        self.until(at(5, "one block") - 0.2)
        self.beat(FadeIn(veil), Create(me), rt=0.5)
        self.close_seg()

        zeros = [orb_num(0, MC_RED, 34).move_to(b.get_center() + UP * 0.05) for b in tree.bars.values()]
        self.seg(6)
        self.beat(Transform(bar, line_bar(code, 1, 2, MC_RED)), FadeIn(rule[0], shift=UP * 0.2), rt=0.4)
        self.until(at(6, "Every barrier") - 0.1)
        self.sfx("click", 0.3)
        self.beat(*[pulse(b, 1.35) for b in tree.bars.values()], rt=0.4)
        self.beat(LaggedStart(*[FadeIn(z, shift=UP * 0.3) for z in zeros], lag_ratio=0.08), rt=0.6)
        self.finish(*[FadeOut(z, shift=UP * 0.3) for z in zeros], rt=0.35)
        self.close_seg()

        ask_l = Arrow(tree.at[3], tree.at[1], color=MC_YELLOW, stroke_width=7, buff=0.38)
        ask_r = Arrow(tree.at[3], tree.at[6], color=MC_YELLOW, stroke_width=7, buff=0.38)
        got1 = orb_num(1, MC_GREEN).move_to(tree.at[1])
        got6 = orb_num(6, MC_GREEN).move_to(tree.at[6])

        self.seg(7)
        self.beat(Transform(bar, line_bar(code, 3, 4, MC_AQUA)), Transform(rule[0], rule[1]), rt=0.4)
        self.until(at(7, "left subtree") - 0.1)
        self.beat(GrowArrow(ask_l), rt=0.3)
        self.sfx("orb", 0.3)
        self.beat(FadeOut(ask_l), FadeIn(got1, scale=0.5), rt=0.2)
        self.beat(got1.animate.move_to(tree.at[3] + np.array([-0.85, -0.5, 0])), rt=0.4)
        self.until(at(7, "right one") - 0.1)
        self.beat(GrowArrow(ask_r), rt=0.3)
        self.sfx("orb", 0.3)
        self.beat(FadeOut(ask_r), FadeIn(got6, scale=0.5), rt=0.2)
        self.beat(got6.animate.move_to(tree.at[3] + np.array([0.85, -0.5, 0])), rt=0.4)
        self.close_seg()

        total = VGroup(MT("3 + 1 + 6 =", 44, MC_WHITE), MT("10", 52, MC_GREEN, PIXEL)).arrange(RIGHT, buff=0.2)
        up10 = orb_num(10, MC_GREEN, 44).move_to(tree.at[3])
        self.seg(8)
        self.beat(Transform(bar, line_bar(code, 5, 5, MC_GREEN)), Transform(rule[0], rule[2]), rt=0.4)
        self.until(at(8, "Three plus") - 0.1)
        total.move_to([0, -1.25, 0])
        box = Rectangle(width=total.width + 0.5, height=total.height + 0.35, fill_color="#000000", fill_opacity=0.65,
                        stroke_width=0).move_to(total)
        sum3 = VGroup(box, total)
        self.beat(FadeOut(rule[0]), FadeIn(sum3, shift=UP * 0.2), got1.animate.move_to(tree.at[3]),
                  got6.animate.move_to(tree.at[3]), rt=0.5)
        self.until(at(8, "ten goes up") - 0.2)
        self.sfx("orb", 0.35)
        self.beat(FadeOut(got1), FadeOut(got6), FadeIn(up10, scale=0.5), FadeOut(me), rt=0.3)
        self.beat(up10.animate.move_to(tree.at[8] + np.array([-0.85, 0.15, 0])), rt=0.7)
        self.close_seg()

        up37 = orb_num(37, MC_GREEN, 44).move_to(tree.at[10])
        fin = VGroup(MT("8 + 10 + 37 =", 44, MC_WHITE), MT("55", 56, MC_GOLD, PIXEL)).arrange(RIGHT, buff=0.2)
        fin.move_to([0, -1.25, 0])
        fbox = Rectangle(width=fin.width + 0.5, height=fin.height + 0.35, fill_color="#000000", fill_opacity=0.65,
                         stroke_width=0).move_to(fin)
        sum8 = VGroup(fbox, fin)
        t = toast("Advancement Made!", "The tree adds up to 55", w=5.6)
        t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.25).shift(RIGHT * 7)

        self.seg(9)
        self.beat(FadeOut(veil), rt=0.3)
        self.until(at(9, "thirty seven") - 0.3)
        self.sfx("orb", 0.35)
        self.beat(FadeIn(up37, scale=0.5), rt=0.2)
        self.beat(up37.animate.move_to(tree.at[8] + np.array([0.85, 0.15, 0])), rt=0.7)
        self.until(at(9, "Eight adds") - 0.1)
        self.beat(Transform(sum3, sum8), rt=0.4)
        self.until(at(9, "fifty five") - 0.4)
        self.sfx("challenge", 0.32)
        for d in (0.1, 0.3, 0.5):
            self.sfx("orb", 0.25, delay=d)
        self.beat(t.animate.shift(LEFT * 7), FadeOut(h), up10.animate.move_to(tree.at[8]), up37.animate.move_to(tree.at[8]),
                  pulse(tree.blocks[8], 1.3), rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene4_Secret(Base):
    def construct(self):
        h = hdr("THE SECRET", MC_GOLD)
        code = code_panel(TREE_SUM, 2.3, width=8.4)
        last = code.code_lines[5]
        alt = MCCode(TREE_SUM.rsplit("\n", 1)[0] + "\n    return 1 + max(left, right)")
        alt.scale(code.code_lines[0].height / alt.code_lines[0].height)
        new = alt.code_lines[5]
        new.move_to(last, aligned_edge=LEFT)
        bar = line_bar(code, 5, 5, MC_GOLD)
        tree = Tree2D(0.6, -0.4, 0.95, 0.62)
        depth = VGroup(MT("maximum depth =", 48, MC_WHITE), MT("4", 56, MC_AQUA, PIXEL)).arrange(RIGHT, buff=0.25)
        dbox = Rectangle(width=depth.width + 0.5, height=depth.height + 0.35, fill_color="#000000", fill_opacity=0.65,
                         stroke_width=0)
        res = VGroup(dbox, depth.move_to(dbox)).move_to([0, -4.5, 0])
        tag = chat("LeetCode #104", MC_AQUA, 48).move_to([0, -0.6, 0])
        path = [tree.blocks[v] for v in (8, 10, 14, 13)]

        self.seg(10)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(code, shift=UP * 0.2), rt=0.6)
        self.until(at(10, "last line") - 0.1)
        self.beat(FadeIn(bar), pulse(last, 1.08), rt=0.5)
        self.close_seg()

        self.seg(11)
        self.until(at(11, "bigger side") - 0.4)
        self.sfx("book_flip2", 0.35)
        self.beat(FadeOut(last, shift=UP * 0.2), FadeIn(new, shift=UP * 0.2), rt=0.4)
        self.add(tree.rods, *tree.block_list())
        self.beat(FadeIn(tree.shift(DOWN * 0.6)), rt=0.4)
        self.until(at(11, "maximum depth") - 0.2)
        for k, b in enumerate(path):
            self.sfx("click", 0.28, delay=0.15 * k)
        self.beat(LaggedStart(*[pulse(b, 1.3) for b in path], lag_ratio=0.3), rt=0.8)
        self.beat(FadeIn(res, shift=UP * 0.2), rt=0.35)
        self.until(at(11, "LeetCode") - 0.2)
        self.sfx("orb", 0.35)
        self.beat(FadeIn(tag, scale=1.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene5_Outro(Base):
    def construct(self):
        topics = VGroup(*[chat(s, c, 50) for s, c in (("traversals", MC_AQUA), ("queues", MC_GOLD), ("search trees", MC_PINK))])
        topics.arrange(DOWN, buff=0.3).move_to([0, 1.6, 0])
        icons = VGroup(pixel_art("lead", 0.8), chest_icon(0.8), pixel_art("hopper", 0.8))
        for ic, tp in zip(icons, topics):
            ic.next_to(tp, LEFT, buff=0.3)
        full = chat("Full guide on the channel", MC_GREEN, 56).move_to([0, -1.2, 0])

        self.seg(12)
        for k, (ic, tp) in enumerate(zip(icons, topics)):
            self.sfx("pop", 0.3, delay=0.2 + 0.3 * k)
        self.beat(LaggedStart(*[FadeIn(VGroup(ic, tp), shift=UP * 0.2) for ic, tp in zip(icons, topics)], lag_ratio=0.3),
                  rt=1.0)
        self.until(at(12, "on the channel") - 0.4)
        self.sfx("levelup", 0.25)
        self.beat(FadeIn(full, scale=1.2), rt=0.4)
        self.until(DUR[12] - 1.4)
        self.beat(FadeOut(Group(topics, icons, full)), rt=0.35)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.8)
        self.close_seg()
