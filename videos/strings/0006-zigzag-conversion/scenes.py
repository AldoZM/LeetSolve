WALK = json.load(open('walk.json', encoding='utf-8'))
S, R = WALK["s"], WALK["rows"]
LETTERS = WALK["letters"]
ROWS = WALK["row_strings"]
ROW_ORE = ["gold_ore", "diamond_ore", "emerald_ore"]
ROW_COL = [MC_GOLD, MC_AQUA, MC_GREEN]

CODE = """def convert(s, numRows):
    if numRows == 1: return s
    rows = [""] * numRows
    r, step = 0, 1
    for ch in s:
        rows[r] += ch
        if r == 0: step = 1
        elif r == numRows - 1: step = -1
        r += step
    return "".join(rows)"""


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


def string_row(y, size=0.55, gap=0.05):
    # The input string: plain stone blocks with a letter each
    row = VGroup(*[Block(ch, "stone", size) for ch in S]).arrange(RIGHT, buff=gap)
    row.move_to([0, y, 0])
    return row


def zig(y0, size=0.75, step=0.95, dy=0.95, x0=None):
    # The zigzag: letter k at its column and row, in its row's ore
    x0 = -3 * step if x0 is None else x0
    return VGroup(*[Block(e["ch"], ROW_ORE[e["row"]], size).move_to([x0 + e["col"] * step, y0 - e["row"] * dy, 0]) for e in LETTERS])


