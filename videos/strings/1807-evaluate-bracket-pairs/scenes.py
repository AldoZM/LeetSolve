WALK = json.load(open('walk.json', encoding='utf-8'))
PIECES, KNOW, ANSWER = WALK["pieces"], WALK["knowledge"], WALK["answer"]
# Values are ores; a key shows on the ore of its value
ORE_OF.update({v: v for _, v in KNOW})
ORE_OF.update({k: v for k, v in KNOW})
# Inventory icons with the game's proportions (the template's are flatter)
ISO_SIDE, ISO_FILL = 0.61, 0.88

BRUTE_CODE = """def lookup(key, knowledge):
    for k, v in knowledge:
        if k == key:
            return v
    return "?\""""

HASH_CODE = """def evaluate(s, knowledge):
    chest = dict(knowledge)
    parts = s.split("(")
    out = [parts[0]]
    for part in parts[1:]:
        key, rest = part.split(")")
        out.append(chest.get(key, "?") + rest)
    return "".join(out)"""


def hdr(text, color):
    return chat(text, color, 42).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def eq_line(parts, size=34, font=PIXEL, buff=0.3):
    return VGroup(*[MT(s, size, c, font) for s, c in parts]).arrange(RIGHT, buff=buff)


def piece_row(y, size=1.0, word=44, buff=0.22):
    # The string as the video shows it: a cobblestone block per bracket, plain words between them
    row = VGroup(*[Block(f"({p['text']})", "cobble", size) if p["kind"] == "key" else MT(p["text"], word, MC_WHITE)
                   for p in PIECES]).arrange(RIGHT, buff=buff)
    row.move_to([0, y, 0])
    return row


def key_blocks(row):
    return [row[k] for k, p in enumerate(PIECES) if p["kind"] == "key"]


def value_block(value, like, size=1.0):
    # What a bracket turns into: its ore with the value on it, or cobblestone with a red question mark
    if value == "?":
        b = Block("?", "cobble", size)
        q = MT("?", 40, MC_RED, PIXEL)
        q.scale_to_fit_height(size * 0.42)
        q.move_to(b.num)
        b.remove(b.num)
        b.num = q
        b.add(q)
    else:
        b = Block(value, f"{ORE_OF[value]}_ore", size)
    b.move_to(like)
    return b


def know_row(y, size=0.9, x=0.0, buff=0.3):
    # The knowledge list: each key on the ore of its value, the value's name under it
    blocks = VGroup(*[Block(k, f"{ORE_OF[v]}_ore", size) for k, v in KNOW]).arrange(RIGHT, buff=buff)
    blocks.move_to([x, y, 0])
    names = VGroup(*[MT(v, 34, MC_GRAY).next_to(b, DOWN, buff=0.12) for b, (_, v) in zip(blocks, KNOW)])
    return blocks, names


def cover():
    # The first and the last frame of the video: both ends draw exactly this
    title = stone_title("BRACKET PAIRS", 60, width=7.8).move_to([0, 4.0, 0])
    spl = splash("Minecraft edition!", 21).move_to([2.25, 2.75, 0])
    row = piece_row(0.95)
    ans = MT(f'"{ANSWER}"', 40, MC_GOLD)
    ans.move_to([0, -0.35, 0])
    pick = pickaxe(1.15).move_to([-1.3, -1.75, 0])
    chest = chest_icon(1.05).move_to([1.3, -1.75, 0])
    tags = VGroup(chat("LeetCode #1807", MC_AQUA, 40), chat("Medium", MC_YELLOW, 40), chat("Hash Map", MC_GOLD, 40))
    tags.arrange(RIGHT, buff=0.2).move_to([0, -3.4, 0])
    if tags.width > 8.4:
        tags.scale_to_fit_width(8.4)
    return VGroup(title, spl, row, ans, pick, chest, tags)


