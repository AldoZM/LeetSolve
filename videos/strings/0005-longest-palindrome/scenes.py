WALK = json.load(open('walk.json', encoding='utf-8'))
S = WALK["s"]
CENTERS = WALK["centers"]
ORE_OF.update(WALK["ore_of"])
MIRROR = "#BFE8FF"

BRUTE_CODE = """def longestPalindrome(s):
    best = ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            sub = s[i:j + 1]
            if sub == sub[::-1] and len(sub) > len(best):
                best = sub
    return best"""

CODE = """def longestPalindrome(s):
    best = ""
    for c in range(2 * len(s) - 1):
        l, r = c // 2, (c + 1) // 2
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l, r = l - 1, r + 1
        if r - l - 1 > len(best):
            best = s[l + 1:r]
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


def index_row(row, size=30, color=MC_GRAY, buff=0.12):
    return VGroup(*[MT(str(k), size, color).next_to(b, DOWN, buff=buff) for k, b in enumerate(row)])


def pulse(m, k=1.15):
    # Emphasis that keeps the pixel art's colors (Indicate would paint it one flat color)
    return m.animate(rate_func=there_and_back).scale(k)


def box(row, i, j, color=MC_GOLD, width=8):
    # Outline around blocks i..j of a row
    a, b = row[i], row[j]
    return Rectangle(width=b.get_right()[0] - a.get_left()[0] + 0.2, height=a.height + 0.2, stroke_color=color, stroke_width=width,
                     fill_opacity=0).move_to([(a.get_left()[0] + b.get_right()[0]) / 2, a.get_y(), 0])


def mirror_at(row, c, h=None):
    # Pale glass line on a center: block c/2 when c is even, the gap after block c//2 when odd
    x = row[c // 2].get_x() if c % 2 == 0 else (row[c // 2].get_right()[0] + row[c // 2 + 1].get_left()[0]) / 2
    h = h or row[0].height * 1.6
    return Rectangle(width=0.09, height=h, fill_color=MIRROR, fill_opacity=0.9, stroke_width=0).move_to([x, row[0].get_y(), 0])


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    t1 = stone_title("LONGEST", width=5.6).move_to([0, 4.85, 0])
    t2 = stone_title("PALINDROME", width=7.4).move_to([0, 3.75, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.55, 2.75, 0])
    row = block_row(list(S), 1.0, size=0.75, gap=0.1)
    idx = index_row(row, 26)
    win = box(row, 3, 9)
    mir = mirror_at(row, 12)
    sub = chat("racecar", MC_GREEN, 52).move_to([1.6, -0.95, 0])
    tags = VGroup(chat("LeetCode #5", MC_AQUA, 46), chat("Medium", MC_GOLD, 46), chat("Strings", MC_GREEN, 46))
    tags.arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, t1, t2, spl, row, idx, win, mir, sub, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, t1, t2, spl, row, idx, win, mir, sub, tags = art
        self.add(art)

        self.seg(0)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.7)
        # Blocks hop in mirrored pairs, outward from the e in the middle of racecar
        self.sfx("stone_dig1", 0.35, delay=0.3)
        pairs = [[row[6]], [row[5], row[7]], [row[4], row[8]], [row[3], row[9]]]
        self.beat(LaggedStart(*[AnimationGroup(*[b.animate(rate_func=there_and_back).shift(UP * 0.35) for b in p]) for p in pairs],
                              lag_ratio=0.3), rt=1.6)
        self.sfx("orb", 0.3)
        self.beat(ShowPassingFlash(win.copy().set_stroke(MC_YELLOW, 14), time_width=0.6), pulse(mir, 1.3), rt=0.9)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.7)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        row = block_row(list(S), 2.6, size=0.75, gap=0.1)
        idx = index_row(row)
        fwd = VGroup(MT("forwards", 40, MC_GRAY), chat("r a c e c a r", MC_AQUA, 46)).arrange(RIGHT, buff=0.35).move_to([0, 0.75, 0])
        bwd = VGroup(MT("backwards", 40, MC_GRAY), chat("r a c e c a r", MC_GOLD, 46)).arrange(RIGHT, buff=0.35).move_to([0, -0.3, 0])
        bwd[1].align_to(fwd[1], LEFT)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        # Blocks fall from the sky and bounce into place
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(len(row)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.28, delay=k * 0.1 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.1), rt=1.8)
        self.beat(FadeIn(idx, shift=UP * 0.1), rt=0.3)
        self.until(at(1, "forwards"))
        self.beat(FadeIn(fwd, shift=RIGHT * 0.2), rt=0.4)
        self.until(at(1, "backwards"))
        self.beat(FadeIn(bwd, shift=LEFT * 0.2), rt=0.4)
        self.close_seg()

        win = box(row, 3, 9)
        ans = VGroup(chat("racecar", MC_GREEN, 60), MT("length 7", 44, MC_GOLD)).arrange(RIGHT, buff=0.5).move_to([0, -2.0, 0])

        self.seg(2)
        self.until(at(2, "the answer") - 0.2)
        self.sfx("pop", 0.4)
        self.beat(Create(win), *[pulse(row[k], 1.12) for k in range(3, 10)], rt=0.6)
        self.beat(FadeIn(ans, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("BRUTE FORCE", MC_RED)
        row = block_row(list(S), 3.0, size=0.75, gap=0.1)
        idx = index_row(row, 26)
        code = code_panel(BRUTE_CODE, -3.7, max_h=2.9)
        pick = pickaxe(1.05).move_to([-2.4, 1.0, 0])
        runs = [(i, j) for i in range(len(S)) for j in range(i, len(S))]
        shown = runs[::2]

        def counter(k):
            return MT(f"runs {k}", 30, MC_WHITE, PIXEL).move_to([1.0, 1.0, 0])

        cnt = counter(0)
        sel = box(row, 0, 0, MC_WHITE, 6)

        def check(n, rt):
            i, j = shown[n]
            ok = S[i:j + 1] == S[i:j + 1][::-1]
            self.sfx(f"stone_dig{n % 4 + 1}", 0.18, delay=rt * 0.5)
            self.beat(Transform(sel, box(row, i, j, MC_GREEN if ok else MC_RED, 6)), Transform(cnt, counter(runs.index((i, j)) + 1)),
                      Rotate(pick, angle=-25 * DEGREES, rate_func=there_and_back), rt=rt)

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in row], lag_ratio=0.08), rt=0.7)
        self.beat(FadeIn(idx), FadeIn(code, shift=UP * 0.3), rt=0.5)
        self.beat(FadeIn(pick, scale=0.6), FadeIn(cnt), Create(sel), rt=0.4)
        for n in range(10):
            check(n, 0.13)
        self.close_seg()

        o = big_o_pow("n", 3, 80, MC_RED)
        o.move_to([0.9, 1.0, 0])

        self.seg(4)
        for n in range(10, len(shown)):
            check(n, 0.1)
        self.until(at(4, "Cubic") - 0.6)
        self.sfx("break", 0.4)
        self.beat(FadeOut(cnt), FadeIn(o, scale=0.5), Wiggle(pick), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        word = "racecar"
        row = block_row(list(word), 2.6, size=0.95, gap=0.15)
        mir = mirror_at(row, 6)

        self.seg(5)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(row), rt=0.5)
        self.until(at(5, "mirror") - 0.1)
        self.sfx("click", 0.3)
        self.beat(GrowFromCenter(mir), rt=0.4)
        self.until(at(5, "center") - 0.1)
        self.beat(pulse(row[3], 1.25), pulse(mir, 1.2), rt=0.5)
        self.close_seg()

        frames = VGroup(outline(row[3], MC_GREEN, 8), outline(row[3], MC_GREEN, 8))
        arrows = VGroup(MT("<", 60, MC_YELLOW, PIXEL).next_to(row, DOWN, buff=0.3).shift(LEFT * 1.0),
                        MT(">", 60, MC_YELLOW, PIXEL).next_to(row, DOWN, buff=0.3).shift(RIGHT * 1.0))

        self.seg(6)
        self.until(at(6, "expand") - 0.2)
        self.beat(Create(frames), FadeIn(arrows), rt=0.35)
        for d in (1, 2, 3):
            self.sfx(f"stone_step{d}", 0.35)
            self.beat(frames[0].animate.move_to(row[3 - d]), frames[1].animate.move_to(row[3 + d]),
                      arrows[0].animate.shift(LEFT * 0.6), arrows[1].animate.shift(RIGHT * 0.6), rt=0.5)
            self.beat(pulse(row[3 - d], 1.12), pulse(row[3 + d], 1.12), rt=0.25)
        self.close_seg()

        odd = block_row(list("aba"), -0.9, size=0.8, gap=0.12, x=-2.1)
        even = block_row(list("abba"), -0.9, size=0.8, gap=0.12, x=2.0)
        mo, me = mirror_at(odd, 2), mirror_at(even, 3)
        lo = MT("odd: on a block", 36, MC_AQUA).next_to(odd, DOWN, buff=0.35)
        le = MT("even: in a gap", 36, MC_GOLD).next_to(even, DOWN, buff=0.35)

        self.seg(7)
        self.beat(FadeOut(frames), FadeOut(arrows), rt=0.3)
        self.until(at(7, "a block") - 0.3)
        self.beat(FadeIn(odd, shift=UP * 0.2), rt=0.4)
        self.beat(GrowFromCenter(mo), FadeIn(lo), rt=0.4)
        self.until(at(7, "the gap") - 0.3)
        self.beat(FadeIn(even, shift=UP * 0.2), rt=0.4)
        self.sfx("click", 0.3)
        self.beat(GrowFromCenter(me), FadeIn(le), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("CENTERS", MC_GREEN)
        code = code_panel(CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 3, 3, MC_YELLOW)
        st = {"best": None, "bt": None, "cmp": None, "barin": False}

        def best_badge(v):
            return chat(f"best {v}", MC_GOLD if v > 1 else MC_GRAY, 42).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)

        def best_text(lo, hi, color=MC_GOLD):
            return chat(" ".join(S[lo:hi + 1]) + f"   len {hi - lo + 1}", color, 46).move_to([0, 4.35, 0])

        def cmp_text(l, r, kind):
            if kind == "edge":
                return MT("end of the row: stop", 46, MC_GRAY).move_to([0, -0.9, 0])
            ok = kind == "match"
            return eq_line([(f"s[{l}] {S[l]}", MC_WHITE), ("=" if ok else "!=", MC_GREEN if ok else MC_RED), (f"{S[r]} s[{r}]", MC_WHITE)],
                           46, buff=0.35).move_to([0, -0.9, 0])

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("row_in", "toast", "beats")]
        for k, e in enumerate(CENTERS):
            ev.append((seg_time(W["first"], e["start"]), "center", k))
            if not e["fast"]:
                for q, spec in enumerate(e["times"]):
                    ev.append((seg_time(W["first"], spec), f"cmp{q}", k))
            if "best" in e:
                ev.append((seg_time(W["first"], e["best"]), "best", k))
        ev.sort(key=lambda x: x[0])

        def move_bar(k0, k1=None, color=MC_YELLOW, rt=0.12):
            self.beat(Transform(bar, line_bar(code, k0, k1, color)), rt=rt)

        def show_cmp(new, rt=0.15):
            anims = [FadeIn(new)]
            if st["cmp"] is not None:
                anims.append(FadeOut(st["cmp"]))
            st["cmp"] = new
            self.beat(*anims, rt=rt)

        def on_first():
            st["best"] = best_badge(0)
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(st["best"]), rt=0.35)

        def on(kind, k):
            e = CENTERS[k] if k is not None else None
            if kind == "row_in":
                for i in range(len(S)):
                    self.sfx(f"stone_dig{i % 4 + 1}", 0.25, delay=0.08 * i + 0.35)
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
            elif kind == "center":
                self.sfx("click", 0.18)
                if not st["barin"]:
                    st["barin"] = True
                    self.beat(FadeIn(bar), rt=0.12)
                if e["fast"]:
                    # Quick centers: show where the expansion ended in one step
                    l, r, kk = e["cmps"][-1]
                    self.beat(Transform(bar, line_bar(code, 4, 4, MC_GREEN if kk == "edge" else MC_RED)), rt=0.12)
                    show_cmp(cmp_text(l, r, kk), rt=0.12)
                else:
                    move_bar(3, rt=0.15)
            elif kind.startswith("cmp"):
                l, r, kk = e["cmps"][int(kind[3:])]
                self.sfx("stone_step%d" % (int(kind[3:]) % 6 + 1) if kk == "match" else "click", 0.32)
                move_bar(4 if kk != "match" else 5, None, MC_GREEN if kk == "match" else MC_GRAY, rt=0.15)
                show_cmp(cmp_text(l, r, kk), rt=0.2)
            elif kind == "best":
                l, r = e["cmps"][-1][:2]
                self.sfx("orb", 0.3)
                anims = [Transform(bar, line_bar(code, 6, 7, MC_GOLD))]
                # After the toast the badge is gone; the best text above the row carries the length
                if st["best"] is not None:
                    anims.append(Transform(st["best"], best_badge(e["len"])))
                new = best_text(l + 1, r - 1)
                if st["bt"] is None:
                    st["bt"] = new
                    anims.append(FadeIn(new, shift=DOWN * 0.1))
                else:
                    anims.append(Transform(st["bt"], new))
                self.beat(*anims, rt=0.2)
            elif kind == "toast":
                t = toast("Advancement Made!", "Racecar found", w=4.6)
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                for d in (0.1, 0.3, 0.5, 0.7):
                    self.sfx("orb", 0.26, delay=d)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(st["best"]), rt=0.5)
                st["best"] = None
            elif kind == "beats":
                self.beat(pulse(st["bt"], 1.1), rt=0.4)

        def on_last():
            # The row leaves the 3D clip when the walk ends; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        row = block_row(list(S), 3.6, size=0.75, gap=0.1)
        ticks = VGroup(*[mirror_at(row, c, 0.5).move_to([mirror_at(row, c).get_x(), 2.85, 0]) for c in range(2 * len(S) - 1)])
        cnt = MT("2n - 1 = 19 centers", 40, MC_WHITE).move_to([0, 2.15, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n²)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, 0.7, 0])
        each = MT("each one expands up to n", 36, MC_GRAY).move_to([0, -0.25, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, -1.0, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(15)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(row), rt=0.5)
        self.until(at(15, "centers") - 0.6)
        self.sfx("click", 0.25)
        self.beat(LaggedStart(*[GrowFromCenter(x) for x in ticks], lag_ratio=0.06), FadeIn(cnt), rt=0.9)
        self.until(at(15, "expand") - 0.2)
        self.beat(FadeIn(each, shift=UP * 0.1), rt=0.4)
        self.until(at(15, "So the time") - 0.2)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.4)
        self.add(xp)
        for d in (0.0, 0.3, 0.6):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=0.9)
        self.beat(Restore(xp), rt=1.0)
        self.close_seg()

        ptrs = VGroup(*[chat(s, MC_WHITE, 46) for s in ("l", "r", "best")]).arrange(RIGHT, buff=0.3).move_to([0, -2.4, 0])
        sp = VGroup(MT("space", 56, MC_GRAY), level_text("O(1)", 1.0)).arrange(RIGHT, buff=0.4).move_to([0, -3.7, 0])

        self.seg(16)
        self.until(at(16, "two pointers") - 0.2)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(*[FadeIn(p, scale=0.6) for p in ptrs], lag_ratio=0.2), rt=0.6)
        self.until(at(16, "constant") - 0.4)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(CODE, 1.6, width=8.4)
        bar = line_bar(code, 3, 3, MC_YELLOW)

        self.seg(17)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(at(17, "expand") - 0.2)
        self.beat(Transform(bar, line_bar(code, 4, 5, MC_GOLD)), rt=0.35)
        self.close_seg()

        self.seg(18)
        msg = chat("Start from the middle", MC_GOLD, 58)
        msg.move_to([0, -2.3, 0])
        self.beat(FadeIn(msg, shift=UP * 0.2), Transform(bar, line_bar(code, 0, 8, MC_GREEN)), rt=0.4)
        self.until(1.2)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.45)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=0.9)
        self.close_seg()