def row_chat(q, text, size=42):
    return chat(f"row {q}: {text}", ROW_COL[q], size)


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("ZIGZAG", width=5.0).move_to([0, 4.85, 0])
    t2 = stone_title("CONVERSION", width=7.2).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    z = zig(1.6, size=0.75, step=0.95, dy=0.95)
    path = VMobject(stroke_color=MC_YELLOW, stroke_width=5, stroke_opacity=0.8).set_points_as_corners([b.get_center() for b in z])
    tags = VGroup(chat("LeetCode #6", MC_AQUA, 46), chat("Medium", MC_GOLD, 46), chat("Strings", MC_GREEN, 46))
    tags.arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    # The path goes behind the blocks
    return VGroup(ground, t1, t2, spl, path, z, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, path, z, tags = art
        self.add(art)

        self.seg(0)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.7)
        # The blocks hop in zigzag order, the path flashes along them
        self.sfx("stone_dig1", 0.35, delay=0.3)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.3) for b in z], lag_ratio=0.12),
                  ShowPassingFlash(path.copy().set_stroke(MC_WHITE, 10), time_width=0.4), rt=1.8)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.7)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        row = string_row(3.4)
        nr = MT("numRows = 3", 40, MC_WHITE).move_to([0, 2.55, 0])

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(0, len(row), 2):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.26, delay=k * 0.07 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.07), rt=1.6)
        self.until(at(1, "number of rows") - 0.2)
        self.beat(FadeIn(nr, shift=UP * 0.1), rt=0.4)
        self.close_seg()

        z = zig(1.2)
        path = VMobject(stroke_color=MC_YELLOW, stroke_width=5, stroke_opacity=0.8).set_points_as_corners([b.get_center() for b in z])
        flies = [b.copy() for b in row]

        self.seg(2)
        self.until(at(2, "the blocks go") - 0.4)
        # Each stone block flies to its zigzag spot and becomes its row's ore
        for k in range(0, len(S), 2):
            self.sfx(f"stone_step{k % 6 + 1}", 0.25, delay=0.16 * k)
        self.beat(LaggedStart(*[Transform(f, z[k]) for k, f in enumerate(flies)], lag_ratio=0.16), rt=3.0)
        self.add(path, *flies)
        self.beat(Create(path), rt=0.8)
        self.close_seg()

        reads = VGroup(*[row_chat(q, " ".join(ROWS[q]), 46) for q in range(R)]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        reads.move_to([0, -2.6, 0])

        self.seg(3)
        for q, (phrase, lead) in enumerate([("P A H N", 0.2), ("A P L S", 0.3), ("Y I R", 0.9)]):
            self.until(at(3, phrase) - lead)
            self.sfx("click", 0.3)
            self.beat(FadeIn(reads[q], shift=RIGHT * 0.2), *[pulse(f, 1.15) for f, e in zip(flies, LETTERS) if e["row"] == q], rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene3_Grid(Base):
    def construct(self):
        h = hdr("FULL GRID?", MC_RED)
        step, dy, size = 0.95, 0.95, 0.75
        cells = VGroup(*[Rectangle(width=0.85, height=0.85, fill_color="#8B8B8B", fill_opacity=0.85, stroke_color="#373737",
                                   stroke_width=4).move_to([-3 * step + c * step, 2.6 - r * dy, 0]) for r in range(R) for c in range(7)])
        z = zig(2.6)
        used = {(e["row"], e["col"]) for e in LETTERS}
        empty = VGroup(*[cells[r * 7 + c] for r in range(R) for c in range(7) if (r, c) not in used])
        crosses = VGroup(*[MT("x", 44, MC_RED, PIXEL).move_to(c) for c in empty])
        cnt = MT("7 of 21 cells empty", 44, MC_RED).move_to([0, -1.2, 0])

        self.seg(4)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(c, scale=0.7) for c in cells], lag_ratio=0.02), rt=0.8)
        self.until(at(4, "place each") - 0.2)
        for k in range(0, len(S), 3):
            self.sfx("pop", 0.25, delay=0.1 * k)
        self.beat(LaggedStart(*[FadeIn(b, scale=1.4) for b in z], lag_ratio=0.1), rt=1.6)
        self.close_seg()

        self.seg(5)
        self.until(at(5, "a third") - 0.1)
        self.sfx("villager_no1", 0.4)
        self.beat(*[c.animate.set_fill("#7A2A2A") for c in empty], FadeIn(crosses), rt=0.6)
        self.beat(FadeIn(cnt, shift=UP * 0.15), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        z = zig(3.4)
        packed = VGroup()
        for q in range(R):
            members = [k for k, e in enumerate(LETTERS) if e["row"] == q]
            for j, k in enumerate(members):
                packed.add(z[k].copy().move_to([-3 * 0.95 + j * 0.95, 3.4 - q * 0.95, 0]))
        labs = VGroup(*[MT(f"row {q}", 34, ROW_COL[q]).next_to(packed[0], LEFT, buff=0.3).set_y(3.4 - q * 0.95) for q in range(R)])

        self.seg(6)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(z), rt=0.5)
        self.until(at(6, "Columns") - 0.1)
        self.sfx("stone_step2", 0.35)
        order = [k for q in range(R) for k, e in enumerate(LETTERS) if e["row"] == q]
        self.beat(*[z[k].animate.move_to(packed[n]) for n, k in enumerate(order)], rt=0.9)
        self.until(at(6, "Only the row") - 0.1)
        self.beat(FadeIn(labs, shift=RIGHT * 0.2), rt=0.4)
        self.close_seg()

        strs = VGroup(*[row_chat(q, '""', 46) for q in range(R)]).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([0.4, -0.6, 0])
        arrow = MT("v", 64, MC_YELLOW, PIXEL).next_to(strs[0], LEFT, buff=0.4)
        up = MT("^", 64, MC_YELLOW, PIXEL)
        bounce = [0, 1, 2, 1, 0]

        self.seg(7)
        self.beat(FadeOut(z), FadeOut(labs), rt=0.3)
        self.beat(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in strs], lag_ratio=0.2), rt=0.6)
        self.until(at(7, "pointer") - 0.2)
        self.beat(FadeIn(arrow), rt=0.3)
        # The pointer bounces: down to the bottom, then back up to the top
        for n in range(1, len(bounce)):
            target = strs[bounce[n]]
            going_up = bounce[n] < bounce[n - 1]
            self.sfx("click", 0.25)
            if going_up and bounce[n - 1] == R - 1:
                up.move_to(arrow)
                self.beat(Transform(arrow, up), rt=0.15)
            self.beat(arrow.animate.set_y(target.get_y()), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("ZIGZAG", MC_GREEN)
        code = code_panel(CODE, -4.35, max_h=3.0)
        bar = line_bar(code, 2, 2, MC_YELLOW)
        built = ["", "", ""]
        st = {"badge": None, "rows": [None] * R}
        Y = [-0.35, -1.05, -1.75]

        def badge(step):
            return chat(f"step {'+1 v' if step > 0 else '-1 ^'}", MC_YELLOW, 42).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)

        def row_line(q):
            return row_chat(q, " ".join(built[q]) or '""', 42).move_to([0, Y[q], 0]).to_edge(LEFT, buff=0.4)

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("row_in", "rows_in", "pointer", "holds", "toast", "join", "read")]
        for e in LETTERS:
            ev.append((seg_time(W["first"], e["t"]), "place", e["k"]))
            if "turn" in e:
                ev.append((seg_time(W["first"], e["turn"]), "turn", e["k"]))
        ev.sort(key=lambda x: x[0])

        def move_bar(k0, k1=None, color=MC_YELLOW, rt=0.12):
            self.beat(Transform(bar, line_bar(code, k0, k1, color)), rt=rt)

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.35)

        def on(kind, k):
            if kind == "row_in":
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.5)
            elif kind == "rows_in":
                self.sfx("wood_dig1", 0.35)
                for q in range(R):
                    st["rows"][q] = row_line(q)
                self.beat(FadeIn(bar),
                          LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in st["rows"]], lag_ratio=0.2), rt=0.6)
            elif kind == "pointer":
                st["badge"] = badge(1)
                move_bar(3, rt=0.15)
                self.beat(FadeIn(st["badge"], shift=LEFT * 0.2), rt=0.3)
            elif kind == "place":
                e = LETTERS[k]
                q = e["row"]
                built[q] += e["ch"]
                self.sfx(f"stone_dig{k % 4 + 1}", 0.32, delay=0.2)
                self.beat(Transform(bar, line_bar(code, 5, 5, ROW_COL[q])), Transform(st["rows"][q], row_line(q)), rt=0.15)
            elif kind == "turn":
                e = LETTERS[k]
                self.sfx("click", 0.3)
                self.beat(Transform(bar, line_bar(code, 6 if e["row"] == 0 else 7, None, MC_GOLD)),
                          Transform(st["badge"], badge(1 if e["row"] == 0 else -1)), rt=0.12)
            elif kind == "holds":
                self.beat(*[pulse(r, 1.06) for r in st["rows"]], rt=0.5)
            elif kind == "toast":
                t = toast("Advancement Made!", "Zigzag read", w=4.6)
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(st["badge"]), rt=0.5)
            elif kind == "join":
                ans = chat("".join(ROWS), MC_GREEN, 56).move_to([0, -1.05, 0])
                self.sfx("book_put", 0.35)
                move_bar(9, None, MC_GREEN, rt=0.15)
                self.beat(*[Transform(r, ans.copy()) for r in st["rows"]], rt=0.6)
            elif kind == "read":
                self.beat(pulse(st["rows"][0], 1.08), rt=0.5)

        def on_last():
            # The rows leave the 3D clip when the walk ends; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        row = string_row(3.5)
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, 2.0, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 1.0, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(14)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(row), rt=0.5)
        self.until(at(14, "placed") - 0.3)
        # Each letter is touched exactly once
        self.sfx("click", 0.25)
        self.beat(LaggedStart(*[pulse(b, 1.2) for b in row], lag_ratio=0.12), rt=1.3)
        self.until(at(14, "linear") - 0.5)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.35)
        self.add(xp)
        for d in (0.0, 0.25):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=0.5)
        self.beat(Restore(xp), rt=0.6)
        self.close_seg()

        rows = VGroup(*[row_chat(q, " ".join(ROWS[q]), 42) for q in range(R)]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        rows.move_to([0, -0.9, 0])
        sp = VGroup(MT("space", 56, MC_GRAY), level_text("O(n)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, -3.2, 0])

        self.seg(15)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.2), rt=0.7)
        self.until(at(15, "space") - 0.2)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.6, width=8.4)
        bar = line_bar(code, 2, 2, MC_YELLOW)

        self.seg(16)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(at(16, "bouncing") - 0.2)
        self.beat(Transform(bar, line_bar(code, 6, 8, MC_GOLD)), rt=0.35)
        self.close_seg()

        self.seg(17)
        msg = chat("Down, up, row by row", MC_GOLD, 58)
        msg.move_to([0, -2.3, 0])
        self.beat(FadeIn(msg, shift=UP * 0.2), Transform(bar, line_bar(code, 0, 9, MC_GREEN)), rt=0.4)
        self.until(1.2)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.45)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.9)
        self.close_seg()