class Scene1_Hook(Base):
    def construct(self):
        art = cover()
        title, spl, row, ans, pick, chest, tags = art
        self.add(art)

        self.seg(0)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        # The pieces hop one after another, like a wave
        self.beat(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.35) for b in row], lag_ratio=0.18), rt=1.6)
        self.sfx("stone_dig1", 0.35, delay=0.35)
        keys = key_blocks(row)
        self.beat(*[ShowPassingFlash(outline(b, MC_GOLD, 10), time_width=0.6) for b in keys],
                  *[b.animate(rate_func=there_and_back).scale(1.12) for b in keys],
                  Rotate(pick, angle=-30 * DEGREES, rate_func=there_and_back), rt=0.9)
        self.beat(Indicate(ans, color=MC_YELLOW, scale_factor=1.08), rt=0.8)
        self.beat(spl.animate(rate_func=there_and_back).scale(1.15), rt=0.8)
        self.clear_all(rt=0.5)
        self.close_seg()


class Scene2_Problem(Base):
    def construct(self):
        h = hdr("THE PROBLEM", MC_AQUA)
        row = piece_row(2.7)
        lab = MT("s", 40, MC_WHITE).next_to(row, UP, buff=0.25).align_to(row, LEFT)
        kb, kn = know_row(0.0, 0.85)
        klab = MT("knowledge", 40, MC_WHITE).next_to(kb, UP, buff=0.25)
        keys = key_blocks(row)

        self.seg(1)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        # The pieces fall from the sky and bounce into place
        for b in row:
            b.shift(UP * 8)
        self.add(row)
        for k in range(len(row)):
            self.sfx(f"stone_dig{k % 4 + 1}", 0.3, delay=k * 0.12 + 0.36)
        self.beat(LaggedStart(*[b.animate(rate_func=rate_functions.ease_out_bounce).shift(DOWN * 8) for b in row],
                              lag_ratio=0.12), rt=1.5)
        self.beat(FadeIn(lab), *[ShowPassingFlash(outline(b, MC_YELLOW, 8), time_width=0.6) for b in keys], rt=0.5)
        self.until(3.1)
        self.sfx("wood_dig1", 0.35)
        self.beat(FadeIn(klab, shift=UP * 0.1), LaggedStart(*[FadeIn(b, scale=0.6) for b in kb], lag_ratio=0.2),
                  FadeIn(kn), rt=0.8)
        self.close_seg()

        self.seg(2)
        self.until(0.4)
        # Known keys become their values
        new = [value_block(v, b) for b, v in zip(keys, ["iron", "gold"])]
        self.sfx("pop", 0.35)
        self.beat(*[Transform(b, n) for b, n in zip(keys[:2], new)],
                  Indicate(kb[0], color=MC_YELLOW), Indicate(kb[1], color=MC_YELLOW), rt=0.6)
        self.until(3.0)
        miss = outline(keys[2], MC_RED, 8)
        self.beat(Create(miss), rt=0.4)
        self.until(4.6)
        self.sfx("click", 0.35)
        self.beat(Transform(keys[2], value_block("?", keys[2])), FadeOut(miss), rt=0.5)
        ret = chat(f'"{ANSWER}"', MC_GREEN, 52)
        ret.move_to([0, -2.6, 0])
        self.until(5.0)
        self.beat(FadeIn(ret, shift=UP * 0.2), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene3_Brute(Base):
    def construct(self):
        h = hdr("BRUTE FORCE", MC_RED)
        row = piece_row(3.0, 0.95, 40)
        keys = key_blocks(row)
        kb, kn = know_row(1.0, 0.85, x=-2.0, buff=0.25)
        code = code_panel(BRUTE_CODE, -3.7, max_h=2.9)
        pick = pickaxe(0.95).move_to([1.15, 1.15, 0])
        dbg = Rectangle(width=1.2, height=0.16, fill_color="#000000", fill_opacity=1, stroke_width=0)
        dbg.next_to(pick, DOWN, buff=0.15)

        def dfill(frac):
            # Durability bar: shrinks and turns from green to red
            r = Rectangle(width=max(1.16 * frac, 0.02), height=0.1, stroke_width=0, fill_opacity=1,
                          fill_color=interpolate_color(ManimColor(MC_RED), ManimColor(MC_GREEN), frac))
            r.move_to(dbg.get_left() + RIGHT * (0.02 + max(1.16 * frac, 0.02) / 2))
            return r

        def counter(k):
            c = MT(f"checks {k}", 30, MC_WHITE, PIXEL)
            c.move_to([3.0, 1.15, 0])
            return c

        fill, cnt = dfill(1.0), counter(0)
        st = {"n": 0}

        self.seg(3)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in row], lag_ratio=0.1), rt=0.9)
        self.beat(LaggedStart(*[FadeIn(b, scale=0.6) for b in kb], lag_ratio=0.15), FadeIn(kn), rt=0.6)
        self.until(1.9)
        self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
        self.until(3.0)
        self.beat(FadeIn(pick, scale=0.6), FadeIn(dbg), FadeIn(fill), FadeIn(cnt), rt=0.5)
        self.close_seg()

        oi = outline(keys[0], MC_YELLOW, 7)
        oj = outline(kb[0], MC_WHITE, 6)
        bar = line_bar(code, 1, 1, MC_YELLOW)

        def check(j, hit, rt):
            # One comparison of the key against knowledge entry j; the pickaxe hits halfway through its swing
            st["n"] += 1
            nf, nc = dfill(1 - st["n"] / 8), counter(st["n"])
            color = MC_GREEN if hit else MC_WHITE
            self.sfx(f"stone_dig{st['n'] % 4 + 1}", 0.22, delay=rt * 0.5)
            self.beat(oj.animate.move_to(kb[j]).set_stroke(color), Transform(fill, nf), Transform(cnt, nc),
                      Transform(bar, line_bar(code, 2, 2, MC_YELLOW)), Rotate(pick, angle=-25 * DEGREES, rate_func=there_and_back),
                      rt=rt)
            if hit:
                self.sfx("orb", 0.3)
                self.beat(Transform(bar, line_bar(code, 3, 3, MC_GREEN)), Indicate(kn[j], color=MC_GREEN), rt=0.3)

        self.seg(4)
        self.until(0.15)
        self.beat(Create(oi), FadeIn(bar), FadeIn(oj), rt=0.35)
        self.until(0.6)
        check(0, True, 0.4)
        self.until(2.4)
        self.beat(oi.animate.move_to(keys[1]), oj.animate.move_to(kb[0]).set_stroke(MC_WHITE),
                  Transform(bar, line_bar(code, 1, 1, MC_YELLOW)), rt=0.3)
        check(0, False, 0.35)
        check(1, True, 0.35)
        self.until(3.75)
        self.beat(oi.animate.move_to(keys[2]), oj.animate.move_to(kb[0]).set_stroke(MC_WHITE),
                  Transform(bar, line_bar(code, 1, 1, MC_YELLOW)), rt=0.25)
        for j in range(3):
            check(j, False, 0.3)
        self.until(5.7)
        q = MT("?", 50, MC_RED, PIXEL).next_to(keys[2], DOWN, buff=0.12)
        self.sfx("click", 0.35)
        self.beat(oi.animate.set_stroke(MC_RED), oj.animate.set_stroke(MC_RED), Transform(bar, line_bar(code, 4, 4, MC_RED)),
                  FadeIn(q, shift=UP * 0.1), rt=0.4)
        self.close_seg()

        self.seg(5)
        self.until(0.2)
        self.beat(Indicate(cnt, color=MC_RED, scale_factor=1.3), rt=0.7)
        self.until(2.3)
        # Every bracket walks the whole list
        for b in keys:
            self.sfx("stone_step2", 0.25)
            self.beat(ShowPassingFlash(outline(b, MC_RED, 9), time_width=0.6),
                      ShowPassingFlash(outline(kb, MC_RED, 9), time_width=0.6), rt=0.45)
        self.sfx("break", 0.35)
        self.beat(Wiggle(pick), rt=0.6)
        self.close_seg()

        self.seg(6)
        self.beat(FadeOut(VGroup(row, kb, kn, oi, oj, code, bar, pick, dbg, fill, cnt, q)), rt=0.5)
        n = eq_line([("30,000", MC_WHITE), ("x", MC_GRAY), ("100,000", MC_WHITE)], 32)
        n.move_to([0, 2.6, 0])
        self.beat(FadeIn(n, shift=UP * 0.2), rt=0.5)
        big = MT("3,000,000,000", 40, MC_RED, PIXEL)
        big.move_to([0, 1.0, 0])
        pl = MT("checks", 52, MC_GRAY)
        pl.next_to(big, DOWN, buff=0.25)
        self.until(3.0)
        self.beat(FadeIn(big, scale=1.4), FadeIn(pl), rt=0.6)
        o = MT("O(n*k)", 72, MC_RED, PIXEL)
        o.move_to([0, -1.9, 0])
        self.until(3.9)
        self.beat(FadeIn(o, scale=0.5), rt=0.5)
        self.clear_all()
        self.close_seg()


