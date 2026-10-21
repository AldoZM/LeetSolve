WALK = json.load(open('walk.json', encoding='utf-8'))
WORDS, TEX = WALK["words"], WALK["tex"]

BRUTE_CODE = """def longestCommonPrefix(strs):
    first = strs[0]
    for k in range(len(first), 0, -1):
        if all(w.startswith(first[:k]) for w in strs):
            return first[:k]
    return \"\""""

CODE = """def longestCommonPrefix(strs):
    first = strs[0]
    for i, ch in enumerate(first):
        for word in strs[1:]:
            if i == len(word) or word[i] != ch:
                return first[:i]
    return first"""


def word_rows(y0, size, gap=0.08, row_gap=0.12):
    # The words stacked, left-aligned, each built from the block it names; rows[w][c] is letter c of word w
    rows = VGroup()
    for w, (word, tex) in enumerate(zip(WORDS, TEX)):
        row = VGroup(*[Block(ch, tex, size) for ch in word]).arrange(RIGHT, buff=gap)
        if tex == "diorite":
            # White letters disappear on the light stone: dark gray, without the shadow
            for ch, b in zip(word, row):
                num = MT(ch, 40, "#3F3F3F", PIXEL, shadow=False)
                num.scale_to_fit_height(b.num.height).move_to(b.num)
                b.remove(b.num)
                b.num = num
                b.add(num)
        rows.add(row)
    rows.arrange(DOWN, buff=row_gap, aligned_edge=LEFT)
    rows.move_to([0, y0, 0])
    return rows


def column(rows, c):
    return VGroup(*[r[c] for r in rows if c < len(r)])


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def pulse(m, k=1.15):
    # Emphasis that keeps the pixel art's colors (Indicate would paint it one flat color)
    return m.animate(rate_func=there_and_back).scale(k)


def col_box(rows, c0, c1, color, width=8, buff=0.08):
    # Rectangle around columns c0..c1 of every row (built from the blocks' edges, so it never takes text into account)
    first = rows[0]
    top = first[0].get_top()[1]
    low = first
    for r in rows:
        if c0 < len(r):
            low = r
    bottom = low[0].get_bottom()[1]
    left, right = first[c0].get_left()[0], first[min(c1, len(first) - 1)].get_right()[0]
    box = Rectangle(width=right - left + 2 * buff, height=top - bottom + 2 * buff, stroke_color=color, stroke_width=width,
                    fill_opacity=0)
    box.move_to([(left + right) / 2, (top + bottom) / 2, 0])
    return box


