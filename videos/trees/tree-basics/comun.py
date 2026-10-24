# ---------------------------------------------------------------- shared by largo/ (16:9) and corto/ (9:16)
# The tree of the whole guide: 8 with 3 (1, 6) on its left and 10 on its right; 10 has only 14, and 14 only 13.
TREE = {8: (3, 10), 3: (1, 6), 10: (None, 14), 1: (None, None), 6: (None, None), 14: (13, None), 13: (None, None)}
ORE_OF.update({8: "diamond", 3: "iron", 10: "lapis", 1: "coal", 6: "redstone", 14: "gold", 13: "emerald"})
PRE = [8, 3, 1, 6, 10, 14, 13]
IN = [1, 3, 6, 8, 10, 13, 14]
POST = [1, 6, 3, 13, 14, 10, 8]
LEVELS = [[8], [3, 10], [1, 6, 14], [13]]
WOOD = "#9C7A48"
NULL_EDGE = "#5A2A2A"

TREE_SUM = """def tree_sum(node):
    if node is None:
        return 0
    left = tree_sum(node.left)
    right = tree_sum(node.right)
    return node.val + left + right"""


def tree_tokens(spread=(2.0, 1.0, 0.5, 0.32)):
    # Preorder with "#" for the empty children; every token has its x, level and parent token
    out = []

    def walk(v, x, lvl, parent):
        tok = {"x": x, "lvl": lvl, "parent": parent}
        out.append(tok)
        if v is None:
            tok["tok"] = "#"
            return
        tok.update({"tok": str(v), "value": v, "ore": ORE_OF[v]})
        me = len(out) - 1
        left, right = TREE[v]
        walk(left, x - spread[lvl], lvl + 1, me)
        walk(right, x + spread[lvl], lvl + 1, me)

    walk(8, 0.0, 0, None)
    return out


TOKS = tree_tokens()
SUB3 = [3, 1, 6]  # 3 and its children, cut off with the shears


def at(i, phrase, nth=0):
    # Seconds into line i where the nth `phrase` starts (even speaking rate inside a line)
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = -1
    for _ in range(nth + 1):
        k = text.find(phrase, k + 1)
    assert k >= 0, (i, phrase)
    return min(dur - 0.1, dur * k / len(text))


def words_at(i, words, start=""):
    # Seconds into line i where each word of `words` is said, searched one after another (after `start`)
    text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
    k = text.find(start) if start else 0
    out = []
    for w in words:
        k = text.find(w, k)
        assert k >= 0, (i, w)
        out.append(min(dur - 0.1, dur * k / len(text)))
        k += len(w)
    return out


class Tree2D(VGroup):
    """The tree as ore blocks joined by wooden rods; with nulls=True, barrier icons mark the empty children.
    blocks, edges and bars are keyed by value (blocks, edges to that value) or by token index (bars, null edges)."""

    def __init__(self, size, top, dy, sx, x0=0.0, nulls=False, only=None, **kwargs):
        super().__init__(**kwargs)
        toks = TOKS
        self.pos = [np.array([x0 + t["x"] * sx, top - t["lvl"] * dy, 0]) for t in toks]
        keep = (lambda t: True) if only is None else (lambda t: t.get("value") in only or (
            t["tok"] == "#" and toks[t["parent"]]["value"] in only))
        self.blocks, self.edges, self.bars, self.null_edges, self.at = {}, {}, {}, {}, {}
        for i, t in enumerate(toks):
            if t["parent"] is None or not keep(t) or (t["tok"] != "#" and not keep(toks[t["parent"]])):
                continue
            null = t["tok"] == "#"
            if null and not nulls:
                continue
            e = Line(self.pos[t["parent"]], self.pos[i], color=NULL_EDGE if null else WOOD,
                     stroke_width=(7 if null else 11) * size, stroke_opacity=0.8 if null else 1)
            (self.null_edges if null else self.edges)[i if null else t["value"]] = e
        for i, t in enumerate(toks):
            if not keep(t):
                continue
            if t["tok"] != "#":
                self.blocks[t["value"]] = Block(t["value"], f"{t['ore']}_ore", size).move_to(self.pos[i])
                self.at[t["value"]] = self.pos[i]
            elif nulls:
                self.bars[i] = pixel_art("barrier", size * 0.62).move_to(self.pos[i])
        self.rods = VGroup(*self.edges.values())
        self.null_rods = VGroup(*self.null_edges.values())
        self.add(self.rods, self.null_rods, VGroup(*self.blocks.values()), VGroup(*self.bars.values()))

    def block_list(self, order=PRE):
        return [self.blocks[v] for v in order if v in self.blocks]

    def bars_of(self, v):
        # The barriers under block v
        i = next(k for k, t in enumerate(TOKS) if t.get("value") == v)
        return [self.bars[k] for k in self.bars if TOKS[k]["parent"] == i]


def glyphs(s, size, color):
    # Game-font text inside an invisible box of its full line height, so pieces placed side by side share a baseline
    img = text_image(s, color)
    u = _px_unit(size, TERM)
    span = Rectangle(width=img.width * u, height=img.height * u, stroke_width=0, fill_opacity=0)
    return VGroup(span, pixel_image(img, img.width * u, img.height * u))


def pulse(m, k=1.15):
    # Emphasis that keeps the pixel art's colors (Indicate would paint it one flat color)
    return m.animate(rate_func=there_and_back).scale(k)


class TokenLine(VGroup):
    """A list of values in a chat box, one mobject per token (toks) plus the commas."""

    def __init__(self, tokens, size=44, color=MC_WHITE, opacity=0.55, label=None, label_color=MC_GOLD, **kwargs):
        super().__init__(**kwargs)
        parts, self.toks, self.commas = [], [], []
        if label:
            self.label = glyphs(label + "  ", size, label_color)
            parts.append(self.label)
        for k, t in enumerate(tokens):
            if k:
                c = glyphs(",", size, MC_GRAY)
                parts.append(c)
                self.commas.append(c)
            m = glyphs(str(t), size, MC_RED if t == "#" else color)
            parts.append(m)
            self.toks.append(m)
        self.row = VGroup(*parts).arrange(RIGHT, buff=0)
        self.box = Rectangle(width=self.row.width + 0.56, height=self.row.height + 0.28, fill_color="#000000",
                             fill_opacity=opacity, stroke_width=0)
        self.row.move_to(self.box)
        self.add(self.box, self.row)

    def upto(self, k):
        # Token k plus the comma before it
        return VGroup(self.toks[k], *([self.commas[k - 1]] if k else []))


def hdr(text, color, size=42):
    return chat(text, color, size).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def orb_num(value, color=MC_GREEN, size=40):
    # A value carried up a rod: the experience orb sprite with the number beside it
    orb = pixel_image(_gui("orb").crop((16, 16, 32, 32)), 0.55)
    num = MT(str(value), size, color, PIXEL)
    num.scale_to_fit_height(0.4)
    return VGroup(orb, num).arrange(RIGHT, buff=0.08)