class Scene4_Idea(Base):
    def construct(self):
        h = hdr("THE TRICK", MC_GOLD)
        kb, kn = know_row(2.6, 0.9)
        inv = Inventory(9, "Chest")
        inv.move_to([0, 0.0, 0])
        items = [inv.item(k, key, "") for k, (key, _) in enumerate(KNOW)]
        title2 = inv.title_for("Chest = hash map")

        self.seg(7)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), LaggedStart(*[FadeIn(b, scale=0.6) for b in kb], lag_ratio=0.15),
                  FadeIn(kn), rt=0.8)
        self.until(1.3)
        self.sfx("wood_dig2", 0.35)
        self.beat(FadeIn(inv, shift=UP * 0.3), rt=0.5)
        self.until(2.7)
        self.sfx("chestopen", 0.3)
        for k in range(len(KNOW)):
            self.sfx("pop", 0.32, delay=0.35 + 0.3 * k)
        self.sfx("chestclosed", 0.25, delay=1.4)
        self.beat(LaggedStart(*[Transform(b, it) for b, it in zip(kb, items)], lag_ratio=0.25), FadeOut(kn), rt=1.2)
        self.close_seg()

        self.seg(8)
        self.until(0.2)
        self.beat(Transform(inv.title, title2), rt=0.4)
        ask = MT('chest["b"]', 56, MC_WHITE)
        arrow = MT("->", 56, MC_GRAY)
        icon = iso_block("gold_ore", 0.7)
        gold = MT("gold", 56, MC_GOLD)
        line = VGroup(ask, arrow, icon, gold).arrange(RIGHT, buff=0.3)
        line.move_to([0, -2.2, 0])
        self.until(1.7)
        self.beat(FadeIn(ask, shift=UP * 0.15), Create(outline(inv.slots[1], MC_YELLOW, 8, buff=0.02)), rt=0.4)
        self.until(3.0)
        self.sfx("pop", 0.38)
        self.beat(FadeIn(arrow), FadeIn(icon, scale=0.5), FadeIn(gold, shift=LEFT * 0.2), rt=0.5)
        o = MT("O(1)", 60, MC_GREEN, PIXEL)
        o.move_to([0, -3.7, 0])
        self.until(4.4)
        self.sfx("orb", 0.3)
        self.beat(FadeIn(o, scale=0.5), rt=0.4)
        self.clear_all()
        self.close_seg()


