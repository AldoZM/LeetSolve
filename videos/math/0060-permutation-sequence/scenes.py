WALK = json.load(open('walk.json', encoding='utf-8'))
NUMS = WALK["nums"]
ORES = WALK["ores"]
ORE_OF.update(dict(zip(NUMS, ORES)))
N = WALK["n"]
K = WALK["k"]
K_0 = WALK["k_0"]

MATH_CODE = """def getPermutation(n, k):
    fact = [1] * n
    for i in range(1, n):
        fact[i] = fact[i - 1] * i
    nums = [i for i in range(1, n + 1)]
    k -= 1
    res = []
    for i in range(n - 1, -1, -1):
        idx = k // fact[i]
        k %= fact[i]
        res.append(str(nums.pop(idx)))
    return "".join(res)"""

BRUTE_CODE = """def getPermutation(n, k):
    nums = [str(i) for i in range(1, n + 1)]
    perms = itertools.permutations(nums)
    for i, p in enumerate(perms):
        if i == k - 1:
            return "".join(p)"""


def index_row(row, size=34, color=MC_GRAY, buff=0.14):
    return VGroup(*[MT(str(k), size, color).next_to(b, DOWN, buff=buff) for k, b in enumerate(row)])


def target_sign(scale=1.0):
    return sign(["target", f"k = {K}"], 2.2, 1.35, 42).scale(scale)


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def eq_line(parts, size=34, font=PIXEL, buff=0.25):
    return VGroup(*[MT(s, size, c, font) for s, c in parts]).arrange(RIGHT, buff=buff)


def iso_block_tall(tex, w=0.6, h_ratio=0.78):
    img = _load(tex)
    faces = VGroup()
    L, B, R, F = np.array([-w / 2, w / 4, 0]), np.array([0, w / 2, 0]), np.array([w / 2, w / 4, 0]), np.array([0, 0, 0])
    down = np.array([0, -w * h_ratio, 0])
    for e1, e2, center, light in [
        (F - L, B - L, (L + R) / 2, 1.0),
        (F - L, -down, (L + F) / 2 + down / 2, 0.8),
        (R - F, -down, (F + R) / 2 + down / 2, 0.62),
    ]:
        art = pixel_image(ImageEnhance.Brightness(img).enhance(light), 1)
        art.apply_matrix([[e1[0], e2[0], 0], [e1[1], e2[1], 0], [0, 0, 1]], about_point=ORIGIN)
        faces.add(art.shift(center))
    return faces.move_to(ORIGIN)


