WALK = json.load(open('walk.json', encoding='utf-8'))
ROW, DOY, ANSWER = WALK["row"], WALK["doy"], WALK["answer"]
ORE_OF.update(dict(zip(ROW, WALK["ores"])))
A0, A1 = WALK["alice"]
B0, B1 = WALK["bob"]
S0, S1 = max(A0, B0), min(A1, B1)
DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Short parameter names keep the longest line short, so the panel is not shrunk to fit it
SOLVE_CODE = """def countDaysTogether(aIn, aOut, bIn, bOut):
    days = [31,28,31,30,31,30,31,31,30,31,30,31]
    def day(d):
        m, dd = int(d[:2]), int(d[3:])
        return sum(days[:m - 1]) + dd
    start = max(day(aIn), day(bIn))
    end = min(day(aOut), day(bOut))
    return max(0, end - start + 1)"""


def ph(i, phrase, shift=0.0):
    # Seconds into line i where `phrase` starts being spoken (even speaking rate inside a line)
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase)
    return max(0.0, min(dur - 0.25, dur * k / len(text) + shift))


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def pulse(m, s=1.15):
    # Pixel art is highlighted with a scale pulse; Indicate with a color paints it flat
    return m.animate(rate_func=there_and_back).scale(s)


def stay_box(row, a, b, color, buff):
    box = SurroundingRectangle(VGroup(*row[a:b + 1]), color=color, buff=buff, stroke_width=7)
    return box