class Scene5_Walk(Overlay):
    def construct(self):
        W = WALK
        h = hdr("ONE PASS", MC_GREEN)
        inv = Inventory(9, "Chest = hash map")
        inv.move_to([0, -1.15, 0])
        items = VGroup(*[inv.item(k, key, "") for k, (key, _) in enumerate(KNOW)])
        slot_of = {key: k for k, (key, _) in enumerate(KNOW)}
        code = code_panel(HASH_CODE, -4.3, max_h=3.25)
        bar = line_bar(code, 4, 4, MC_YELLOW)
        st = {"out": None}

        ev = [(seg_time(W["first"], W[key]), key, None) for key in ("intro_row", "chest_in", "demo_key", "demo_ask", "toast", "answer_t")]
        for k, s in enumerate(W["steps"]):
            for kind in ("visit", "key_t", "ask", "hit", "miss", "write", "copy"):
                if kind in s:
                    ev.append((seg_time(W["first"], s[kind]), kind, k))
        ev.sort(key=lambda e: e[0])

        def move_bar(k0, k1=None, color=MC_YELLOW, rt=0.15):
            self.beat(Transform(bar, line_bar(code, k0, k1, color)), rt=rt)

        def show_out(text, rt=0.2):
            # The answer being built, high in the frame above the 3D row
            new = chat(f'out = "{text}"', MC_WHITE, 40)
            new.move_to([0, 4.55, 0]).to_edge(LEFT, buff=0.4)
            if st["out"] is None:
                st["out"] = new
                self.beat(FadeIn(new, shift=UP * 0.1), rt=rt)
            else:
                self.beat(Transform(st["out"], new), rt=rt)

        def on_first():
            self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.35)

        def on(kind, k):
            s = W["steps"][k] if k is not None else None
            if kind == "intro_row":
                self.beat(FadeIn(code, shift=UP * 0.3), rt=0.6)
            elif kind == "chest_in":
                self.sfx("wood_dig2", 0.4)
                self.sfx("chestopen", 0.28, delay=0.25)
                for j in range(len(KNOW)):
                    self.sfx("pop", 0.3, delay=0.45 + 0.25 * j)
                self.sfx("chestclosed", 0.22, delay=1.45)
                self.beat(FadeIn(inv, shift=UP * 0.3), Transform(bar, line_bar(code, 1, 1, MC_YELLOW)), rt=0.5)
                self.beat(LaggedStart(*[FadeIn(it, scale=1.6) for it in items], lag_ratio=0.3), rt=0.8)
            elif kind == "demo_key":
                move_bar(4, 5, rt=0.3)
            elif kind == "demo_ask":
                self.sfx("chestopen", 0.3)
                self.sfx("chestclosed", 0.25, delay=1.0)
                move_bar(6, rt=0.3)
            elif kind == "visit":
                move_bar(4)
            elif kind == "key_t":
                move_bar(5)
            elif kind == "ask":
                self.sfx("chestopen", 0.28)
                move_bar(6)
            elif kind == "hit":
                fr = outline(inv.slots[slot_of[s["key"]]], MC_GOLD, 8, buff=0.02)
                for d in (0.0, 0.18):
                    self.sfx("orb", 0.28, delay=d)
                self.beat(Transform(bar, line_bar(code, 6, 6, MC_GREEN)), ShowPassingFlash(fr, time_width=0.8), rt=0.3)
            elif kind == "miss":
                self.sfx("click", 0.35)
                self.beat(Transform(bar, line_bar(code, 6, 6, MC_RED)),
                          *[ShowPassingFlash(outline(sl, MC_RED, 7, buff=0.02), time_width=0.8) for sl in inv.slots[:len(KNOW)]],
                          rt=0.35)
            elif kind == "write":
                self.sfx("pop", 0.35)
                self.sfx("chestclosed", 0.22, delay=0.1)
                show_out(s["out_value"])
            elif kind == "copy":
                self.sfx("pop", 0.3)
                show_out(s["out_rest"])
            elif kind == "toast":
                t = toast("Advancement Made!", "Bracket Pairs solved")
                t.move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.3)
                t.shift(RIGHT * 7)
                self.sfx("challenge", 0.32)
                self.beat(t.animate.shift(LEFT * 7), FadeOut(h), Transform(bar, line_bar(code, 7, 7, MC_GREEN)), rt=0.5)
            elif kind == "answer_t":
                ans = chat(f'return "{ANSWER}"', MC_GREEN, 44)
                ans.move_to([0, 4.55, 0])
                self.beat(FadeOut(st["out"]), FadeIn(ans, shift=UP * 0.2), rt=0.4)

        def on_last():
            # The 3D walk ends with its last line; the overlay leaves with it
            self.finish(FadeOut(Group(*self.mobjects)), rt=0.5)

        self.run_events(W, ev, on, on_first=on_first, on_last=on_last)


