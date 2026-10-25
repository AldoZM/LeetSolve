# Short 2 of the tree guide: the depth-first walk (lines 20-25 of the long video), cut right after preorder.
# The 3D tree fills the upper half of the frame; the text goes in rows under it.
NAMES = {1: "one", 3: "three", 6: "six", 8: "eight", 10: "ten", 13: "thirteen", 14: "fourteen"}
ROW_W = 8.2
ROW_Y = (-2.0, -3.2)  # the two text rows under the tree
CARD = len(SUBS) - 1  # the silent last line: the "full video" card


def entry(key, desc, color):
    # The word in color and what it means, in a chat box
    row = VGroup(MT(key, 54, color), MT(desc, 48, MC_WHITE)).arrange(RIGHT, buff=0.3)
    box = Rectangle(width=row.width + 0.5, height=0.86, fill_color="#000000", fill_opacity=0.6, stroke_width=0)
    return fit(VGroup(box, row.move_to(box)))


def fit(m, w=ROW_W):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def walk_header():
    h = hdr("DEPTH FIRST", MC_AQUA, 50)
    lead = pixel_art("lead", 0.7).next_to(h, RIGHT, buff=0.25)
    return h, lead


def moment_chips():
    chips = VGroup(chat("down", MC_AQUA, 52), chat("underneath", MC_GOLD, 52), chat("back up", MC_PINK, 52))
    chips.arrange(RIGHT, buff=0.2)
    return fit(chips).move_to([0, ROW_Y[0], 0])


def pre_line():
    ln = TokenLine(PRE, 58, MC_WHITE, label="PRE ", label_color=MC_AQUA)
    return fit(ln).move_to([0, ROW_Y[1], 0])


def intro_cover(tag, color):
    # Title of the long guide plus this short's topic, in the empty lower half while the first line plays
    t1 = stone_title("HOW TREES", width=6.8).move_to([0, -2.3, 0])
    t2 = stone_title("REALLY WORK", width=7.6).move_to([0, -3.5, 0])
    spl = splash("Minecraft edition!", 24).move_to([2.35, -4.35, 0])
    label = chat(tag, color, 56).move_to([-1.2, -5.15, 0])
    return VGroup(t1, t2, label, spl)


def wood_sign(lines, w=6.6, h=2.7, size=72):
    # A standing oak sign: tiled planks, a dark rim, black game-font text (no shadow, as in the game) and a log post
    n, m = 6, 3
    tile_w, tile_h = w / n, h / m
    board = VGroup(*[pixel_art("planks", tile_w, tile_h).move_to([(i + 0.5) * tile_w - w / 2, (j + 0.5) * tile_h - h / 2, 0])
                     for i in range(n) for j in range(m)])
    rim = Rectangle(width=w, height=h, stroke_color="#3B2410", stroke_width=6, fill_opacity=0)
    txt = VGroup(*[MT(s, size, "#000000", TERM, shadow=False) for s in lines]).arrange(DOWN, buff=0.22)
    fit(txt, w - 0.7).move_to(board)
    post = pixel_art("log_side", 0.5, 2.0).next_to(board, DOWN, buff=0)
    return VGroup(post, board, rim, txt)


class Scene1_Walk(Overlay):
    def construct(self):
        h, lead = walk_header()
        rule = entry("LEFT FIRST", "as deep as you can", MC_AQUA).move_to([0, ROW_Y[0], 0])
        back = entry("DEAD END", "back up the lead", MC_RED).move_to([0, ROW_Y[1], 0])
        chips = moment_chips()
        ln = pre_line()

        cover = intro_cover("Depth first", MC_AQUA)
        self.add(cover)

        self.seg(20)
        self.sfx("levelup", 0.22)
        self.beat(pulse(cover[3], 1.12), rt=0.6)
        self.until(at(20, "At eight") - 0.4)
        self.beat(FadeOut(cover), FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(at(20, "splits"))
        self.sfx("click", 0.3)
        self.close_seg()

        self.seg(21)
        self.until(at(21, "lead") - 0.2)
        self.sfx("lead_tie", 0.45)
        self.beat(FadeIn(lead, scale=1.5), rt=0.35)
        self.until(at(21, "always go left") - 0.1)
        self.beat(FadeIn(rule, shift=UP * 0.2), rt=0.35)
        self.close_seg()

        self.seg(22)
        for w in words_at(22, ["Eight", "three", "one"]):
            self.sfx("click", 0.28, delay=w)
        self.until(at(22, "only barriers"))
        self.beat(FadeIn(back, shift=UP * 0.2), rt=0.35)
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
            self.beat(FadeIn(chips[k], shift=UP * 0.2), rt=0.3)
        self.close_seg()

        self.seg(25)
        self.until(at(25, "preorder") - 0.3)
        self.beat(FadeIn(ln.box), FadeIn(ln.label), pulse(chips[0], 1.15), rt=0.35)
        names = [NAMES[v] if k else NAMES[v].capitalize() for k, v in enumerate(PRE)]
        for k, w in enumerate(words_at(25, names, "preorder")):
            self.until(w - 0.05)
            self.sfx("pop", 0.22)
            self.beat(FadeIn(ln.upto(k), shift=DOWN * 0.1), rt=0.12)
        self.close_seg()


class Scene2_Full(Overlay):
    def construct(self):
        # Starts on the last frame of Scene1_Walk; the 3D page darkens the whole picture at the same time
        h, lead = walk_header()
        ln = pre_line()
        state = VGroup(h, lead, moment_chips(), ln)
        self.add(state)
        sign = wood_sign(["FULL VIDEO", "ON YOUTUBE"]).move_to([0, 0.9, 0])
        title = chat("How Trees Really Work", MC_GOLD, 56).next_to(sign, DOWN, buff=0.45)

        self.seg(CARD)  # silent line with empty text: only its time budget
        self.beat(FadeOut(state), rt=0.6)
        self.sfx("wood_dig1", 0.4)
        self.beat(FadeIn(sign, shift=DOWN * 0.4), rt=0.35)
        self.sfx("wood_dig3", 0.3, delay=0.1)
        self.until(1.2)
        self.sfx("toast_in", 0.3)
        self.beat(FadeIn(title, shift=UP * 0.2), rt=0.35)
        self.until(2.2)
        self.beat(pulse(sign, 1.05), rt=0.5)
        self.close_seg()