def month_tags(row, size=30):
    tags = VGroup(MT("OCT", size, MC_GRAY).next_to(VGroup(*row[:5]), UP, buff=0.12),
                  MT("NOV", size, MC_GRAY).next_to(VGroup(*row[5:]), UP, buff=0.12))
    return tags


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    title = stone_title("DAYS TOGETHER", 60, width=7.8).move_to([0, 4.0, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.25, 2.75, 0])
    row = block_row(ROW, 0.95, size=0.74, gap=0.1)
    tags_m = month_tags(row, 28)
    pick = pickaxe(1.25).move_to([-1.3, -1.2, 0])
    clock = pixel_art("clock", 1.2).move_to([1.3, -1.2, 0])
    tags = VGroup(chat("LeetCode #2409", MC_AQUA, 46), chat("Easy", MC_GREEN, 46), chat("Math", MC_GOLD, 46))
    tags.arrange(RIGHT, buff=0.2)
    if tags.width > 8.4:
        tags.scale_to_fit_width(8.4)
    tags.move_to([0, -3.05, 0])
    # Over a 3D world the dirt strip is not needed; an empty group keeps the unpacking in Scene1_Hook
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, title, spl, row, tags_m, pick, clock, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, title, spl, row, tags_m, pick, clock, tags = art
        self.add(art)

        self.seg(0)
        self.beat(pulse(spl), rt=0.8)
        # Blocks hop one after another, like a wave
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.3) for b in row], lag_ratio=0.15), rt=1.6)
        self.sfx("stone_dig1", 0.35, delay=0.35)
        self.until(ph(0, "LeetCode"))
        self.sfx("click", 0.35)
        self.beat(Rotate(clock, angle=-20 * DEGREES, rate_func=there_and_back), *[pulse(row[k], 1.12) for k in range(S0, S1 + 1)], rt=0.8)
        self.until(ph(0, "a little"))
        self.beat(pulse(spl), Rotate(pick, angle=-30 * DEGREES, rate_func=there_and_back), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        who = VGroup(chat("Alice", MC_GOLD, 48), pixel_art("clock", 0.8), chat("Bob", MC_AQUA, 48)).arrange(RIGHT, buff=0.6)
        who.move_to([0, 3.5, 0])
        fmt = chat("MM-DD", MC_WHITE, 56)
        fmt.move_to([0, 2.0, 0])

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.sfx("pop", 0.3)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in who], lag_ratio=0.2), rt=0.7)
        self.until(ph(1, "month, dash"))
        self.sfx("book_flip1", 0.3)
        self.beat(FadeIn(fmt, scale=0.7), rt=0.5)
        self.close_seg()

        self.seg(2)
        row = block_row(ROW, 0.2, size=0.74, gap=0.1)
        tags_m = month_tags(row)
        al = chat("Alice  10-28  ->  11-03", MC_GOLD, 40)
        bo = chat("Bob  10-30  ->  11-05", MC_AQUA, 40)
        VGroup(al, bo).arrange(DOWN, buff=0.15).move_to([0, 2.0, 0])
        abox = stay_box(row, A0, A1, MC_GOLD, 0.07)
        bbox = stay_box(row, B0, B1, MC_AQUA, 0.17)
        self.beat(FadeOut(fmt), rt=0.3)
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(0, len(row), 2):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.28, delay=k * 0.1 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.1), FadeIn(tags_m), rt=1.3)
        self.until(ph(2, "Alice stays"))
        self.beat(FadeIn(al, shift=UP * 0.15), Create(abox), rt=0.6)
        self.until(ph(2, "Bob,"))
        self.beat(FadeIn(bo, shift=UP * 0.15), Create(bbox), rt=0.6)
        self.close_seg()

        self.seg(3)
        both = stay_box(row, S0, S1, MC_GREEN, 0.27)
        self.until(ph(3, "both"))
        self.beat(Create(both), *[pulse(row[k], 1.12) for k in range(S0, S1 + 1)], rt=0.6)
        ans = chat(f"return {ANSWER}", MC_GREEN, 60)
        ans.move_to([0, -2.0, 0])
        self.until(ph(3, "Here"))
        self.sfx("orb", 0.3)
        self.beat(FadeIn(ans, shift=UP * 0.2), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("BRUTE FORCE", MC_RED)
        a_doy, b_doy = WALK["alice_doy"], WALK["bob_doy"]
        # The whole calendar: one row per month, one square per day
        months = VGroup()
        d = 0
        for m, n in enumerate(DAYS):
            r = VGroup(*[Square(0.2, stroke_width=0, fill_color=MC_DGRAY, fill_opacity=0.9) for _ in range(n)]).arrange(RIGHT, buff=0.04)
            r.move_to([0, 3.6 - m * 0.3, 0], aligned_edge=UP).align_to([-3.6, 0, 0], LEFT)
            months.add(r)
        squares = [s for r in months for s in r]

        def color_of(doy):
            ina, inb = a_doy[0] <= doy <= a_doy[1], b_doy[0] <= doy <= b_doy[1]
            return MC_GREEN if ina and inb else MC_GOLD if ina else MC_AQUA if inb else MC_GRAY

        def counter(c, both):
            g = VGroup(chat(f"days checked {c}", MC_WHITE, 32, PIXEL), chat(f"both there {both}", MC_GREEN, 32, PIXEL))
            g.arrange(DOWN, buff=0.15).move_to([0, -0.9, 0])
            return g

        cnt = counter(0, 0)

        self.seg(4)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(ph(4, "whole calendar"))
        self.sfx("book_flip2", 0.3)
        self.beat(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in months], lag_ratio=0.08), FadeIn(cnt), rt=1.2)
        self.close_seg()

        # Month by month: every day is looked at, and the shared ones turn green
        self.seg(5)
        span = ph(5, "count the days") - 0.3
        rt = max(2 / 30, math.floor(span / len(DAYS) * 30) / 30)
        seen, both = 0, 0
        for m, r in enumerate(months):
            first = seen + 1
            seen += DAYS[m]
            both += sum(1 for doy in range(first, seen + 1) if color_of(doy) == MC_GREEN)
            if m % 2 == 0:
                self.sfx(f"stone_step{m % 6 + 1}", 0.22)
            self.beat(*[s.animate.set_fill(color_of(first + k)) for k, s in enumerate(r)], Transform(cnt, counter(seen, both)), rt=rt)
        greens = [s for k, s in enumerate(squares) if color_of(k + 1) == MC_GREEN]
        self.until(ph(5, "count the days"))
        self.sfx("orb", 0.3)
        self.beat(*[pulse(s, 1.6) for s in greens], rt=0.6)
        self.close_seg()

        self.seg(6)
        note = chat(f"365 checks  ->  {ANSWER} days", MC_RED, 44)
        note.move_to([0, -2.6, 0])
        self.until(ph(6, "every day"))
        self.sfx("villager_no1", 0.25)
        self.beat(FadeIn(note, shift=UP * 0.2), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        date = chat("10-28", MC_GOLD, 56)
        arrow = MT("->", 60, MC_GRAY)
        num = chat("day 301", MC_GOLD, 56)
        VGroup(date, arrow, num).arrange(RIGHT, buff=0.4).move_to([0, 3.4, 0])

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(date, shift=UP * 0.15), rt=0.5)
        self.until(ph(7, "day of the year", -0.3))
        self.sfx("pop", 0.35)
        self.beat(FadeIn(arrow), FadeIn(num, shift=LEFT * 0.2), rt=0.6)
        self.close_seg()

        self.seg(8)
        sums = MT("31+28+31+30+31+30+31+31+30", 34, MC_WHITE, PIXEL)
        if sums.width > 8.4:
            sums.scale_to_fit_width(8.4)
        tot = MT(f"= {WALK['before_oct']}", 40, MC_AQUA, PIXEL)
        plus = MT(f"{WALK['before_oct']} + 28 = 301", 40, MC_GOLD, PIXEL)
        VGroup(sums, tot, plus).arrange(DOWN, buff=0.25).move_to([0, 1.4, 0])
        self.until(ph(8, "Add up"))
        self.beat(FadeIn(sums, shift=UP * 0.15), rt=0.5)
        self.until(ph(8, "months before"))
        self.beat(FadeIn(tot, shift=UP * 0.15), rt=0.4)
        self.until(ph(8, "then add the day"))
        self.sfx("pop", 0.35)
        self.beat(FadeIn(plus, shift=UP * 0.15), pulse(num, 1.1), rt=0.5)
        self.close_seg()

        # Both stays on a number line; together they run from the later start to the earlier end
        self.seg(9)
        x = lambda v: (v - 305) * 0.6
        line = Line([x(298.5), -1.9, 0], [x(311.5), -1.9, 0], color=MC_GRAY, stroke_width=4)
        ticks = VGroup(*[MT(str(v), 22, MC_GRAY, PIXEL).move_to([x(v), -2.25, 0]) for v in range(299, 312, 2)])
        a_doy, b_doy = WALK["alice_doy"], WALK["bob_doy"]

        def bar(a, b, y, color):
            r = Rectangle(width=x(b) - x(a), height=0.26, stroke_width=0, fill_color=color, fill_opacity=1)
            r.move_to([(x(a) + x(b)) / 2, y, 0])
            return r

        ab, bb = bar(*a_doy, -0.9, MC_GOLD), bar(*b_doy, -1.35, MC_AQUA)
        al = MT("Alice", 30, MC_GOLD).next_to(ab, LEFT, buff=0.2)
        bl = MT("Bob", 30, MC_AQUA).next_to(bb, RIGHT, buff=0.2)
        self.beat(FadeOut(VGroup(sums, tot, plus)), rt=0.3)
        self.beat(Create(line), FadeIn(ticks), rt=0.4)
        self.until(ph(9, "range of numbers", -0.3))
        self.beat(GrowFromEdge(ab, LEFT), FadeIn(al), GrowFromEdge(bb, LEFT), FadeIn(bl), rt=0.6)
        ov = bar(WALK["start"], WALK["end"], -2.9, MC_GREEN)
        s_lab = chat(f"later start {WALK['start']}", MC_GREEN, 32)
        e_lab = chat(f"earlier end {WALK['end']}", MC_GREEN, 32)
        VGroup(s_lab, e_lab).arrange(RIGHT, buff=0.3).move_to([0, -3.7, 0])
        self.until(ph(9, "later arrival", -0.3))
        self.sfx("click", 0.3)
        self.beat(GrowFromEdge(ov, LEFT), FadeIn(s_lab, shift=UP * 0.1), rt=0.5)
        self.until(ph(9, "earlier departure", -0.3))
        self.sfx("click", 0.3)
        self.beat(FadeIn(e_lab, shift=UP * 0.1), pulse(ov, 1.08), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("DAY NUMBERS", MC_GREEN)
        code = code_panel(SOLVE_CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 4, 4, MC_YELLOW)
        st = {"ro": None, "lines": []}

        def show(*lines):
            # The readout under the 3D row: one chat box per line, replaced as the walk goes
            g = VGroup(*[chat(s, c, 38) for s, c in lines]).arrange(DOWN, buff=0.12)
            g.move_to([0, -1.15, 0])
            old = st["ro"]
            st["ro"] = g
            self.beat(*([FadeOut(old)] if old is not None else []), FadeIn(g, shift=UP * 0.15), rt=0.3)

        def move_bar(a, color=MC_YELLOW, rt=0.15):
            self.beat(Transform(bar, line_bar(code, a, a, color)), rt=rt)

        keys = ("months_t", "alice_in_doy", "alice_out_doy", "bob_in_doy", "bob_out_doy", "start_t", "end_t", "count_t",
                "five_t", "toast", "answer_t")
        ev = sorted([(seg_time(W["first"], W[k]), k, None) for k in keys], key=lambda e: e[0])
        ad, bd = W["alice_doy"], W["bob_doy"]

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(code, shift=UP * 0.3), rt=0.5)

        def on(kind, k):
            if kind == "months_t":
                self.sfx("wood_dig1", 0.35)
                self.beat(FadeIn(bar), rt=0.2)
                show((f"Jan - Sep = {W['before_oct']} days", MC_WHITE))
            elif kind == "alice_in_doy":
                self.sfx("pop", 0.35)
                show((f"Alice  {ad[0]}", MC_GOLD))
            elif kind == "alice_out_doy":
                self.sfx("pop", 0.35)
                show((f"Alice  {ad[0]} - {ad[1]}", MC_GOLD))
            elif kind == "bob_in_doy":
                self.sfx("pop", 0.35)
                show((f"Alice  {ad[0]} - {ad[1]}", MC_GOLD), (f"Bob  {bd[0]}", MC_AQUA))
            elif kind == "bob_out_doy":
                self.sfx("pop", 0.35)
                show((f"Alice  {ad[0]} - {ad[1]}", MC_GOLD), (f"Bob  {bd[0]} - {bd[1]}", MC_AQUA))
            elif kind == "start_t":
                self.sfx("click", 0.35)
                move_bar(5)
                show((f"start = max({ad[0]}, {bd[0]}) = {W['start']}", MC_GREEN))
            elif kind == "end_t":
                self.sfx("click", 0.35)
                move_bar(6)
                show((f"start = {W['start']}", MC_GREEN), (f"end = min({ad[1]}, {bd[1]}) = {W['end']}", MC_GREEN))
            elif kind == "count_t":
                move_bar(7)
                for j in range(ANSWER):
                    self.sfx("orb", 0.25, delay=0.22 * j)
            elif kind == "five_t":
                show((f"{W['end']} - {W['start']} + 1 = {ANSWER}", MC_GOLD))
            elif kind == "toast":
                t = toast("Advancement Made!", "Days counted", w=4.6)
                t.move_to([0, 5.5, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                self.beat(t.animate.shift(LEFT * 7), Transform(bar, line_bar(code, 7, 7, MC_GREEN)), rt=0.5)
            elif kind == "answer_t":
                # The answer takes the place of the readout: higher up it would cover the 3D row
                ans = chat(f"return {ANSWER}", MC_GREEN, 60)
                ans.move_to([0, -1.15, 0])
                self.beat(FadeOut(st["ro"]), FadeIn(ans, shift=UP * 0.2), rt=0.4)

        def on_last():
            # The 3D clip fades to the roam at its end; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        per = VGroup(pixel_art("clock", 0.7), MT("a few additions per date", 44, MC_WHITE))
        per.arrange(RIGHT, buff=0.35).move_to([0, 3.4, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(1)", 1.05)).arrange(RIGHT, buff=0.4)
        tm.move_to([0, 1.65, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.6, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(ph(16, "few additions", -0.3))
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in per], lag_ratio=0.25), rt=0.6)
        self.until(ph(16, "constant", -0.6))
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.35)
        self.add(xp)
        self.sfx("levelup", 0.3, delay=0.3)
        self.beat(Restore(xp), rt=0.5)
        self.close_seg()

        self.seg(17)
        few = MT("start, end, and the answer", 44, MC_WHITE)
        few.move_to([0, -1.4, 0])
        self.until(ph(17, "a few numbers", -0.3))
        self.sfx("click", 0.3)
        self.beat(FadeIn(few, shift=UP * 0.15), rt=0.4)
        sp = VGroup(MT("space", 56, MC_GRAY), MT("O(1)", 52, MC_GOLD, PIXEL)).arrange(RIGHT, buff=0.4)
        sp.move_to([0, -3.1, 0])
        self.until(ph(17, "constant", -0.6))
        self.sfx("pop", 0.35)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(SOLVE_CODE, 1.6, width=8.4)
        bar = line_bar(code, 2, 4, MC_YELLOW)

        self.seg(18)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(ph(18, "later start"))
        self.beat(Transform(bar, line_bar(code, 5, 5, MC_GOLD)), rt=0.3)
        self.until(ph(18, "earlier end"))
        self.beat(Transform(bar, line_bar(code, 6, 7, MC_GREEN)), rt=0.3)
        self.close_seg()

        self.seg(19)
        msg = chat("Dates -> numbers", MC_GOLD, 56)
        msg.move_to([0, -3.0, 0])
        self.until(ph(19, "turn them into numbers", -0.3))
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.5)
        # The lesson stays until the cover replaces it, so the screen is never empty; the cover is the first frame too
        self.finish(FadeOut(Group(code, bar, msg)), FadeIn(cover()), rt=1.0)
        self.close_seg()