class Scene6_Complexity(Base):
    def construct(self):
        h = hdr("COMPLEXITY", MC_AQUA)
        look = VGroup(chest_icon(0.9), MT("lookup", 52, MC_WHITE), MT("O(1)", 40, MC_GREEN, PIXEL))
        look.arrange(RIGHT, buff=0.35).move_to([0, 3.4, 0])
        once = VGroup(MT("string once", 44, MC_WHITE), MT("n", 36, MC_AQUA, PIXEL), MT("+", 36, MC_GRAY, PIXEL),
                      MT("list once", 44, MC_WHITE), MT("k", 36, MC_GOLD, PIXEL))
        once.arrange(RIGHT, buff=0.3).move_to([0, 1.9, 0])
        # The game's experience bar fills up as the walk reads everything once
        bg, fill = xp_bar(7.4)
        bg.move_to([0, 1.0, 0])
        xp = fill(1.0)
        xp.save_state()
        xp.stretch(0.01, 0, about_edge=LEFT)

        self.seg(16)
        self.beat(FadeIn(h, shift=RIGHT * 0.3), rt=0.4)
        self.until(0.5)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in look], lag_ratio=0.25), rt=0.8)
        self.until(2.1)
        self.beat(FadeIn(once[:2], shift=UP * 0.15), FadeIn(bg), rt=0.4)
        self.add(xp)
        for d in (0.0, 0.4, 0.8, 1.2):
            self.sfx("orb", 0.25, delay=d)
        self.beat(Restore(xp), FadeIn(once[2:], shift=UP * 0.15, lag_ratio=0.3), rt=1.6)
        self.close_seg()

        self.seg(17)
        old = MT("O(n*k)", 44, MC_RED, PIXEL)
        arrow = MT("->", 70, MC_GRAY)
        new = level_text("O(n+k)", 0.9)
        cmp = VGroup(old, arrow, new).arrange(RIGHT, buff=0.45)
        cmp.move_to([0, -0.8, 0])
        tl = MT("time", 52, MC_GRAY).next_to(cmp, UP, buff=0.3)
        strike = Line(old.get_left() + LEFT * 0.1, old.get_right() + RIGHT * 0.1, color=MC_RED, stroke_width=8)
        self.until(0.2)
        self.beat(FadeIn(tl), FadeIn(old, shift=UP * 0.15), rt=0.4)
        self.until(1.0)
        self.sfx("levelup", 0.3)
        self.beat(Create(strike), FadeIn(arrow), FadeIn(new, shift=LEFT * 0.2), rt=0.6)
        mem = VGroup(chest_icon(0.85), MT("memory", 52, MC_WHITE), MT("O(k)", 40, MC_GOLD, PIXEL))
        mem.arrange(RIGHT, buff=0.35).move_to([0, -3.1, 0])
        self.until(2.4)
        self.beat(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in mem], lag_ratio=0.2), rt=0.7)
        self.clear_all()
        self.close_seg()