def slot_item(inv, k, val, ore):
    icon = iso_block_tall(f"{ore}_ore", 14 * inv.u, h_ratio=0.78)
    slot_center = inv.slots[k].get_center()
    icon.move_to(slot_center + UP * (inv.u * 0.8))
    txt = gui_text(str(val), MC_WHITE, inv.u * 0.85)
    txt.move_to(slot_center + np.array([inv.u * 5.2, -inv.u * 4.8, 0]), aligned_edge=DR)
    return VGroup(icon, txt)


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    title = stone_title("PERMUTATION SEQUENCE", 44, width=8.2).move_to([0, 4.0, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.25, 2.75, 0])
    row = block_row(NUMS, 1.05, size=1.05, gap=0.2)
    idx = index_row(row)
    ts = target_sign(0.85).move_to([-1.6, -1.2, 0])
    chest = chest_icon(1.15).move_to([1.6, -1.2, 0])
    tags = VGroup(
        chat("LeetCode #60", MC_AQUA, 40),
        chat("Hard", MC_RED, 40),
        chat("Factorial Math", MC_GOLD, 40)
    )
    tags.arrange(RIGHT, buff=0.2).move_to([0, -3.05, 0])
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, title, spl, row, idx, ts, chest, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, title, spl, row, idx, ts, chest, tags = art
        self.add(art)

        self.seg(0)
        # Splash pulses continuously across beats like in the title screen, with no rotation drift
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        self.sfx("stone_dig1", 0.35, delay=0.2)
        self.beat(
            spl.animate(rate_func=there_and_back).scale(1.15),
            LaggedStart(
                *[b.animate(rate_func=there_and_back).shift(UP * 0.3) for b in row],
                lag_ratio=0.18
            ),
            rt=1.4
        )
        self.beat(
            spl.animate(rate_func=there_and_back).scale(1.15),
            *[ShowPassingFlash(outline(row[k], MC_GOLD, 10), time_width=0.6) for k in range(4)],
            *[row[k].animate(rate_func=there_and_back).scale(1.12) for k in range(4)],
            rt=1.0
        )
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        row = block_row(NUMS, 1.3, size=1.05, gap=0.2)
        idx = index_row(row)
        lab = MT("nums = [1, 2, 3, 4]", 38, MC_WHITE).next_to(row, UP, buff=0.25)
        tsign = target_sign().move_to([0, 3.55, 0])

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(len(row)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.32, delay=k * 0.12 + 0.36)
        self.beat(
            LaggedStart(
                *[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                lag_ratio=0.12
            ),
            rt=1.6
        )
        self.beat(FadeIn(idx, shift=UP * 0.1), FadeIn(lab), rt=0.4)
        self.until(3.2)
        fact_text = eq_line([("4!", MC_YELLOW), ("=", MC_GRAY), ("24", MC_GOLD), ("permutations", MC_WHITE)], 36)
        fact_text.move_to([0, -0.6, 0])
        self.beat(FadeIn(fact_text, shift=UP * 0.2), rt=0.6)
        self.close_seg()

        self.seg(2)
        self.sfx("wood_dig1", 0.4)
        self.beat(FadeIn(tsign, scale=0.6), rt=0.5)
        self.until(1.4)
        q_box = eq_line([("9th sequence:", MC_WHITE), ("?", MC_GOLD)], 42)
        q_box.move_to([0, -2.2, 0])
        self.beat(FadeIn(q_box, shift=UP * 0.2), rt=0.5)
        self.until(3.6)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("BRUTE FORCE", MC_RED)
        row = block_row(NUMS, 3.1, size=0.95, gap=0.2)
        idx = index_row(row, 30)
        code = code_panel(BRUTE_CODE, -3.7, max_h=2.9)
        pick = pickaxe(1.05).move_to([-2.4, 1.2, 0])
        dbg = Rectangle(width=1.2, height=0.16, fill_color="#000000", fill_opacity=1, stroke_width=0)
        dbg.next_to(pick, DOWN, buff=0.15)

        def dfill(frac):
            r = Rectangle(
                width=max(1.16 * frac, 0.02), height=0.1, stroke_width=0, fill_opacity=1,
                fill_color=interpolate_color(ManimColor(MC_RED), ManimColor(MC_GREEN), frac)
            )
            r.move_to(dbg.get_left() + RIGHT * (0.02 + max(1.16 * frac, 0.02) / 2))
            return r

        def counter(k):
            c = MT(f"perm #{k}", 30, MC_WHITE, PIXEL)
            c.move_to([1.0, 1.2, 0])
            return c

        fill, cnt = dfill(1.0), counter(1)

        self.seg(3)
        self.beat(
            FadeIn(h, shift=RIGHT * 0.3),
            LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in row], lag_ratio=0.1),
            rt=0.9
        )
        self.beat(FadeIn(idx), rt=0.3)
        self.until(1.6)
        self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
        self.until(2.8)
        self.beat(FadeIn(pick, scale=0.6), FadeIn(dbg), FadeIn(fill), FadeIn(cnt), rt=0.5)
        self.close_seg()

        bar = line_bar(code, 3, 4, MC_YELLOW)

        self.seg(4)
        self.beat(FadeIn(bar), rt=0.3)
        perms_preview = ["1234", "1243", "1324", "1342", "1423", "1432", "2134", "2143", "2314"]
        cur_p = MT(perms_preview[0], 36, MC_GOLD, PIXEL).move_to([0, -0.6, 0])
        self.beat(FadeIn(cur_p), rt=0.3)

        for step_i in range(1, 6):
            nf, nc = dfill(1 - step_i / 9), counter(step_i + 1)
            next_p = MT(perms_preview[step_i], 36, MC_GOLD, PIXEL).move_to([0, -0.6, 0])
            self.sfx(f"stone_dig{step_i % 4 + 1}", 0.22, delay=0.15)
            self.beat(
                Transform(fill, nf),
                Transform(cnt, nc),
                Transform(cur_p, next_p),
                Rotate(pick, angle=-25 * DEGREES, rate_func=there_and_back),
                rt=0.5
            )
        self.close_seg()

        self.seg(5)
        for step_i in range(6, 9):
            nf, nc = dfill(1 - step_i / 9), counter(step_i + 1)
            next_p = MT(perms_preview[step_i], 36, MC_GREEN if step_i == 8 else MC_GOLD, PIXEL).move_to([0, -0.6, 0])
            self.sfx(f"stone_dig{step_i % 4 + 1}", 0.22, delay=0.12)
            self.beat(
                Transform(fill, nf),
                Transform(cnt, nc),
                Transform(cur_p, next_p),
                Rotate(pick, angle=-25 * DEGREES, rate_func=there_and_back),
                rt=0.45
            )

        n9 = eq_line([("n = 9", MC_YELLOW), ("->", MC_GRAY), ("9! = 362,880", MC_RED)], 36)
        n9.move_to([0, 1.8, 0])
        self.until(3.8)
        self.beat(FadeIn(n9, shift=UP * 0.2), rt=0.6)
        self.close_seg()

        self.seg(6)
        self.sfx("villager_no1", 0.4)
        self.sfx("break", 0.45, delay=0.8)
        broken = MT("pickaxe broken!", 36, MC_RED)
        broken.next_to(dbg, DOWN, buff=0.15)
        self.beat(Wiggle(pick), FadeIn(broken, shift=UP * 0.1), rt=0.8)
        self.until(2.2)
        self.beat(
            FadeOut(VGroup(row, idx, code, bar, pick, dbg, fill, cnt, cur_p, n9, broken)),
            rt=0.5
        )
        big_o = eq_line([("Time:", MC_GRAY), ("O(n * n!)", MC_RED)], 52)
        big_o.move_to([0, 0, 0])
        brutal = MT("Factorial growth is brutal", 40, MC_RED)
        brutal.next_to(big_o, DOWN, buff=0.4)
        self.beat(FadeIn(big_o, scale=0.6), FadeIn(brutal), rt=0.7)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        tsign = target_sign().move_to([0, 3.55, 0])

        g0 = eq_line([("Starts with 1:", MC_AQUA), ("3! = 6", MC_WHITE)], 32)
        g1 = eq_line([("Starts with 2:", MC_GOLD), ("3! = 6", MC_YELLOW)], 32)
        g2 = eq_line([("Starts with 3:", MC_AQUA), ("3! = 6", MC_WHITE)], 32)
        g3 = eq_line([("Starts with 4:", MC_AQUA), ("3! = 6", MC_WHITE)], 32)
        groups_box = VGroup(g0, g1, g2, g3).arrange(DOWN, buff=0.25).move_to([0, 1.4, 0])

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(tsign, scale=0.6), rt=0.6)
        self.until(1.5)
        self.beat(
            LaggedStart(*[FadeIn(g, shift=RIGHT * 0.2) for g in groups_box], lag_ratio=0.18),
            rt=1.2
        )
        self.until(4.2)
        frame_g1 = outline(g1, MC_GOLD, 6, buff=0.08)
        self.sfx("pop", 0.35)
        self.beat(Create(frame_g1), g1.animate.scale(1.08), rt=0.6)
        self.close_seg()

        self.seg(8)
        self.beat(FadeOut(groups_box), FadeOut(frame_g1), rt=0.35)
        div_title = MT("Factorial Number System", 44, MC_GOLD).move_to([0, 1.5, 0])
        k0_text = eq_line([("k - 1 =", MC_GRAY), ("8", MC_YELLOW)], 38).move_to([0, 0.5, 0])
        div_step = eq_line([
            ("8", MC_YELLOW), ("//", MC_GRAY), ("6", MC_AQUA), ("=", MC_GRAY), ("1", MC_GOLD),
            ("(rem 2)", MC_GRAY)
        ], 38).move_to([0, -0.4, 0])
        pick_text = chat("quotient 1 -> pick iron block (2!)", MC_GREEN, 38).move_to([0, -1.5, 0])

        self.beat(FadeIn(div_title, shift=UP * 0.2), rt=0.5)
        self.until(1.4)
        self.beat(FadeIn(k0_text), rt=0.4)
        self.until(2.6)
        self.beat(FadeIn(div_step, shift=UP * 0.15), rt=0.5)
        self.until(4.2)
        self.sfx("pop", 0.4)
        self.beat(FadeIn(pick_text, shift=UP * 0.15), rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("FACTORIAL WALK", MC_GREEN)
        tsign = target_sign(0.6)
        tsign.move_to([0, TOP_Y - 0.05, 0]).to_edge(RIGHT, buff=0.4)
        inv = Inventory(9, "Chest")
        inv.move_to([0, -1.15, 0])
        title2 = inv.title_for("Chest = result permutation")
        code = code_panel(MATH_CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 4, 5, MC_YELLOW)
        calc_box = VGroup()

        ev = [
            (seg_time(W["first"], W["k_zero"]), "k_zero", None),
            (seg_time(W["first"], W["chest_in"]), "chest_in", None),
            (seg_time(W["first"], W["toast"]), "toast", None),
            (seg_time(W["first"], W["answer"]), "answer", None),
        ]

        for s in W["steps"]:
            k = s["step"]
            for field in ("calc_t", "quot_t", "pick_t", "store_t", "show_rem_t"):
                if field in s:
                    ev.append((seg_time(W["first"], s[field]), field, k))

        ev.sort(key=lambda e: e[0])

        def move_bar(line, color=MC_YELLOW, rt=0.15):
            self.beat(Transform(bar, line_bar(code, line, line, color)), rt=rt)

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(tsign), rt=0.35)

        def on(kind, k):
            nonlocal calc_box
            if kind == "k_zero":
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.5)
                move_bar(5)
            elif kind == "chest_in":
                self.sfx("wood_dig2", 0.4)
                self.beat(FadeIn(inv, shift=UP * 0.3), Transform(inv.title, title2), rt=0.5)
            elif kind == "calc_t":
                move_bar(8)
                st = W["steps"][k]
                new_calc = eq_line([
                    (f"k={st['k_in']}", MC_YELLOW),
                    ("//", MC_GRAY),
                    (f"{st['fact']}!", MC_AQUA),
                    ("=", MC_GRAY),
                    (f"{st['idx']}", MC_GOLD),
                ], 36).move_to([0, 1.3, 0])
                if len(calc_box) > 0:
                    self.beat(Transform(calc_box, new_calc), rt=0.2)
                else:
                    calc_box = new_calc
                    self.beat(FadeIn(calc_box, shift=UP * 0.1), rt=0.25)
            elif kind == "quot_t":
                move_bar(9)
            elif kind == "pick_t":
                move_bar(10)
            elif kind == "show_rem_t":
                move_bar(7)
            elif kind == "store_t":
                st = W["steps"][k]
                move_bar(10, MC_GREEN)
                it = slot_item(inv, st["step"], st["picked_val"], st["ore"])
                self.sfx("pop", 0.35)
                self.sfx("chestclosed", 0.22, delay=0.25)
                self.beat(FadeIn(it, scale=1.5), rt=0.25)
            elif kind == "toast":
                t = toast("Advancement Made!", "Permutation Sequence solved")
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(tsign), rt=0.5)
            elif kind == "answer":
                ans = chat("return '2314'", MC_GREEN, 56).move_to([0, 3.8, 0])
                self.sfx("orb", 0.35)
                self.beat(FadeIn(ans, shift=UP * 0.2), rt=0.4)

        def on_last():
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        look = VGroup(chest_icon(0.9), MT("direct math", 48, MC_WHITE), MT("O(1) step", 38, MC_GREEN, PIXEL))
        look.arrange(RIGHT, buff=0.35).move_to([0, 3.4, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n²)", 1.05)).arrange(RIGHT, buff=0.4)
        tm.move_to([0, 1.65, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.6, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(0.5)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in look], lag_ratio=0.25), rt=0.8)
        self.until(2.4)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.4)
        self.add(xp)
        for d in (0.0, 0.3, 0.6, 0.9):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=1.2)
        self.beat(Restore(xp), rt=1.2)
        self.close_seg()

        self.seg(17)
        old = MT("O(n * n!)", 44, MC_RED, PIXEL)
        arrow = MT("->", 70, MC_GRAY)
        new = MT("O(n²)", 44, MC_GREEN, PIXEL)
        cmp = VGroup(old, arrow, new).arrange(RIGHT, buff=0.45).move_to([0, -1.25, 0])
        strike = Line(old.get_left() + LEFT * 0.1, old.get_right() + RIGHT * 0.1, color=MC_RED, stroke_width=8)
        self.until(0.2)
        self.beat(FadeIn(old, shift=UP * 0.15), rt=0.4)
        self.until(1.2)
        self.beat(Create(strike), FadeIn(arrow), FadeIn(new, shift=LEFT * 0.2), rt=0.6)
        mem = VGroup(chest_icon(0.85), MT("memory", 52, MC_WHITE), MT("O(n)", 40, MC_GOLD, PIXEL))
        mem.arrange(RIGHT, buff=0.35).move_to([0, -3.1, 0])
        self.until(2.6)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in mem], lag_ratio=0.2), rt=0.7)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(MATH_CODE, 1.6, width=8.4)
        bar = line_bar(code, 7, 10, MC_YELLOW)
        icon = chest_icon(0.55)

        self.seg(18)
        self.beat(
            FadeIn(code.background),
            LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08),
            FadeIn(code.line_numbers),
            rt=0.7
        )
        self.beat(FadeIn(bar), rt=0.25)
        self.until(1.2)
        icon.next_to(code.code_lines[8], RIGHT, buff=0.4)
        self.beat(Transform(bar, line_bar(code, 1, 3, MC_GOLD)), FadeIn(icon, scale=0.5), rt=0.35)
        self.until(2.4)
        self.beat(Transform(bar, line_bar(code, 0, 11, MC_GREEN)), rt=0.4)
        self.close_seg()

        self.seg(19)
        msg = chat("Calculate, don't generate!", MC_GOLD, 56).move_to([0, -2.3, 0])
        self.until(0.1)
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.5)
        self.until(2.2)
        self.beat(FadeOut(Group(code, bar, icon, msg)), rt=0.5)
        # Ends on cover so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=1.0)
        self.close_seg()
