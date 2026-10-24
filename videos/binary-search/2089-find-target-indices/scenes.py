WALK = json.load(open('walk.json', encoding='utf-8'))
NUMS, TARGET, ANSWER = WALK["nums"], WALK["target"], WALK["answer"]
ORE_OF.update(dict(zip(NUMS, WALK["ores"])))
LESS, EQUAL = WALK["less"], WALK["equal"]

SORT_CODE = """def targetIndices(nums, target):
    nums.sort()
    return [i for i, x in enumerate(nums) if x == target]"""

COUNT_CODE = """def targetIndices(nums, target):
    less = equal = 0
    for x in nums:
        if x < target:
            less += 1
        elif x == target:
            equal += 1
    return list(range(less, less + equal))"""


def ph(i, phrase, shift=0.0):
    # Seconds into line i where `phrase` starts being spoken (even speaking rate inside a line)
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(phrase)
    assert k >= 0, (i, phrase)
    return max(0.0, min(dur - 0.25, dur * k / len(text) + shift))


def index_row(row, size=34, color=MC_GRAY, buff=0.14):
    return VGroup(*[MT(str(k), size, color).next_to(b, DOWN, buff=buff) for k, b in enumerate(row)])


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def pulse(m, s=1.15):
    # Pixel art is highlighted with a scale pulse; Indicate with a color paints it flat
    return m.animate(rate_func=there_and_back).scale(s)


def target_sign(scale=1.0):
    return sign(["target", str(TARGET)], 2.2, 1.35, 46).scale(scale)


def sort_anims(row):
    # Every block slides to its place in the sorted row (ties keep their order); order[s] is the block in slot s
    slots = [b.get_center() for b in row]
    order = sorted(range(len(slots)), key=lambda i: NUMS[i])
    return [row[i].animate(path_arc=-60 * DEGREES).move_to(slot) for slot, i in zip(slots, order)], order


