import math

WALK = json.load(open('walk.json', encoding='utf-8'))
CHARS, ORES = WALK["chars"], WALK["ores"]
ORE_OF.update(dict(zip(CHARS, ORES)))
ORE_OF.update({"g": "gold", "f": "iron"})

ISO_SIDE, ISO_FILL = 0.61, 0.88

SEARCH_CODE = """def minOperations(s):
    # BFS: try every substring of length < n
    q = deque([(s, 0)])
    while q:
        curr, ops = q.popleft()
        if curr == sorted(curr):
            return ops
        for i in range(len(s)):
            for j in range(i + 1, len(s) + 1):
                if j - i < len(s):
                    q.append((sort_sub(curr, i, j), ops + 1))"""

GREEDY_CODE = """def minOperations(s: str) -> int:
    if s == "".join(sorted(s)):
        return 0
    n = len(s)
    if n <= 2:
        return -1
    mn, mx = min(s), max(s)
    if s[0] == mn or s[-1] == mx:
        return 1
    if mn in s[:-1] or mx in s[1:]:
        return 2
    return 3"""


def index_row(row, size=34, color=MC_GRAY, buff=0.14):
    return VGroup(*[MT(str(k), size, color).next_to(b, DOWN, buff=buff) for k, b in enumerate(row)])


def target_sign(scale=1.0):
    return sign(["target", "abcd"], 2.2, 1.35, 46).scale(scale)


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def eq_line(parts, size=34, font=PIXEL, buff=0.3):
    return VGroup(*[MT(s, size, c, font) for s, c in parts]).arrange(RIGHT, buff=buff)