class Scene7_Outro(Base):
    def construct(self):
        code = code_panel(HASH_CODE, 1.6, width=8.4)
        bar = line_bar(code, 1, 1, MC_GOLD)
        icon = chest_icon(0.55)

        self.seg(18)
        self.beat(FadeIn(code.background),
                  LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in code.code_lines], lag_ratio=0.08), FadeIn(code.line_numbers),
                  rt=0.7)
        self.until(0.8)
        icon.next_to(code.code_lines[1], RIGHT, buff=0.4)
        self.beat(FadeIn(bar), FadeIn(icon, scale=0.5), rt=0.35)
        self.until(1.6)
        self.beat(Transform(bar, line_bar(code, 4, 6, MC_YELLOW)), rt=0.4)
        self.until(2.6)
        self.beat(Transform(bar, line_bar(code, 0, 7, MC_GREEN)), rt=0.4)
        self.close_seg()

        self.seg(19)
        msg = chat("Look it up, don't search", MC_GOLD, 56)
        msg.move_to([0, -2.6, 0])
        if msg.width > 8.4:
            msg.scale_to_fit_width(8.4)
        self.until(0.1)
        self.beat(FadeIn(msg, shift=UP * 0.2), rt=0.5)
        self.until(2.1)
        self.beat(FadeOut(Group(code, bar, icon, msg)), rt=0.5)
        # Ends on the cover, so the last frame matches the first one
        self.finish(FadeIn(cover()), rt=1.0)
        self.close_seg()
