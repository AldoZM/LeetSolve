WALK = json.load(open('walk.json', encoding='utf-8'))
S = WALK["s"]
STEPS = WALK["steps"]
LETTERS = WALK["letters"]
ORE_OF.update(WALK["ore_of"])

BRUTE_CODE = """def lengthOfLongestSubstring(s):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            if len(set(s[i:j + 1])) == j - i + 1:
                best = max(best, j - i + 1)
    return best"""

CODE = """def lengthOfLongestSubstring(s):
    last = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
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


def index_row(row, size=34, color=MC_GRAY, buff=0.14):
    return VGroup(*[MT(str(k), size, color).next_to(b, DOWN, buff=buff) for k, b in enumerate(row)])


def pulse(m, k=1.15):
    # Emphasis that keeps the pixel art's colors (Indicate would paint it one flat color)
    return m.animate(rate_func=there_and_back).scale(k)


def window_box(row, i, j, color=MC_GOLD, width=8):
    # Outline around blocks i..j of a row
    a, b = row[i], row[j]
    w = b.get_right()[0] - a.get_left()[0] + 0.22
    h = a.height + 0.22
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=width, fill_opacity=0).move_to(
        [(a.get_left()[0] + b.get_right()[0]) / 2, a.get_y(), 0])


def letter_item(inv, k, ch, index):
    # Ore block of a letter in slot k: the letter where the game prints stack counts, the stored index in yellow
    u = inv.u
    icon = iso_block(f"{ORE_OF[ch]}_ore", 16 * u)
    let = gui_text(ch, MC_WHITE, u * 1.15)
    let.move_to(icon.get_corner(DR) + np.array([1 * u, 0.5 * u, 0]), aligned_edge=DR)
    num = gui_text(str(index), MC_YELLOW, u * 1.0)
    num.move_to(icon.get_corner(UL) + np.array([-1 * u, 0.5 * u, 0]), aligned_edge=UL)
    return VGroup(icon, let, num).move_to(inv.slots[k])


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("LONGEST", width=5.6).move_to([0, 4.85, 0])
    t2 = stone_title("SUBSTRING", width=7.0).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    row = block_row(list(S), 1.0, size=0.95, gap=0.15)
    idx = index_row(row, 30)
    win = window_box(row, 2, 6)
    sub = MT("no repeats inside", 40, MC_GOLD).move_to([1.6, -0.75, 0])
    tags = VGroup(chat("LeetCode #3", MC_AQUA, 42), chat("Medium", MC_GOLD, 42), chat("Sliding Window", MC_GREEN, 42))
    tags.arrange(RIGHT, buff=0.2).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, row, idx, win, sub, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, row, idx, win, sub, tags = art
        self.add(art)

        self.seg(0)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        # Blocks hop one after another, like a wave
        self.sfx("stone_dig1", 0.35, delay=0.35)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.35) for b in row], lag_ratio=0.15), rt=1.6)
        self.sfx("orb", 0.3, delay=0.2)
        self.beat(ShowPassingFlash(win.copy().set_stroke(MC_YELLOW, 14), time_width=0.6),
                  *[pulse(row[k], 1.12) for k in range(2, 7)], rt=1.0)
        self.until(4.6)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        row = block_row(list(S), 2.6, size=1.0, gap=0.15)
        idx = index_row(row)
        lab = MT("s", 40, MC_WHITE).next_to(row, UP, buff=0.2).align_to(row, LEFT)
        pairs = VGroup(*[outline(row[k], c, 8) for k, c in ((0, MC_YELLOW), (6, MC_YELLOW), (1, MC_AQUA), (3, MC_AQUA))])

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        # Blocks fall from the sky and bounce into place
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(len(row)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.3, delay=k * 0.12 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.12), rt=1.7)
        self.beat(FadeIn(idx, shift=UP * 0.1), FadeIn(lab), rt=0.4)
        self.until(at(1, "same letter"))
        self.sfx("click", 0.3)
        self.beat(Create(pairs), *[pulse(row[k]) for k in (0, 6, 1, 3)], rt=0.6)
        self.close_seg()

        goal = MT("longest run, no ore repeated", 40, MC_WHITE).move_to([0, 0.6, 0])

        self.seg(2)
        self.beat(FadeOut(pairs), rt=0.3)
        self.beat(FadeIn(goal, shift=UP * 0.15), rt=0.4)
        self.close_seg()

        win = window_box(row, 2, 6)
        ans = VGroup(MT("length", 44, MC_GRAY), MT("5", 60, MC_GOLD, PIXEL)).arrange(RIGHT, buff=0.35).move_to([0, -0.8, 0])
        run = chat("c b d e a", MC_GREEN, 60).move_to([0, -2.4, 0])

        self.seg(3)
        self.until(at(3, "the answer"))
        self.sfx("pop", 0.4)
        self.beat(Create(win), FadeIn(ans, shift=UP * 0.15), rt=0.6)
        self.until(at(3, "The run"))
        self.beat(FadeIn(run, shift=UP * 0.2), rt=0.4)
        self.until(at(3, "no repeats") - 0.6)
        self.sfx("orb", 0.3)
        self.beat(*[pulse(row[k]) for k in range(2, 7)], rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("BRUTE FORCE", MC_RED)
        row = block_row(list(S), 3.0, size=0.95, gap=0.15)
        idx = index_row(row, 30)
        code = code_panel(BRUTE_CODE, -3.7, max_h=2.9)
        pick = pickaxe(1.05).move_to([-2.4, 1.0, 0])
        dbg = Rectangle(width=1.2, height=0.16, fill_color="#000000", fill_opacity=1, stroke_width=0)
        dbg.next_to(pick, DOWN, buff=0.15)
        runs = [(i, j) for i in range(len(S)) for j in range(i, len(S))]

        def dfill(frac):
            # Durability bar: shrinks and turns from green to red
            r = Rectangle(width=max(1.16 * frac, 0.02), height=0.1, stroke_width=0, fill_opacity=1,
                          fill_color=interpolate_color(ManimColor(MC_RED), ManimColor(MC_GREEN), frac))
            r.move_to(dbg.get_left() + RIGHT * (0.02 + max(1.16 * frac, 0.02) / 2))
            return r

        def counter(k):
            return MT(f"runs {k}", 30, MC_WHITE, PIXEL).move_to([1.0, 1.0, 0])

        fill, cnt = dfill(1.0), counter(0)
        box = window_box(row, 0, 0, MC_WHITE, 6)
        bar = line_bar(code, 3, 4, MC_YELLOW)

        def check(k, rt):
            i, j = runs[k]
            ok = len(set(S[i:j + 1])) == j - i + 1
            self.sfx(f"stone_dig{k % 4 + 1}", 0.2, delay=rt * 0.5)
            self.beat(Transform(box, window_box(row, i, j, MC_GREEN if ok else MC_RED, 6)), Transform(fill, dfill(1 - (k + 1) / 29)),
                      Transform(cnt, counter(k + 1)), Rotate(pick, angle=-25 * DEGREES, rate_func=there_and_back), rt=rt)

        self.seg(4)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in row], lag_ratio=0.1), rt=0.8)
        self.beat(FadeIn(idx), FadeIn(code, shift=UP * 0.3), rt=0.5)
        self.beat(FadeIn(pick, scale=0.6), FadeIn(dbg), FadeIn(fill), FadeIn(cnt), Create(box), FadeIn(bar), rt=0.4)
        for k in range(3):
            check(k, 0.4)
        self.close_seg()

        self.seg(5)
        for k in range(3, len(runs)):
            check(k, 0.17)
        self.close_seg()

        o = big_o_pow("n", 3, 80, MC_RED)
        o.move_to([0.9, 1.0, 0])
        broken = MT("broken!", 34, MC_RED)
        broken.next_to(dbg, DOWN, buff=0.15)

        self.seg(6)
        self.beat(FadeOut(cnt), FadeIn(o, scale=0.5), rt=0.5)
        self.until(at(6, "pickaxe") - 0.2)
        self.sfx("break", 0.45)
        self.beat(Wiggle(pick), FadeIn(broken, shift=UP * 0.1), rt=0.8)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        row = block_row(list(S), 3.2, size=0.95, gap=0.15)
        idx = index_row(row, 30)
        win = window_box(row, 0, 0)

        def edge_labels(i, j):
            l = MT("left", 42, MC_AQUA).next_to(row[i], DOWN, buff=0.6)
            r = MT("right", 42, MC_YELLOW).next_to(row[j], DOWN, buff=0.6)
            if j - i < 1:
                l.shift(LEFT * 0.4)
                r.shift(RIGHT * 0.4)
            return VGroup(l, r)

        labs = edge_labels(0, 0)

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(row), FadeIn(idx), rt=0.5)
        self.until(at(7, "slide"))
        self.beat(Create(win), FadeIn(labs), rt=0.5)
        self.until(at(7, "The right edge"))
        # The right edge only moves forward: a, b, c
        for j in (1, 2):
            self.sfx("click", 0.25)
            self.beat(Transform(win, window_box(row, 0, j)), Transform(labs, edge_labels(0, j)), rt=0.4)
        self.until(at(7, "left edge"))
        self.beat(Transform(win, window_box(row, 0, 3)), Transform(labs, edge_labels(0, 3)), rt=0.4)
        self.sfx("villager_no1", 0.35)
        reds = VGroup(outline(row[1], MC_RED, 8), outline(row[3], MC_RED, 8))
        self.beat(Create(reds), rt=0.3)
        self.until(at(7, "jumps"))
        self.sfx("stone_step2", 0.4)
        self.beat(Transform(win, window_box(row, 2, 3)), Transform(labs, edge_labels(2, 3)), FadeOut(reds), rt=0.5)
        self.close_seg()

        inv = Inventory(9, "Chest = last index")
        inv.move_to([0, -0.4, 0])
        items = VGroup(*[letter_item(inv, k, ch, k) for k, ch in enumerate("abc")])
        rule = VGroup(MT("left = last[b] + 1 =", 42, MC_WHITE), MT("2", 52, MC_GOLD, PIXEL)).arrange(RIGHT, buff=0.3)
        rule.move_to([0, -2.4, 0])
        step = MT("one step, no scanning", 38, MC_GREEN).move_to([0, -3.6, 0])

        self.seg(8)
        self.sfx("chestopen", 0.3)
        self.beat(FadeIn(inv, shift=UP * 0.3), rt=0.5)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(*[FadeIn(it, scale=1.5) for it in items], lag_ratio=0.25), rt=0.7)
        self.until(at(8, "so every") - 0.2)
        self.beat(Create(outline(inv.slots[1], MC_GOLD, 7, buff=0.02)), FadeIn(rule, shift=UP * 0.15), rt=0.5)
        self.until(at(8, "single step") - 0.3)
        self.sfx("orb", 0.3)
        self.beat(FadeIn(step, shift=UP * 0.15), rt=0.3)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("SLIDING WINDOW", MC_GREEN)
        inv = Inventory(9, "Chest = last index")
        inv.move_to([0, -1.15, 0])
        code = code_panel(CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 2, 2, MC_YELLOW)
        slot_of = {ch: k for k, ch in enumerate(LETTERS)}
        st = {"best": None, "win": None, "items": {}, "mark": None}

        def best_badge(v):
            return chat(f"best {v}", MC_GOLD if v else MC_GRAY, 42).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)

        def win_text(i, j, color=MC_WHITE):
            letters = " ".join(S[i:j + 1]) if j >= i else "-"
            return chat(f"window {letters}   len {max(j - i + 1, 0)}", color, 46).move_to([0, 4.3, 0])

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("row_in", "window_in", "chest_in", "grows3", "four", "toast",
                                                                     "five", "answer")]
        for k, s in enumerate(STEPS):
            for kind in ("visit", "check", "jump", "ignore", "store"):
                if kind in s:
                    ev.append((seg_time(W["first"], s[kind]), kind, k))
        ev.sort(key=lambda e: e[0])

        def move_bar(k0, color=MC_YELLOW, rt=0.15):
            self.beat(Transform(bar, line_bar(code, k0, k0, color)), rt=rt)

        def set_win(i, j, color=MC_WHITE, rt=0.2):
            new = win_text(i, j, color)
            self.beat(Transform(st["win"], new), rt=rt)

        def mark(k, color):
            box = outline(inv.slots[k], color, 7, buff=0.02)
            if st["mark"] is None:
                st["mark"] = box
                self.beat(Create(box), rt=0.15)
            else:
                self.beat(Transform(st["mark"], box), rt=0.15)

        def on_first():
            st["best"] = best_badge(0)
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(st["best"]), rt=0.35)

        def on(kind, k):
            s = STEPS[k] if k is not None else None
            if kind == "row_in":
                for i in range(len(S)):
                    self.sfx(f"stone_dig{i % 4 + 1}", 0.28, delay=0.12 * i + 0.35)
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
            elif kind == "window_in":
                st["win"] = win_text(0, -1, MC_GRAY)
                self.beat(FadeIn(st["win"]), FadeIn(bar), rt=0.4)
            elif kind == "chest_in":
                self.sfx("wood_dig2", 0.4)
                self.beat(FadeIn(inv, shift=UP * 0.3), rt=0.5)
            elif kind == "visit":
                self.sfx("click", 0.25)
                move_bar(3, rt=0.12)
                # A repeat inside the window shows in red until the left edge jumps
                set_win(s["left0"], s["r"], MC_RED if s["repeat"] else MC_WHITE)
            elif kind == "check":
                self.sfx("chestopen", 0.28)
                move_bar(4, MC_RED if s["repeat"] else MC_GRAY, rt=0.15)
                mark(slot_of[s["ch"]], MC_RED if s["repeat"] else MC_GRAY)
            elif kind == "jump":
                self.sfx("stone_step3", 0.4)
                move_bar(5, MC_GOLD, rt=0.15)
                set_win(s["left"], s["r"], MC_GOLD, rt=0.3)
            elif kind == "ignore":
                self.sfx("villager_no2", 0.3)
                move_bar(4, MC_GRAY, rt=0.12)
            elif kind == "store":
                slot = slot_of[s["ch"]]
                it = letter_item(inv, slot, s["ch"], s["r"])
                self.sfx("pop", 0.35)
                anims = [Transform(bar, line_bar(code, 6, 6, MC_YELLOW))]
                if s["ch"] in st["items"]:
                    anims.append(Transform(st["items"][s["ch"]], it))
                else:
                    st["items"][s["ch"]] = it
                    anims.append(FadeIn(it, scale=1.6))
                if st["mark"] is not None:
                    anims.append(FadeOut(st["mark"]))
                    st["mark"] = None
                self.beat(*anims, rt=0.18)
                prev_best = STEPS[k - 1]["best"] if k else 0
                if s["best"] > prev_best:
                    self.beat(Transform(bar, line_bar(code, 7, 7, MC_GREEN)), Transform(st["best"], best_badge(s["best"])), rt=0.15)
            elif kind in ("grows3", "four"):
                self.beat(pulse(st["win"], 1.1), rt=0.4)
            elif kind == "toast":
                t = toast("Advancement Made!", "Longest run found", w=4.8)
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(st["best"]), rt=0.5)
            elif kind == "five":
                set_win(2, 6, MC_GOLD, rt=0.3)
            elif kind == "answer":
                ans = chat("return 5", MC_GREEN, 60).move_to([0, 4.3, 0])
                self.beat(Transform(st["win"], ans), Transform(bar, line_bar(code, 8, 8, MC_GREEN)), rt=0.4)

        def on_last():
            # The row leaves the 3D clip when the walk ends; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        row = block_row(list(S), 3.5, size=0.8, gap=0.14)
        win = window_box(row, 0, 0)
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, 1.7, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.75, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(15)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(row), rt=0.5)
        self.beat(Create(win), rt=0.3)
        # Right edge goes block by block; the left edge only ever jumps forward
        for j in range(1, len(S)):
            i = 2 if j >= 3 else 0
            self.sfx("click", 0.2)
            self.beat(Transform(win, window_box(row, i, j)), rt=0.32)
        self.until(at(15, "linear") - 1.3)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.4)
        self.add(xp)
        for d in (0.0, 0.25, 0.5):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=0.75)
        self.beat(Restore(xp), rt=0.8)
        self.close_seg()

        inv = Inventory(9, "Chest = last index")
        inv.move_to([0, -1.0, 0])
        items = VGroup(*[letter_item(inv, k, ch, S.rindex(ch)) for k, ch in enumerate(LETTERS)])
        sp = VGroup(MT("space", 56, MC_GRAY), level_text("O(k)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, -2.7, 0])
        kk = MT("k = letters in the alphabet", 36, MC_WHITE).move_to([0, -3.85, 0])

        self.seg(16)
        self.beat(FadeIn(inv, shift=UP * 0.2), rt=0.4)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(*[FadeIn(it, scale=1.5) for it in items], lag_ratio=0.2), rt=0.8)
        self.until(at(16, "extra space") - 0.2)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.5)
        self.until(at(16, "bounded"))
        self.beat(FadeIn(kk, shift=UP * 0.15), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.6, width=8.4)
        bar = line_bar(code, 3, 3, MC_YELLOW)
        icon = chest_icon(0.55)

        self.seg(17)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(at(17, "one chest") - 0.1)
        icon.next_to(code.code_lines[1], RIGHT, buff=0.4)
        self.beat(Transform(bar, line_bar(code, 1, 1, MC_GOLD)), FadeIn(icon, scale=0.5), rt=0.35)
        self.until(at(17, "left edge") - 0.1)
        self.beat(Transform(bar, line_bar(code, 4, 5, MC_AQUA)), rt=0.35)
        self.close_seg()

        self.seg(18)
        msg = chat("Slide, never restart", MC_GOLD, 60)
        msg.move_to([0, -2.3, 0])
        self.beat(Transform(bar, line_bar(code, 0, 8, MC_GREEN)), FadeIn(msg, shift=UP * 0.2), rt=0.5)
        self.until(2.6)
        self.beat(FadeOut(Group(code, bar, icon, msg)), rt=0.5)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=1.0)
        self.close_seg()