def cover():
    title = stone_title("SORT STRING", 56, width=7.8).move_to([0, 4.0, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.25, 2.75, 0])
    row = block_row(CHARS, 0.95, size=1.05, gap=0.2)
    idx = index_row(row)
    pick = pickaxe(1.25).move_to([-1.3, -1.2, 0])
    chest = chest_icon(1.15).move_to([1.3, -1.2, 0])
    tags = VGroup(chat("LeetCode #3863", MC_AQUA, 46), chat("Medium", MC_YELLOW, 46), chat("Greedy", MC_GOLD, 46))
    tags.arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, title, spl, row, idx, pick, chest, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, title, spl, row, idx, pick, chest, tags = art
        self.add(art)

        spl_w = spl.width
        spl_center = spl.get_center()

        def pulse(m, dt):
            factor = 1.0 + 0.22 * math.sin(self.time * 2 * math.pi)
            m.scale_to_fit_width(spl_w * factor)
            m.move_to(spl_center)

        spl.add_updater(pulse)

        self.seg(0)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.35) for b in row], lag_ratio=0.18), rt=1.6)
        self.sfx("stone_dig1", 0.35, delay=0.35)
        self.beat(*[ShowPassingFlash(outline(b, MC_GOLD, 10), time_width=0.6) for b in row],
                  Rotate(pick, angle=-30 * DEGREES, rate_func=there_and_back), rt=0.9)
        self.until(7.0)
        spl.clear_updaters()
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        tsign = target_sign().move_to([0, 3.55, 0])
        row = block_row(CHARS, 1.15, size=1.05, gap=0.2)
        idx = index_row(row)
        lab = MT("s = \"dbca\"", 40, MC_WHITE).next_to(row, UP, buff=0.2).align_to(row, LEFT)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(len(row)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.32, delay=k * 0.12 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                               lag_ratio=0.12), rt=1.6)
        self.beat(FadeIn(idx, shift=UP * 0.1), FadeIn(lab), rt=0.4)
        self.until(3.2)
        self.sfx("wood_dig1", 0.4)
        self.beat(FadeIn(tsign, scale=0.6), rt=0.5)
        self.close_seg()

        self.seg(2)
        # Highlight substring rule
        sub_box = outline(VGroup(row[0], row[1], row[2]), MC_YELLOW, 8)
        rule = chat("sort substring (len < n)", MC_YELLOW, 36).move_to([0, -0.9, 0])
        q = chat("fewest operations?", MC_GOLD, 46).move_to([0, -2.2, 0])

        self.until(0.3)
        self.sfx("click", 0.3)
        self.beat(Create(sub_box), FadeIn(rule, shift=UP * 0.1), rt=0.6)
        self.until(2.5)
        self.beat(FadeIn(q, scale=0.8), rt=0.6)
        self.until(4.8)
        self.clear_all(rt=0.4)
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("BRUTE SEARCH", MC_RED)
        
        # Edge case len 2
        bad_row = block_row(["g", "f"], 2.2, size=1.05, gap=0.2)
        bad_lbl = MT("length 2:", 36, MC_GRAY).next_to(bad_row, LEFT, buff=0.4)
        no_op = chat("len < 2 -> size 1 only! (no change)", MC_RED, 34).next_to(bad_row, DOWN, buff=0.3)
        res_neg1 = chat("return -1", MC_RED, 44).move_to([0, 0.2, 0])

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(0.8)
        self.beat(FadeIn(bad_lbl), FadeIn(bad_row), FadeIn(no_op), rt=0.6)
        self.until(3.6)
        self.sfx("villager_no1", 0.35)
        self.beat(FadeIn(res_neg1, scale=1.1), rt=0.5)
        self.close_seg()

        self.seg(4)
        self.beat(FadeOut(VGroup(bad_row, bad_lbl, no_op, res_neg1)), rt=0.4)
        zero_rule = chat("already sorted? -> return 0", MC_GREEN, 38).move_to([0, 2.5, 0])
        search_lbl = chat("otherwise: explore every sort!", MC_YELLOW, 38).move_to([0, 0.8, 0])
        self.until(0.4)
        self.beat(FadeIn(zero_rule), rt=0.5)
        self.until(2.4)
        self.beat(FadeIn(search_lbl, shift=UP * 0.2), rt=0.5)
        self.close_seg()

        self.seg(5)
        self.beat(FadeOut(VGroup(zero_rule, search_lbl)), rt=0.3)
        code = code_panel(SEARCH_CODE, -1.0, width=8.4, max_h=3.6)
        bar = line_bar(code, 6, 8, MC_YELLOW)
        self.beat(FadeIn(code), FadeIn(bar), rt=0.6)
        self.until(2.5)
        n2_lbl = chat("~ n^2 substrings per step", MC_RED, 40).move_to([0, 2.8, 0])
        self.beat(FadeIn(n2_lbl, shift=DOWN * 0.2), rt=0.5)
        self.close_seg()

        self.seg(6)
        big_n = MT("n = 100,000", 42, MC_WHITE).move_to([0, 2.8, 0])
        blowup = chat("Search space explodes!", MC_RED, 46).move_to([0, 1.6, 0])
        never = MT("NEVER FINISHES", 48, MC_RED, PIXEL).move_to([0, -2.5, 0])
        self.beat(FadeOut(VGroup(code, bar, n2_lbl)), rt=0.4)
        self.beat(FadeIn(big_n), FadeIn(blowup, scale=1.1), rt=0.6)
        self.until(2.0)
        self.sfx("break", 0.4)
        self.beat(FadeIn(never, scale=1.3), rt=0.6)
        self.until(3.6)
        self.clear_all(rt=0.4)
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        bound = chat("Answer is ALWAYS <= 3", MC_GOLD, 46).move_to([0, 3.6, 0])
        
        c1 = chat("min at s[0] -> sort suffix s[1:] (1 op)", MC_GREEN, 34).move_to([0, 2.0, 0])
        c2 = chat("max at s[-1] -> sort prefix s[:-1] (1 op)", MC_GREEN, 34).move_to([0, 1.1, 0])
        c3 = chat("min in s[:-1] or max in s[1:] (2 ops)", MC_AQUA, 34).move_to([0, 0.2, 0])
        c4 = chat("min stuck at end AND max at start (3 ops)", MC_RED, 34).move_to([0, -0.7, 0])

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(bound, scale=0.8), rt=0.6)
        self.until(2.0)
        self.sfx("pop", 0.3)
        self.beat(FadeIn(c1, shift=UP * 0.1), rt=0.5)
        self.until(4.5)
        self.sfx("pop", 0.3)
        self.beat(FadeIn(c2, shift=UP * 0.1), rt=0.5)
        self.close_seg()

        self.seg(8)
        self.until(0.3)
        self.sfx("pop", 0.3)
        self.beat(FadeIn(c3, shift=UP * 0.1), rt=0.5)
        self.until(3.2)
        self.sfx("pop", 0.3)
        self.beat(FadeIn(c4, shift=UP * 0.1), rt=0.5)
        self.until(6.5)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        E = W["events"]
        h = hdr("THE CHECKS", MC_GREEN)
        tsign = target_sign(0.6)
        tsign.move_to([0, TOP_Y - 0.05, 0]).to_edge(RIGHT, buff=0.4)

        code = code_panel(GREEDY_CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 0, 0, MC_YELLOW)
        
        info_panel = chat("Checking s = \"dbca\"...", MC_WHITE, 36).move_to([0, 4.3, 0])
        
        chk1 = chat("1. Sorted? No", MC_GRAY, 32).move_to([-1.8, 0.9, 0])
        chk2 = chat("2. n <= 2? No", MC_GRAY, 32).move_to([1.8, 0.9, 0])
        chk3 = chat("3. s[0]=='a' or s[-1]=='d'? No", MC_GRAY, 32).move_to([0, 0.2, 0])
        chk4 = chat("4. 'a' in s[:-1] or 'd' in s[1:]? No", MC_GRAY, 32).move_to([0, -0.5, 0])
        verdict = chat("Stuck at wrong ends! -> 3 Ops", MC_RED, 38).move_to([0, -1.35, 0])
        
        op_step = chat("", MC_YELLOW, 42).move_to([0, 4.3, 0])

        ev = [
            (seg_time(W["first"], E["intro_row"]), "intro_row", None),
            (seg_time(W["first"], E["checks_in"]), "checks_in", None),
            (seg_time(W["first"], E["check_sorted"]), "check_sorted", None),
            (seg_time(W["first"], E["check_len2"]), "check_len2", None),
            (seg_time(W["first"], E["check_min_first"]), "check_min_first", None),
            (seg_time(W["first"], E["check_max_last"]), "check_max_last", None),
            (seg_time(W["first"], E["check_min_prefix"]), "check_min_prefix", None),
            (seg_time(W["first"], E["check_max_suffix"]), "check_max_suffix", None),
            (seg_time(W["first"], E["stuck"]), "stuck", None),
            (seg_time(W["first"], E["answer_three"]), "answer_three", None),
            (seg_time(W["first"], E["watch"]), "watch", None),
            (seg_time(W["first"], E["op1_select"]), "op1_select", None),
            (seg_time(W["first"], E["op1_sort"]), "op1_sort", None),
            (seg_time(W["first"], E["op2_select"]), "op2_select", None),
            (seg_time(W["first"], E["op2_sort"]), "op2_sort", None),
            (seg_time(W["first"], E["op3_select"]), "op3_select", None),
            (seg_time(W["first"], E["op3_sort"]), "op3_sort", None),
            (seg_time(W["first"], E["sorted_done"]), "sorted_done", None),
            (seg_time(W["first"], E["toast"]), "toast", None),
            (seg_time(W["first"], E["answer"]), "answer", None),
        ]
        ev.sort(key=lambda e: e[0])

        def move_bar(line, color=MC_YELLOW, rt=0.15):
            self.beat(Transform(bar, line_bar(code, line, line, color)), rt=rt)

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(tsign), rt=0.35)

        def on(kind, _):
            if kind == "intro_row":
                self.beat(FadeIn(code, shift=UP * 0.3), FadeIn(info_panel), rt=0.5)
            elif kind == "checks_in":
                self.beat(FadeIn(bar), rt=0.3)
            elif kind == "check_sorted":
                move_bar(1)
                self.sfx("click", 0.25)
                self.beat(FadeIn(chk1), rt=0.25)
            elif kind == "check_len2":
                move_bar(3)
                self.sfx("click", 0.25)
                self.beat(FadeIn(chk2), rt=0.25)
            elif kind == "check_min_first":
                move_bar(6)
                self.sfx("click", 0.25)
                self.beat(FadeIn(chk3), rt=0.25)
            elif kind == "check_max_last":
                move_bar(6, MC_RED)
            elif kind == "check_min_prefix":
                move_bar(8)
                self.sfx("click", 0.25)
                self.beat(FadeIn(chk4), rt=0.25)
            elif kind == "check_max_suffix":
                move_bar(8, MC_RED)
            elif kind == "stuck":
                move_bar(10, MC_RED)
                self.sfx("villager_no1", 0.3)
                self.beat(FadeIn(verdict, scale=1.1), rt=0.4)
            elif kind == "answer_three":
                self.beat(verdict.animate.set_color(MC_GOLD).scale(1.1), rt=0.3)
            elif kind == "watch":
                self.beat(FadeOut(VGroup(chk1, chk2, chk3, chk4, verdict, info_panel)), rt=0.4)
            elif kind == "op1_select":
                self.sfx("wood_dig1", 0.3)
                self.beat(Transform(op_step, chat("Op 1: Sort \"dbc\" -> \"bcd\"", MC_YELLOW, 42).move_to([0, 4.3, 0])), rt=0.25)
            elif kind == "op1_sort":
                self.sfx("stone_dig1", 0.35)
            elif kind == "op2_select":
                self.sfx("wood_dig2", 0.3)
                self.beat(Transform(op_step, chat("Op 2: Sort \"cda\" -> \"acd\"", MC_AQUA, 42).move_to([0, 4.3, 0])), rt=0.25)
            elif kind == "op2_sort":
                self.sfx("stone_dig2", 0.35)
            elif kind == "op3_select":
                self.sfx("wood_dig3", 0.3)
                self.beat(Transform(op_step, chat("Op 3: Sort \"bac\" -> \"abc\"", MC_GREEN, 42).move_to([0, 4.3, 0])), rt=0.25)
            elif kind == "op3_sort":
                self.sfx("stone_dig3", 0.35)
            elif kind == "sorted_done":
                for d in (0.0, 0.15, 0.35, 0.55):
                    self.sfx("orb", 0.3, delay=d)
                self.beat(Transform(op_step, chat("Sorted: \"abcd\"!", MC_GREEN, 48).move_to([0, 4.3, 0])), rt=0.3)
            elif kind == "toast":
                t = toast("Advancement Made!", "3 operations sort dbca")
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(tsign), rt=0.5)
            elif kind == "answer":
                ans = chat("return 3", MC_GREEN, 56)
                ans.move_to([0, -0.6, 0])
                self.beat(FadeIn(ans, shift=UP * 0.2), rt=0.4)

        def on_last():
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        scan = VGroup(pickaxe(0.9), MT("scan & min/max", 48, MC_WHITE), MT("O(n)", 40, MC_GREEN, PIXEL))
        scan.arrange(RIGHT, buff=0.35).move_to([0, 3.4, 0])
        
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n)", 1.05)).arrange(RIGHT, buff=0.4)
        tm.move_to([0, 1.65, 0])
        
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.6, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(0.5)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in scan], lag_ratio=0.25), rt=0.8)
        self.until(2.2)
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.4)
        self.add(xp)
        for d in (0.0, 0.3, 0.6, 0.9):
            self.sfx("orb", 0.25, delay=d)
        self.sfx("levelup", 0.3, delay=1.2)
        self.beat(Restore(xp), rt=1.2)
        self.close_seg()

        self.seg(17)
        mem = VGroup(chest_icon(0.85), MT("extra space", 52, MC_WHITE), MT("O(1)", 44, MC_GOLD, PIXEL))
        mem.arrange(RIGHT, buff=0.35).move_to([0, -1.5, 0])
        self.until(0.3)
        self.beat(FadeIn(mem, shift=UP * 0.2), rt=0.6)
        self.until(3.0)
        self.clear_all(rt=0.4)
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(GREEDY_CODE, 1.6, width=8.4)
        bar = line_bar(code, 0, 0, MC_YELLOW)

        self.seg(18)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.06), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(1.2)
        self.beat(Transform(bar, line_bar(code, 6, 7, MC_AQUA)), rt=0.35)
        self.until(2.4)
        self.beat(Transform(bar, line_bar(code, 8, 9, MC_GREEN)), rt=0.4)
        self.close_seg()

        self.seg(19)
        msg = chat("Think before you search", MC_GOLD, 56)
        msg.move_to([0, -2.4, 0])
        self.until(0.1)
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.5)
        self.until(2.2)
        self.beat(FadeOut(Group(code, bar, msg)), rt=0.5)
        self.finish(FadeIn(cover()), rt=1.0)
        self.close_seg()