def take(items, ks):
    # items[k] for each k that exists: the linter's stand-in groups are empty, so plain indexing would break it
    return [items[k] for k in ks if k < len(items)]


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    title = stone_title("TARGET INDICES", 60, width=7.8).move_to([0, 4.0, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.25, 2.75, 0])
    row = block_row(NUMS, 0.95, size=1.05, gap=0.18)
    idx = index_row(row)
    pick = pickaxe(1.25).move_to([-1.3, -1.2, 0])
    tsign = target_sign(0.6).move_to([1.3, -1.2, 0])
    tags = VGroup(chat("LeetCode #2089", MC_AQUA, 46), chat("Easy", MC_GREEN, 46), chat("Counting", MC_GOLD, 46))
    tags.arrange(RIGHT, buff=0.2)
    if tags.width > 8.4:
        tags.scale_to_fit_width(8.4)
    tags.move_to([0, -3.05, 0])
    ground = VGroup() if globals().get("FONDO") else ground_strip(-5.15)
    return VGroup(ground, title, spl, row, idx, pick, tsign, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        ground, title, spl, row, idx, pick, tsign, tags = art
        self.add(art)

        self.seg(0)
        self.beat(pulse(spl), rt=0.8)
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.35) for b in row], lag_ratio=0.18), rt=1.6)
        self.sfx("stone_dig1", 0.35, delay=0.35)
        self.until(ph(0, "LeetCode"))
        self.sfx("wood_dig1", 0.35)
        self.beat(pulse(tsign, 1.15), *[pulse(row[i], 1.12) for i, x in enumerate(NUMS) if x == TARGET], rt=0.8)
        self.until(ph(0, "and a sneaky"))
        self.beat(pulse(spl), Rotate(pick, angle=-30 * DEGREES, rate_func=there_and_back), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        row = block_row(NUMS, 2.2, size=1.05, gap=0.18)
        idx = index_row(row)
        lab = MT("nums", 40, MC_WHITE).next_to(row, UP, buff=0.2).align_to(row, LEFT)
        tsign = target_sign(0.8).move_to([0, 4.0, 0]).to_edge(RIGHT, buff=0.5)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(len(row)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.3, delay=k * 0.12 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.12), rt=1.6)
        self.beat(FadeIn(idx, shift=UP * 0.1), FadeIn(lab), rt=0.4)
        self.until(ph(1, "a target"))
        self.sfx("wood_dig1", 0.4)
        self.beat(FadeIn(tsign, scale=0.6), rt=0.5)
        self.close_seg()

        self.seg(2)
        q = chat("where would every 2 end up?", MC_GOLD, 42)
        q.move_to([0, 0.2, 0])
        self.until(ph(2, "where would"))
        self.beat(FadeIn(q, shift=UP * 0.15), *[pulse(row[i], 1.12) for i, x in enumerate(NUMS) if x == TARGET], rt=0.6)
        self.close_seg()

        self.seg(3)
        anims, order = sort_anims(row)
        self.until(ph(3, "Sorted"))
        self.sfx("stone_step1", 0.3, delay=0.3)
        self.beat(*anims, FadeOut(q), rt=0.9)
        frames = VGroup(*[outline(row[i], MC_GOLD, 8) for i in take(order, ANSWER)])
        ans = chat(f"return {ANSWER}", MC_GREEN, 56)
        ans.move_to([0, -0.4, 0])
        self.until(ph(3, "So the answer"))
        self.sfx("orb", 0.3)
        self.beat(Create(frames), FadeIn(ans, shift=UP * 0.2), *[pulse(m, 1.4) for m in take(idx, ANSWER)], rt=0.6)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("BRUTE FORCE", MC_RED)
        row = block_row(NUMS, 3.1, size=0.95, gap=0.18)
        idx = index_row(row, 30)
        code = code_panel(SORT_CODE, -3.6, max_h=2.0)
        pick = pickaxe(1.0).move_to([-2.9, 1.2, 0])

        self.seg(4)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(row), FadeIn(idx), rt=0.6)
        self.until(ph(4, "sort the whole row"))
        self.beat(FadeIn(code, shift=UP * 0.3), FadeIn(pick, scale=0.6), rt=0.5)
        bar = line_bar(code, 1, 1, MC_YELLOW)
        anims, order = sort_anims(row)
        self.sfx("stone_step2", 0.3, delay=0.3)
        self.beat(FadeIn(bar), *anims, rt=0.9)
        self.until(ph(4, "scan it"))
        self.beat(Transform(bar, line_bar(code, 2, 2, MC_YELLOW)), rt=0.3)
        self.close_seg()

        self.seg(5)
        extra = [row[i] for i in take(order, (4, 5))]
        self.until(ph(5, "even the three"))
        self.sfx("villager_no1", 0.25)
        self.beat(*[pulse(b, 1.18) for b in extra], *[Create(outline(b, MC_RED, 7)) for b in extra], rt=0.7)
        nn = chat("never needed in order", MC_RED, 40)
        nn.move_to([1.0, 1.2, 0])
        self.until(ph(5, "never needed"))
        self.beat(FadeIn(nn, shift=UP * 0.15), rt=0.4)
        self.close_seg()

        self.seg(6)
        o = MT("O(n log n)", 52, MC_RED, PIXEL)
        o.move_to([0, -0.6, 0])
        self.until(ph(6, "n log n", -0.3))
        self.beat(FadeIn(o, scale=0.6), rt=0.5)
        two = chat("but we only need 2 counts", MC_GOLD, 40)
        two.move_to([0, -1.7, 0])
        self.until(ph(6, "two counts", -0.5))
        self.beat(FadeIn(two, shift=UP * 0.15), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        srt = sorted(NUMS)
        row = block_row(srt, 2.4, size=1.05, gap=0.18)
        idx = index_row(row)
        small = Brace(VGroup(*take(row, range(LESS))) if len(row) else row, UP, color=MC_AQUA)
        small_l = MT("smaller", 34, MC_AQUA).next_to(small, UP, buff=0.1)
        tgt = Brace(VGroup(*take(row, range(LESS, LESS + EQUAL))) if len(row) else row, UP, color=MC_GOLD)
        tgt_l = MT("the 2s", 34, MC_GOLD).next_to(tgt, UP, buff=0.1)

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(row), FadeIn(idx), rt=0.6)
        self.until(ph(7, "every block smaller"))
        self.beat(GrowFromCenter(small), FadeIn(small_l), *[pulse(m, 1.12) for m in take(row, range(LESS))], rt=0.6)
        self.close_seg()

        self.seg(8)
        self.until(ph(8, "start right after"))
        self.beat(GrowFromCenter(tgt), FadeIn(tgt_l), rt=0.5)
        st = chat(f"first 2 at index less = {LESS}", MC_AQUA, 40)
        st.move_to([0, 0.3, 0])
        self.until(ph(8, "With one smaller"))
        self.sfx("pop", 0.35)
        self.beat(FadeIn(st, shift=UP * 0.15), *[pulse(m, 1.5) for m in take(idx, [LESS])], rt=0.5)
        self.close_seg()

        self.seg(9)
        ln = chat(f"then equal = {EQUAL} slots", MC_GOLD, 40)
        ln.move_to([0, -0.7, 0])
        self.until(ph(9, "three twos"))
        self.sfx("pop", 0.35)
        self.beat(FadeIn(ln, shift=UP * 0.15), *[pulse(m, 1.4) for m in take(idx, range(LESS, LESS + EQUAL))], rt=0.6)
        rng = chat(f"range({LESS}, {LESS} + {EQUAL})", MC_GREEN, 48)
        rng.move_to([0, -2.0, 0])
        self.until(ph(9, "from there", -0.6))
        self.beat(FadeIn(rng, shift=UP * 0.15), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("COUNT ONLY", MC_GREEN)
        tsign = target_sign(0.6)
        tsign.move_to([0, TOP_Y - 0.05, 0]).to_edge(RIGHT, buff=0.4)
        code = code_panel(COUNT_CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 1, 1, MC_YELLOW)
        st = {"ro": None}

        def show(text, color=MC_WHITE):
            g = chat(text, color, 44)
            g.move_to([0, -1.15, 0])
            old = st["ro"]
            st["ro"] = g
            self.beat(*([FadeOut(old)] if old is not None else []), FadeIn(g, shift=UP * 0.15), rt=0.3)

        def move_bar(a, color=MC_YELLOW, rt=0.15):
            self.beat(Transform(bar, line_bar(code, a, a, color)), rt=rt)

        ev = [(seg_time(W["first"], W[k]), k, None) for k in ("counters", "place_less", "place_equal", "toast", "answer_t")]
        for j, s in enumerate(W["steps"]):
            ev += [(seg_time(W["first"], s["visit"]), "visit", j), (seg_time(W["first"], s["count"]), "count", j)]
        ev.sort(key=lambda e: e[0])

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(tsign), FadeIn(code, shift=UP * 0.3), rt=0.5)

        def on(kind, j):
            if kind == "counters":
                self.beat(FadeIn(bar), rt=0.2)
                show("less 0   equal 0")
            elif kind == "visit":
                move_bar(2)
            elif kind == "count":
                s = W["steps"][j]
                if s["kind"] == "bigger":
                    self.sfx("villager_no2", 0.2)
                    move_bar(5, MC_RED)
                    return
                self.sfx("pop", 0.35, delay=0.4)
                move_bar(4 if s["kind"] == "less" else 6, MC_GREEN)
                show(f"less {s['less']}   equal {s['equal']}")
            elif kind == "place_less":
                self.sfx("stone_step1", 0.3, delay=0.4)
                move_bar(7)
                show(f"start at less = {LESS}", MC_AQUA)
            elif kind == "place_equal":
                for d in (0.4, 0.55, 0.7):
                    self.sfx("stone_step2", 0.28, delay=d)
                show(f"range({LESS}, {LESS} + {EQUAL})", MC_GOLD)
            elif kind == "toast":
                t = toast("Advancement Made!", "No sort needed", w=4.6)
                t.move_to([0, 5.5, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(tsign), Transform(bar, line_bar(code, 7, 7, MC_GREEN)), rt=0.5)
            elif kind == "answer_t":
                for d in (0.0, 0.2, 0.4):
                    self.sfx("orb", 0.28, delay=d)
                ans = chat(f"return {ANSWER}", MC_GREEN, 56)
                ans.move_to([0, -1.15, 0])
                self.beat(FadeOut(st["ro"]), FadeIn(ans, shift=UP * 0.2), rt=0.4)

        def on_last():
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        per = MT("one pass, two counters", 46, MC_WHITE)
        per.move_to([0, 3.4, 0])
        tm = VGroup(MT("time", 56, MC_GRAY), level_text("O(n)", 1.05)).arrange(RIGHT, buff=0.4)
        tm.move_to([0, 1.65, 0])
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 0.6, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), FadeIn(per, shift=UP * 0.15), rt=0.5)
        self.until(ph(16, "linear", -0.5))
        self.beat(FadeIn(tm, shift=UP * 0.2), FadeIn(bg), rt=0.35)
        self.add(xp)
        self.sfx("levelup", 0.3, delay=0.3)
        self.beat(Restore(xp), rt=0.5)
        self.close_seg()

        self.seg(17)
        two = MT("less and equal", 44, MC_WHITE)
        two.move_to([0, -1.4, 0])
        self.until(ph(17, "two numbers", -0.3))
        self.sfx("click", 0.3)
        self.beat(FadeIn(two, shift=UP * 0.15), rt=0.4)
        sp = VGroup(MT("space", 56, MC_GRAY), MT("O(1)", 52, MC_GOLD, PIXEL)).arrange(RIGHT, buff=0.4)
        sp.move_to([0, -3.1, 0])
        self.until(ph(17, "Constant", -0.4))
        self.sfx("pop", 0.35)
        self.beat(FadeIn(sp, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(COUNT_CODE, 1.6, width=8.4)
        bar = line_bar(code, 3, 4, MC_YELLOW)

        self.seg(18)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.beat(FadeIn(bar), rt=0.25)
        self.until(ph(18, "count the matches"))
        self.beat(Transform(bar, line_bar(code, 5, 6, MC_GOLD)), rt=0.3)
        self.until(ph(18, "read off the range"))
        self.beat(Transform(bar, line_bar(code, 7, 7, MC_GREEN)), rt=0.3)
        self.close_seg()

        self.seg(19)
        msg = chat("Counts, not order", MC_GOLD, 56)
        msg.move_to([0, -3.0, 0])
        self.until(ph(19, "you don't need"))
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.5)
        # The lesson stays until the cover replaces it, so the screen is never empty; the cover is the first frame too
        self.finish(FadeOut(Group(code, bar, msg)), FadeIn(cover()), rt=1.0)
        self.close_seg()