def reads(k):
    # Letters compared when checking first[:k] against every word with startswith (stops at the first mismatch)
    n = 0
    for w in WORDS:
        if len(w) < k:
            continue
        m = 0
        while m < k and w[m] == WORDS[0][m]:
            m += 1
        n += min(k, m + 1)
    return n


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("LONGEST COMMON", width=8.0).move_to([0, 4.85, 0])
    t2 = stone_title("PREFIX", width=4.6).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    rows = word_rows(0.95, 0.7)
    box = col_box(rows, 0, 1, MC_GOLD, 10)
    tags = VGroup(chat("LeetCode #14", MC_AQUA, 46), chat("Easy", MC_GREEN, 46), chat("Strings", MC_GOLD, 46))
    tags.arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, rows, box, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, rows, box, tags = art
        self.add(art)

        self.seg(0)
        self.beat(pulse(spl), rt=0.8)
        self.sfx("stone_dig1", 0.35, delay=0.35)
        self.beat(LaggedStart(*[r.animate(rate_func=there_and_back).shift(RIGHT * 0.3) for r in rows], lag_ratio=0.25), rt=1.4)
        self.sfx("orb", 0.3, delay=0.2)
        self.beat(ShowPassingFlash(box.copy().set_stroke(MC_YELLOW), time_width=0.6), pulse(column(rows, 0)), pulse(column(rows, 1)),
                  rt=0.9)
        self.beat(pulse(spl), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        rows = word_rows(1.6, 0.85)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(1.6)
        for k, r in enumerate(rows):
            self.sfx(f"stone_dig{k + 1}", 0.3)
            self.beat(LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in r], lag_ratio=0.08), rt=0.6)
        self.close_seg()

        self.seg(2)
        box = col_box(rows, 0, 1, MC_GOLD, 9)
        ans = chat('"di"', MC_GREEN, 64).move_to([0, -1.5, 0])
        self.until(min(1.2, DUR[2] - 2.6))
        self.beat(Create(box), rt=0.5)
        self.until(DUR[2] - 1.4)
        self.sfx("pop", 0.35)
        self.beat(FadeIn(ans, shift=UP * 0.2), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("EVERY PREFIX", MC_RED)
        rows = word_rows(2.7, 0.6)
        code = code_panel(BRUTE_CODE, -3.7, max_h=2.9)
        first = WORDS[0]

        def cand(k, color=MC_WHITE):
            return chat(f'"{first[:k]}"?', color, 50).move_to([0, 0.55, 0])

        def counter(n):
            return MT(f"letters read {n}", 34, MC_WHITE, PIXEL).move_to([0, -0.6, 0])

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(r, shift=DOWN * 0.2) for r in rows], lag_ratio=0.2), rt=0.8)
        self.until(1.4)
        self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
        self.close_seg()

        bar = line_bar(code, 2, 2, MC_YELLOW)
        box = col_box(rows, 0, 6, MC_YELLOW, 7)
        c = cand(7)
        total = 0
        cnt = counter(0)
        self.seg(4)
        self.beat(FadeIn(bar), Create(box), FadeIn(c), FadeIn(cnt), rt=0.35)
        ks = [7, 6, 5, 4, 3, 2]
        step = (DUR[4] - 0.6) / len(ks)
        for j, k in enumerate(ks):
            total += reads(k)
            ok = k == 2
            col = MC_GREEN if ok else MC_RED
            self.sfx("orb" if ok else f"stone_dig{j % 4 + 1}", 0.3 if ok else 0.22)
            anims = [Transform(c, cand(k, col)), Transform(box, col_box(rows, 0, k - 1, col, 7)), Transform(cnt, counter(total)),
                     Transform(bar, line_bar(code, 3, 3, col))]
            self.beat(*anims, rt=min(0.4, step * 0.6))
            self.hold(max(0.05, step - min(0.4, step * 0.6)))
        self.close_seg()

        self.seg(5)
        self.until(0.3)
        flashes = [ShowPassingFlash(col_box(rows, 0, 1, MC_GOLD, 10), time_width=0.6) for _ in range(1)]
        self.sfx("stone_step2", 0.3)
        self.beat(*flashes, pulse(column(rows, 0)), pulse(column(rows, 1)), rt=0.7)
        self.until(DUR[5] - 1.0)
        self.beat(pulse(cnt, 1.2), rt=0.5)
        self.close_seg()

        self.seg(6)
        again = MT("d and i read 6 times", 40, MC_RED).move_to([0, -1.5, 0])
        self.until(0.4)
        self.sfx("villager_no2", 0.35)
        self.beat(FadeIn(again, shift=UP * 0.15), Transform(cnt, counter(total).set_color(MC_RED)), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        rows = word_rows(2.3, 0.85)
        lab = MT("read down the columns", 46, MC_GOLD).move_to([0, -0.4, 0])
        scan = col_box(rows, 0, 0, MC_YELLOW, 9)

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(1.4)
        self.sfx("stone_dig1", 0.3)
        self.beat(LaggedStart(*[FadeIn(r, shift=UP * 0.4) for r in rows], lag_ratio=0.25), rt=0.8)
        self.until(min(3.0, DUR[7] - 1.8))
        self.beat(Create(scan), FadeIn(lab, shift=UP * 0.1), rt=0.5)
        self.close_seg()

        self.seg(8)
        stop = MT("first mismatch = end of prefix", 40, MC_RED).move_to([0, -1.5, 0])
        out = MT("or a word runs out", 40, MC_GRAY).next_to(stop, DOWN, buff=0.25)
        for c in (1, 2):
            col = MC_YELLOW if c < 2 else MC_RED
            self.sfx("click", 0.3)
            self.beat(Transform(scan, col_box(rows, c, c, col, 9)), rt=0.35)
            self.hold(0.3)
        self.sfx("villager_no1", 0.3)
        self.beat(FadeIn(stop, shift=UP * 0.15), rt=0.5)
        self.until(min(3.4, DUR[8] - 1.0))
        self.beat(FadeIn(out, shift=UP * 0.1), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("VERTICAL SCAN", MC_GREEN)
        code = code_panel(CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 2, 2, MC_YELLOW)

        def colchip(c):
            return chat(f"column {c}", MC_WHITE, 40).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)

        def pref(s, color=MC_WHITE):
            return chat(f'prefix "{s}"', color, 56).move_to([0, -1.1, 0])

        st = {"chip": colchip(0), "pref": pref("")}

        ev = [(seg_time(W["first"], W[key]), key, None)
              for key in ("intro_rows", "scan", "grows", "stop", "unread", "ret", "toast", "answer")]
        for k, c in enumerate(W["cols"]):
            ev.append((seg_time(W["first"], c["show"]), "show", k))
            ev.append((seg_time(W["first"], c["reads"][0]), "read", k))
            ev.append((seg_time(W["first"], c["verdict"]), "verdict", k))
        ev.sort(key=lambda e: e[0])

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.35)

        def on(kind, k):
            if kind == "intro_rows":
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
            elif kind == "scan":
                self.beat(FadeIn(bar), FadeIn(st["chip"]), FadeIn(st["pref"], shift=UP * 0.1), rt=0.35)
            elif kind == "show":
                self.beat(Transform(st["chip"], colchip(k)), Transform(bar, line_bar(code, 2, 2, MC_YELLOW)), rt=0.15)
            elif kind == "read":
                self.beat(Transform(bar, line_bar(code, 4, 4, MC_YELLOW)), rt=0.12)
            elif kind == "verdict":
                c = W["cols"][k]
                if c["match"]:
                    for d in (0.0, 0.15):
                        self.sfx("orb", 0.26, delay=d)
                    self.beat(Transform(bar, line_bar(code, 3, 3, MC_GREEN)),
                              Transform(st["pref"], pref(W["prefix"][:k + 1], MC_GREEN)), rt=0.25)
                else:
                    self.sfx("villager_no3", 0.35)
                    self.beat(Transform(bar, line_bar(code, 4, 4, MC_RED)), rt=0.25)
            elif kind == "grows":
                self.beat(pulse(st["pref"], 1.12), rt=0.4)
            elif kind == "stop":
                self.beat(Transform(bar, line_bar(code, 5, 5, MC_GOLD)), rt=0.3)
            elif kind == "unread":
                self.beat(Transform(st["pref"], pref(W["prefix"], MC_GOLD)), rt=0.3)
            elif kind == "ret":
                self.sfx("pop", 0.35)
                self.beat(pulse(st["pref"], 1.15), rt=0.5)
            elif kind == "toast":
                t = toast("Advancement Made!", "Common prefix found", w=4.6)
                t.move_to([0, 5.5, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(st["chip"]), rt=0.5)
            elif kind == "answer":
                # The answer takes the prefix's place: the 3D blocks use the top of the frame
                ans = chat('return "di"', MC_GREEN, 60).move_to(st["pref"])
                self.beat(FadeTransform(st["pref"], ans), rt=0.4)

        def on_last():
            # The 3D clip fades to sky at its end; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        cmp = VGroup(VGroup(MT("every prefix", 40, MC_GRAY), MT("52 letters", 44, MC_RED, PIXEL)).arrange(DOWN, buff=0.2),
                     VGroup(MT("column scan", 40, MC_GRAY), MT("8 letters", 44, MC_GREEN, PIXEL)).arrange(DOWN, buff=0.2))
        cmp.arrange(RIGHT, buff=1.0).move_to([0, 3.3, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(S)", 1.05)).arrange(RIGHT, buff=0.4)
        tm.move_to([0, 1.5, 0])
        note = MT("S = all the letters", 40, MC_WHITE).move_to([0, 0.6, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, -0.15, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in cmp], lag_ratio=0.3), rt=0.8)
        self.until(min(2.4, DUR[16] - 1.8))
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(note), FadeIn(bg), rt=0.4)
        self.add(xp)
        for d in (0.0, 0.3, 0.6, 0.9):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=1.2)
        self.beat(Restore(xp), rt=1.2)
        self.close_seg()

        self.seg(17)
        mem = VGroup(MT("memory", 56, MC_GRAY), MT("O(1)", 52, MC_GOLD, PIXEL)).arrange(RIGHT, buff=0.4)
        mem.move_to([0, -1.8, 0])
        one = MT("one index", 44, MC_WHITE).next_to(mem, DOWN, buff=0.35)
        self.until(0.3)
        self.beat(FadeIn(mem, shift=UP * 0.15), rt=0.5)
        self.until(min(2.0, DUR[17] - 1.0))
        self.beat(FadeIn(one, shift=UP * 0.1), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.6, width=8.4)
        bar = line_bar(code, 2, 3, MC_YELLOW)

        self.seg(18)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(min(1.6, DUR[18] - 1.2))
        self.beat(Transform(bar, line_bar(code, 4, 4, MC_AQUA)), rt=0.3)
        self.until(DUR[18] - 0.7)
        self.beat(Transform(bar, line_bar(code, 5, 5, MC_GOLD)), rt=0.3)
        self.close_seg()

        self.seg(19)
        msg = VGroup(chat("Read in columns,", MC_GOLD, 54), chat("stop at the first mismatch", MC_WHITE, 48)).arrange(DOWN, buff=0.2)
        msg.move_to([0, -2.6, 0])
        self.until(0.1)
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.5)
        self.until(DUR[19] - 1.9)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.5)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=1.0)
        self.close_seg()
