from manim import *
import math
import os
import random
import json

FPS = 30
config.pixel_width, config.pixel_height = 1080, 1440
config.frame_width, config.frame_height = 9, 12
config.frame_rate = FPS

# Palette shared with the three.js scenes (herramientas/three/stage.js)
BG = "#0B0E1A"
PANEL = "#141B2F"
CODE_BG = "#11162A"
CYAN = "#22D3EE"
MAGENTA = "#F472B6"
YELLOW = "#FACC15"
GREEN = "#34D399"
RED = "#F87171"
VIOLET = "#A78BFA"
ORANGE = "#FB923C"
MUTED = "#64748B"
INK = "#E2E8F0"
ARROW = "#8291AD"

TOP_Y = 5.4

# Narration lines and their exact durations (from the TTS step)
SUBS = json.load(open('timestamps.json', encoding='utf-8'))['subtitles']
DUR = [x['duration_s'] for x in SUBS]


def T(s, size=36, color=INK, weight=BOLD):
    return Text(s, font="Segoe UI", weight=weight, font_size=size, color=color)


def M(s, size=36, color=INK):
    return Text(s, font="Consolas", weight=BOLD, font_size=size, color=color)


def glow(m, color, layers=8, max_w=26, max_op=0.30):
    # Stacked translucent strokes behind a shape fake a neon bloom
    g = VGroup()
    for k in range(layers):
        frac = (k + 1) / layers
        g.add(m.copy().set_fill(opacity=0).set_stroke(color, width=max_w * frac, opacity=max_op * (1 - frac) + 0.02))
    return g


def ring(m, color, width=8):
    # Light that travels around a shape's border without touching its fill
    return ShowPassingFlash(m.copy().set_fill(opacity=0).set_stroke(color, width=width), time_width=0.5)


def restyle(m, fn):
    # Animate the whole group while changing only part of it; animating just the box lets Manim draw it over the text
    return ApplyFunction(lambda x: (fn(x), x)[1], m)


def pill(text, color, size=24):
    label = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.2, width=label.width + 0.5, height=label.height + 0.3,
                           fill_color=color, fill_opacity=0.12, stroke_color=color, stroke_width=2)
    return VGroup(box, label.move_to(box))


def header(text, color):
    return pill(text, color, 22).move_to([0, TOP_Y, 0]).to_edge(LEFT, buff=0.4)


def corner_pill(text, color, size=26):
    return pill(text, color, size).move_to([0, TOP_Y, 0]).to_edge(RIGHT, buff=0.4)


def tags_block(items, y=-3.7):
    # items: [(text, color), ...]; first two on one row, the rest below
    first = VGroup(*[pill(t, c, 26) for t, c in items[:2]]).arrange(RIGHT, buff=0.3)
    rest = VGroup(*[pill(t, c, 26) for t, c in items[2:]]).arrange(RIGHT, buff=0.3)
    return VGroup(first, rest).arrange(DOWN, buff=0.25).move_to([0, y, 0])


def dot_grid():
    return VGroup(*[Dot([x, y, 0], radius=0.016, color=MUTED, fill_opacity=0.35)
                    for x in np.arange(-4.2, 4.3, 0.6) for y in np.arange(-5.7, 5.8, 0.6)])


def gradient_title(lines, size=96, y=3.35, colors=(CYAN, VIOLET, MAGENTA)):
    title = VGroup(*[T(s, size) for s in lines]).arrange(DOWN, buff=0.08)
    title.set_color_by_gradient(*colors).move_to([0, y, 0])
    return title, glow(title, colors[1], layers=6, max_w=20, max_op=0.25)


class Tile(VGroup):
    """Rounded square holding one value; `box` and `num` are animated through restyle()."""

    def __init__(self, value, color, size=0.95, text_color=INK, **kwargs):
        super().__init__(**kwargs)
        self.box = RoundedRectangle(corner_radius=0.14 * size / 0.95, width=size, height=size, fill_color=PANEL,
                                    fill_opacity=1, stroke_color=color, stroke_width=3)
        self.num = M(str(value), int(38 * size / 0.95), text_color).move_to(self.box)
        self.add(self.box, self.num)


def tile_row(values, color, y, size=0.8, gap=0.12, x=0.0, text_color=INK):
    row = VGroup(*[Tile(v, color, size, text_color) for v in values]).arrange(RIGHT, buff=gap)
    row.move_to([x, y, 0])
    return row  # returned separately so the linter stub keeps the children


def index_labels(row, size=18, color=MUTED, buff=0.12, start=0):
    return VGroup(*[M(str(start + k), size, color).next_to(t, DOWN, buff=buff) for k, t in enumerate(row)])


def code_panel(src, y, width=8.4, max_h=None):
    code = Code(code_string=src, language="python", formatter_style="monokai", background="rectangle",
                background_config={"fill_color": CODE_BG, "stroke_color": VIOLET, "stroke_width": 2},
                paragraph_config={"font": "Consolas"})
    code.scale_to_fit_width(width)
    if max_h and code.height > max_h:
        code.scale_to_fit_height(max_h)
    return code.move_to([0, y, 0])


def line_bar(code, k0, k1=None, color=YELLOW):
    k1 = k0 if k1 is None else k1
    lines = code.code_lines
    step = abs(lines[1].get_y() - lines[0].get_y())
    top, bottom = lines[k0].get_y() + step / 2, lines[k1].get_y() - step / 2
    bar = Rectangle(width=code.background.width - 0.12, height=(top - bottom) * 0.97, fill_color=color, fill_opacity=0.16,
                    stroke_color=color, stroke_width=1.5)
    return bar.move_to([code.background.get_x(), (top + bottom) / 2, 0])


def big_o(tex, color, y, label, size=80):
    o = MathTex(tex, font_size=size, color=color).move_to([0, y, 0])
    lab = T(label, 30, MUTED).next_to(o, DOWN, buff=0.15)
    return o, lab, glow(o, color, layers=6, max_w=14, max_op=0.3)


class Base(Scene):
    scene_budget = 0.0
    scene_used = 0.0
    seg_begin = 0.0

    def setup(self):
        self.camera.background_color = BG
        self.add(dot_grid())

    # Manim renders whole frames; keep animations on frame boundaries so audio stays in sync
    def frames(self, t):
        return math.ceil(t * FPS - 1e-6) / FPS

    def seg(self, i):
        text, dur = SUBS[i]['text'], SUBS[i]['duration_s']
        self.add_subcaption(text, duration=dur)
        self.seg_begin = self.scene_budget
        self.scene_budget += dur
        self.seg_index = i

    def sfx(self, name, gain=0.5, delay=0.0):
        # Queues a sound effect at the current time; build.py mixes media/sfx/<Scene>.json into the final audio
        t = SUBS[self.seg_index]['start_s'] + (self.scene_used - self.seg_begin) + delay
        cues = self.__dict__.get('sfx_cues', [])  # not getattr: the linter's scene stub invents missing attributes
        cues.append([round(t, 3), name, gain])
        self.sfx_cues = cues
        os.makedirs('media/sfx', exist_ok=True)
        with open(f'media/sfx/{type(self).__name__}.json', 'w') as f:
            json.dump(cues, f)

    def beat(self, *anims, rt=1.0, **kwargs):
        rt = self.frames(rt)
        self.play(*anims, run_time=rt, **kwargs)
        self.scene_used += rt

    def hold(self, t):
        t = self.frames(t)
        self.wait(t)
        self.scene_used += t

    def until(self, u):
        # Wait until u seconds into the current narration segment
        gap = self.seg_begin + u - self.scene_used
        if gap > 1e-6:
            self.hold(gap)

    def close_seg(self):
        rest = self.scene_budget - self.scene_used
        if rest > 0:
            self.wait(rest)
            self.scene_used += rest

    def finish(self, *anims, rt=0.5):
        # Play so the animation ends right at the close of the current segment
        rt = self.frames(rt)
        self.until(self.scene_budget - self.seg_begin - rt - 1.0 / FPS)
        self.beat(*anims, rt=rt)

    def clear_all(self, rt=0.5):
        self.finish(FadeOut(Group(*self.mobjects[1:])), rt=rt)


def seg_time(first, spec):
    # [segment index, seconds into it] -> seconds since the start of segment `first`
    return sum(DUR[first:spec[0]]) + spec[1]


def walk_events(walk, kinds):
    # walk.json is shared with three/walk.html; each step lists [segment, seconds] per event kind
    ev = []
    for k, st in enumerate(walk["steps"]):
        for kind in kinds:
            if kind in st:
                ev.append((seg_time(walk["first"], st[kind]), kind, k))
    return sorted(ev, key=lambda e: e[0])


class Overlay(Base):
    """Transparent layer composited over a three.js clip (rendered with -t)."""

    def setup(self):
        pass

    def run_events(self, walk, events, handler, on_first=None, on_last=None):
        # Plays each narration segment of the walk, firing handler(kind, step) at the shared event times
        first, last = walk["first"], walk["last"]
        ei = 0
        for i in range(first, last + 1):
            self.seg(i)
            s0 = seg_time(first, [i, 0])
            if i == first and on_first:
                on_first()
            while ei < len(events) and events[ei][0] < s0 + DUR[i] - 0.05:
                t, kind, k = events[ei]
                ei += 1
                self.until(t - s0)
                handler(kind, k)
            if i == last and on_last:
                on_last()
            self.close_seg()

# ---------------------------------------------------------------- video-specific code below

TEMA_DIR = 'C:/Users/aldo-/OneDrive/Documentos/CodigoAbierto/LeetSolve/herramientas/temas/minecraft'
# ---------------------------------------------------------------- Minecraft theme (herramientas/temas/minecraft)
# Appended after prelude.py when video.json has "tema": "minecraft". TEMA_DIR is set by build.py.
# Original procedural pixel art (textures.py) and OFL pixel fonts; no game assets are used.
import manimpango
from PIL import Image as PILImage
from pygments.style import Style as PygStyle
from pygments.token import Token, Keyword, Name, Number, String, Operator, Comment, Punctuation

for _font in ("PressStart2P-Regular.ttf", "VT323-Regular.ttf"):
    manimpango.register_font(f"{TEMA_DIR}/fonts/{_font}")

PIXEL = "Press Start 2P"  # titles, numbers on blocks
TERM = "VT323"            # body text and code

# Text colors in the game's chat palette
MC_WHITE = "#FFFFFF"
MC_GRAY = "#AAAAAA"
MC_DGRAY = "#555555"
MC_YELLOW = "#FFFF55"
MC_GOLD = "#FFAA00"
MC_GREEN = "#55FF55"
MC_AQUA = "#55FFFF"
MC_RED = "#FF5555"
MC_PINK = "#FF55FF"
GUI_TITLE = "#404040"

SKY_TOP = "#4A7FE0"
SKY_BOTTOM = "#A6C8F8"

ORE_OF = {}  # value -> ore name, filled per video


def shadow_color(color):
    # Text shadows are the same color at a quarter of the brightness
    return rgb_to_color(color_to_rgb(color) * 0.25)


_FONT_PX = {}


def font_px(font, size):
    # Height of one pixel of a pixel font at this size: "M" is 7 font pixels tall in Press Start 2P, 10 in VT323
    key = (font, size)
    if key not in _FONT_PX:
        _FONT_PX[key] = Text("M", font=font, font_size=size).height / (7 if font == PIXEL else 10)
    return _FONT_PX[key]


def MT(s, size=40, color=MC_WHITE, font=TERM, shadow=True):
    t = Text(s, font=font, font_size=size, color=color)
    if not shadow:
        return t
    d = font_px(font, size)
    sh = t.copy().set_color(shadow_color(color)).shift([d, -d, 0])
    return VGroup(sh, t)


# ---------- pixel art ----------
_PX = {}


def _load(name):
    if name not in _PX:
        _PX[name] = PILImage.open(f"{TEMA_DIR}/tex/{name}.png").convert("RGBA")
    return _PX[name]


def pixel_image(img, w, h=None):
    # One VMobject per color, made of merged horizontal runs; a base rectangle hides hairline seams
    h = w if h is None else h
    iw, ih = img.size
    px, py = w / iw, h / ih
    eps = 0.04
    runs, total, count = {}, np.zeros(3), 0
    for y in range(ih):
        x = 0
        while x < iw:
            c = img.getpixel((x, y))
            x2 = x
            while x2 + 1 < iw and img.getpixel((x2 + 1, y)) == c:
                x2 += 1
            if c[3] > 0:
                runs.setdefault(c[:3], []).append((x, x2 + 1, y))
                total += np.array(c[:3]) * (x2 + 1 - x)
                count += x2 + 1 - x
            x = x2 + 1
    g = VGroup()
    if count == iw * ih:
        g.add(Rectangle(width=w, height=h, fill_color=rgb_to_color(total / count / 255), fill_opacity=1, stroke_width=0))
    for c, rs in runs.items():
        vm = VMobject(fill_color=rgb_to_color([v / 255 for v in c]), fill_opacity=1, stroke_width=0)
        for x0, x1, y in rs:
            a, b = -w / 2 + x0 * px, -w / 2 + (x1 + eps) * px
            t, u = h / 2 - y * py, h / 2 - (y + 1 + eps) * py
            vm.start_new_path([a, t, 0])
            vm.add_points_as_corners([[b, t, 0], [b, u, 0], [a, u, 0], [a, t, 0]])
        g.add(vm)
    return g


def pixel_art(name, w, h=None):
    return pixel_image(_load(name), w, h)


def pixel_map(rows, colors, w):
    # rows: strings of equal length; colors: char -> hex ('.' is transparent)
    img = PILImage.new("RGBA", (len(rows[0]), len(rows)), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in colors:
                img.putpixel((x, y), tuple(int(colors[ch][i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    return pixel_image(img, w, w * len(rows) / len(rows[0]))


def _pickaxe_rows():
    g = [["."] * 16 for _ in range(16)]
    # Head: a thick arc bulging toward the upper right
    for y in range(16):
        for x in range(16):
            r = math.hypot(x - 3.5, y - 11.5)
            ang = math.degrees(math.atan2(11.5 - y, x - 3.5))
            if 7.6 <= r <= 9.6 and -8 <= ang <= 98:
                g[y][x] = "h" if r < 8.6 else "H"
            elif 6.9 <= r < 7.6 and -8 <= ang <= 98:
                g[y][x] = "k"
    # Handle: a diagonal stick from the bottom left into the head
    for k in range(9):
        x, y = 1 + k, 14 - k
        g[y][x] = "w"
        if x + 1 < 16:
            g[y][x + 1] = "W"
    return ["".join(r) for r in g]


PICKAXE = _pickaxe_rows()
PICKAXE_COLORS = {"h": "#5FE8F0", "H": "#2BA7B0", "k": "#16585C", "w": "#8A6236", "W": "#5A3E1E"}


def pickaxe(w=1.2):
    return pixel_map(PICKAXE, PICKAXE_COLORS, w)


# ---------- blocks and GUI ----------
class Block(VGroup):
    """A textured block with its value printed on it; `art`, `edge` and `num` are its parts."""

    def __init__(self, value, tex, size=1.0, num_h=0.3, **kwargs):
        super().__init__(**kwargs)
        self.art = pixel_art(tex, size)
        self.edge = Square(size, stroke_color="#000000", stroke_width=3, stroke_opacity=0.55, fill_opacity=0)
        self.num = MT(str(value), 40, MC_WHITE, PIXEL)
        self.num.scale_to_fit_height(size * num_h)
        if self.num.width > size * 0.8:
            self.num.scale_to_fit_width(size * 0.8)
        self.add(self.art, self.edge, self.num)


def block_row(values, y, size=1.0, gap=0.25, x=0.0, num_h=0.3):
    row = VGroup(*[Block(v, f"{ORE_OF[v]}_ore", size, num_h) for v in values]).arrange(RIGHT, buff=gap)
    row.move_to([x, y, 0])
    return row  # returned separately so the linter stub keeps the children


def outline(m, color=MC_WHITE, width=6, buff=0.06):
    return Square(m.width + 2 * buff, stroke_color=color, stroke_width=width, fill_opacity=0).move_to(m)


def chat(text, color=MC_WHITE, size=40, font=TERM, pad=(0.28, 0.14), opacity=0.55):
    # Dark translucent box, like the in-game chat
    t = MT(text, size, color, font)
    box = Rectangle(width=t.width + 2 * pad[0], height=t.height + 2 * pad[1], fill_color="#000000", fill_opacity=opacity,
                    stroke_width=0)
    return VGroup(box, t.move_to(box))


def bevel(w, h, fill, light, dark, t=0.05, outer=None):
    # Raised (light top-left, dark bottom-right) or sunken box, built from flat rectangles
    g = VGroup(Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_width=0))
    g.add(Rectangle(width=w, height=t, fill_color=light, fill_opacity=1, stroke_width=0).move_to([0, h / 2 - t / 2, 0]))
    g.add(Rectangle(width=t, height=h, fill_color=light, fill_opacity=1, stroke_width=0).move_to([-w / 2 + t / 2, 0, 0]))
    g.add(Rectangle(width=w, height=t, fill_color=dark, fill_opacity=1, stroke_width=0).move_to([0, -h / 2 + t / 2, 0]))
    g.add(Rectangle(width=t, height=h, fill_color=dark, fill_opacity=1, stroke_width=0).move_to([w / 2 - t / 2, 0, 0]))
    if outer:
        g.add(Rectangle(width=w + 0.04, height=h + 0.04, stroke_color=outer, stroke_width=3, fill_opacity=0))
    return g


def gui_panel(w, h):
    return bevel(w, h, "#C6C6C6", "#FFFFFF", "#555555", 0.07, outer="#000000")


def slot(s=0.9):
    return bevel(s, s, "#8B8B8B", "#373737", "#FFFFFF", 0.05)


class Inventory(VGroup):
    """A chest GUI with one row of slots; item(k, value, count) builds the stack shown in slot k."""

    def __init__(self, n, title="Chest", s=0.9, gap=0.04, **kwargs):
        super().__init__(**kwargs)
        self.s = s
        self.slots = VGroup(*[slot(s) for _ in range(n)]).arrange(RIGHT, buff=gap)
        self.title = MT(title, 38, GUI_TITLE, TERM, shadow=False)
        w = self.slots.width + 0.5
        h = self.slots.height + self.title.height + 0.55
        self.panel = gui_panel(w, h)
        self.slots.move_to(self.panel).shift(DOWN * (self.title.height + 0.1) / 2 + DOWN * 0.04)
        self.title.next_to(self.slots, UP, buff=0.12).align_to(self.slots, LEFT)
        self.add(self.panel, self.slots, self.title)

    def item(self, k, value, count, count_color=MC_WHITE):
        b = Block(value, f"{ORE_OF[value]}_ore", self.s * 0.72, num_h=0.34)
        b.move_to(self.slots[k])
        c = MT(str(count), 36, count_color, TERM)
        c.move_to(self.slots[k].get_corner(DR) + np.array([-0.15, 0.17, 0]))
        return VGroup(b, c)


class Hotbar(VGroup):
    def __init__(self, n=9, s=0.82, **kwargs):
        super().__init__(**kwargs)
        self.s = s
        self.slots = VGroup(*[Square(s, fill_color="#000000", fill_opacity=0.45, stroke_color="#8B8B8B", stroke_width=4)
                              for _ in range(n)]).arrange(RIGHT, buff=0)
        self.add(self.slots)

    def selector(self, k):
        return Square(self.s * 1.12, stroke_color=MC_WHITE, stroke_width=8, fill_opacity=0).move_to(self.slots[k])


def sign(lines, w=3.0, h=1.4, size=44):
    board = pixel_art("planks", w, h)
    edge = Rectangle(width=w, height=h, stroke_color="#3b2410", stroke_width=4, fill_opacity=0)
    txt = VGroup(*[Text(s, font=TERM, font_size=size, color="#000000") for s in lines]).arrange(DOWN, buff=0.08)
    return VGroup(board, edge, txt.move_to(board))


def toast(title, sub, icon_tex="gold_block", w=5.6):
    box = Rectangle(width=w, height=1.25, fill_color="#212121", fill_opacity=0.96, stroke_color="#A0A0A0", stroke_width=4)
    icon = pixel_art(icon_tex, 0.72).move_to(box.get_left() + RIGHT * 0.62)
    t1 = MT(title, 40, MC_YELLOW, TERM)
    t2 = MT(sub, 40, MC_WHITE, TERM)
    txt = VGroup(t1, t2).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(icon, RIGHT, buff=0.35)
    return VGroup(box, icon, txt)


def big_o_pow(inner, exp, size=44, color=MC_RED):
    # "O(n²)" built from parts: the pixel font has no usable superscript digits
    base = MT(f"O({inner}", size, color, PIXEL)
    sup = MT(str(exp), int(size * 0.55), color, PIXEL)
    close = MT(")", size, color, PIXEL)
    sup.next_to(base, RIGHT, buff=size * 0.0025).align_to(base, UP).shift(UP * size * 0.002)
    close.next_to(sup, RIGHT, buff=size * 0.0025).align_to(base, DOWN)
    return VGroup(base, sup, close)


def splash(text, size=30):
    # Yellow tilted splash text that pulses
    return MT(text, size, MC_YELLOW, PIXEL).rotate(18 * DEGREES)


def stone_title(text, size=88, depth=3, width=None):
    # Light stone letters over a stack of dark copies one font pixel apart: a cheap extruded look
    face = Text(text, font=PIXEL, font_size=size)
    face.set_color_by_gradient("#FFFFFF", "#B9B9B9")
    step = font_px(PIXEL, size)
    ext = VGroup(*[Text(text, font=PIXEL, font_size=size, color="#3A3A3A" if k == depth else "#5C5C5C")
                   .shift([k * step * 0.5, -k * step, 0]) for k in range(depth, 0, -1)])
    g = VGroup(ext, face)
    if width:
        g.scale_to_fit_width(width)
    return g


def ground_strip(y, n=11, s=0.9):
    tops = VGroup(*[pixel_art("grass_side", s) for _ in range(n)]).arrange(RIGHT, buff=0)
    below = VGroup(*[pixel_art("dirt", s) for _ in range(n)]).arrange(RIGHT, buff=0)
    g = VGroup(tops, below).arrange(DOWN, buff=0)
    g.move_to([0, y, 0])
    return g


def sky():
    # Banded sky gradient plus a few blocky clouds
    bands = 28
    H = config.frame_height
    g = VGroup()
    for k in range(bands):
        c = interpolate_color(ManimColor(SKY_TOP), ManimColor(SKY_BOTTOM), k / (bands - 1))
        g.add(Rectangle(width=config.frame_width + 0.1, height=H / bands + 0.01, fill_color=c, fill_opacity=1,
                        stroke_width=0).move_to([0, H / 2 - (k + 0.5) * H / bands, 0]))
    for cx, cy, w in [(-3.3, 5.6, 2.0), (3.6, 5.45, 1.5), (-3.8, -1.9, 1.4), (3.8, -4.15, 1.7)]:
        cloud = VGroup(Rectangle(width=w, height=0.36), Rectangle(width=w * 0.55, height=0.3).shift([w * 0.1, 0.3, 0]))
        cloud.set_fill("#FFFFFF", 0.8).set_stroke(width=0).move_to([cx, cy, 0])
        g.add(cloud)
    return g


def _mc_setup(self):
    # With a 3D world behind every scene (video.json "fondo"), scenes render transparent and add no sky
    if globals().get("FONDO"):
        self.add(VMobject())  # placeholder: clear_all() keeps the first mobject
        return
    self.camera.background_color = SKY_BOTTOM
    self.add(sky())


Base.setup = _mc_setup


class MCCodeStyle(PygStyle):
    background_color = "#000000"
    styles = {
        Token: "#FFFFFF",
        Keyword: "#FFAA00",
        Name.Builtin: "#55FFFF",
        Name.Function: "#55FF55",
        Number: "#FF55FF",
        String: "#FFFF55",
        Operator: "#AAAAAA",
        Punctuation: "#AAAAAA",
        Comment: "#AAAAAA",
    }


def code_panel(src, y, width=8.4, max_h=None):
    code = Code(code_string=src, language="python", formatter_style=MCCodeStyle, background="rectangle",
                background_config={"fill_color": "#000000", "fill_opacity": 0.82, "stroke_color": "#000000",
                                   "stroke_width": 0},
                paragraph_config={"font": TERM})
    code.scale_to_fit_width(width)
    if max_h and code.height > max_h:
        code.scale_to_fit_height(max_h)
    return code.move_to([0, y, 0])

TEMA_DIR = 'C:/Users/aldo-/OneDrive/Documentos/CodigoAbierto/LeetSolve/herramientas/temas/minecraft-original'
# extends: minecraft
# ---------------------------------------------------------------- Minecraft theme with the game's own assets
# Run extraer.py first: it copies textures, GUI sprites, the bitmap font and sounds from the local install.
# build.py puts the original-art theme (../minecraft/tema.py) first; this file replaces its art, text and GUI.
from pygments.lexers import PythonLexer
from PIL import ImageEnhance

SKY_TOP = "#6B98F5"
SKY_BOTTOM = "#B8D2FF"
MC_YELLOW = "#FFFF55"


def _gui(name):
    return PILImage.open(f"{TEMA_DIR}/gui/{name}.png").convert("RGBA")


# ---------- bitmap font (font/ascii.png from the game) ----------
_FONT = {}


def _font():
    if not _FONT:
        sheet = PILImage.open(f"{TEMA_DIR}/font/ascii.png").convert("RGBA")
        meta = json.load(open(f"{TEMA_DIR}/font/ascii.json", encoding="utf-8"))
        cell = sheet.width // 16
        for r, row in enumerate(meta["chars"]):
            for c, ch in enumerate(row):
                if ch == "\u0000":
                    continue
                g = sheet.crop((c * cell, r * cell, (c + 1) * cell, (r + 1) * cell))
                cols = [x for x in range(cell) if any(g.getpixel((x, y))[3] for y in range(cell))]
                width = (max(cols) + 1) if cols else 3
                _FONT[ch] = (g, width)
        _FONT[" "] = (PILImage.new("RGBA", (cell, cell)), 3)
    return _FONT


def _rgb(color):
    h = str(color).lstrip("#")[:6]
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def text_image(s, color, shadow=True):
    # One line of text at native size; glyph advance = width + 1, shadow one pixel down-right at 1/4 brightness
    f = _font()
    glyphs = [f.get(ch, f["?"]) for ch in s]
    w = sum(gw + 1 for _, gw in glyphs) + 1
    img = PILImage.new("RGBA", (max(w, 1), 9), (0, 0, 0, 0))
    col = _rgb(color)
    sh = tuple(v // 4 for v in col)

    def paint(g, rgb):
        solid = PILImage.new("RGBA", g.size, rgb + (255,))
        solid.putalpha(g.getchannel("A"))
        return solid

    x = 0
    for g, gw in glyphs:
        if shadow:
            img.alpha_composite(paint(g, sh), (x + 1, 1))
        img.alpha_composite(paint(g, col), (x, 0))
        x += gw + 1
    return img


def _px_unit(size, font):
    # Units per font pixel, sized like the TTF fonts the original-art theme used
    return size * (0.0016 if font == PIXEL else 0.00098)


def gui_text(s, color, u, shadow=True):
    # Text at the scale of a GUI sprite: one font pixel = u
    img = text_image(s, color, shadow)
    return pixel_image(img, img.width * u, img.height * u)


def MT(s, size=40, color=MC_WHITE, font=TERM, shadow=True):
    img = text_image(s, color, shadow)
    u = _px_unit(size, font)
    g = pixel_image(img, img.width * u, img.height * u)
    return g


def stone_title(text, size=88, depth=1, width=None):
    # Big game-font letters: light-to-gray face over dark extruded copies
    f = _font()
    glyphs = [f.get(ch, f["?"]) for ch in text]
    w = sum(gw + 1 for _, gw in glyphs) + depth + 1
    img = PILImage.new("RGBA", (w, 8 + depth + 1), (0, 0, 0, 0))
    x = 0
    for g, gw in glyphs:
        a = g.getchannel("A")
        for k in range(depth, 0, -1):
            layer = PILImage.new("RGBA", g.size, (58, 58, 58, 255) if k == depth else (92, 92, 92, 255))
            layer.putalpha(a)
            img.alpha_composite(layer, (x + k, k))
        face = PILImage.new("RGBA", g.size)
        for y in range(g.height):
            v = int(255 - 95 * y / 7)
            for xx in range(g.width):
                if a.getpixel((xx, y)):
                    face.putpixel((xx, y), (v, v, v, 255))
        img.alpha_composite(face, (x, 0))
        x += gw + 1
    u = (width / img.width) if width else _px_unit(size, PIXEL)
    return pixel_image(img, img.width * u, img.height * u)


def big_o_pow(inner, exp, size=44, color=MC_RED):
    # The game font has a superscript two
    return MT(f"O({inner}{'²' if exp == 2 else '^' + str(exp)})", size, color, PIXEL)


def splash(text, size=30):
    return MT(text, size, MC_YELLOW, PIXEL).rotate(20 * DEGREES)


def pickaxe(w=1.2):
    return pixel_image(_gui("pickaxe"), w)


# ---------- inventory icons ----------
# Side height of the icon over its width, and how much of a slot an inventory item fills. The game's icon (orthographic,
# tilted 30 degrees) has sides of about 0.61 and fills about 14 of 16 pixels; 0.5 and 1.0 keep the template's look
ISO_SIDE = 0.5
ISO_FILL = 1.0


def iso_block(tex, w=0.6, side=None):
    # The inventory look: top, left and right faces in a 2:1 isometric view with the game's face shading
    img = _load(tex)
    faces = VGroup()
    L, B, R, F = np.array([-w / 2, w / 4, 0]), np.array([0, w / 2, 0]), np.array([w / 2, w / 4, 0]), np.array([0, 0, 0])
    down = np.array([0, -w * (ISO_SIDE if side is None else side), 0])
    for e1, e2, center, light in [
        (F - L, B - L, (L + R) / 2, 1.0),
        (F - L, -down, (L + F) / 2 + down / 2, 0.8),
        (R - F, -down, (F + R) / 2 + down / 2, 0.62),
    ]:
        art = pixel_image(ImageEnhance.Brightness(img).enhance(light), 1)
        art.apply_matrix([[e1[0], e2[0], 0], [e1[1], e2[1], 0], [0, 0, 1]], about_point=ORIGIN)
        faces.add(art.shift(center))
    return faces.move_to(ORIGIN)


class Block(VGroup):
    """A flat textured block with its value printed on it; `art`, `edge` and `num` are its parts."""

    def __init__(self, value, tex, size=1.0, num_h=0.42, **kwargs):
        super().__init__(**kwargs)
        self.art = pixel_art(tex, size)
        self.edge = Square(size, stroke_color="#000000", stroke_width=3, stroke_opacity=0.6, fill_opacity=0)
        self.num = MT(str(value), 40, MC_WHITE, PIXEL)
        self.num.scale_to_fit_height(size * num_h)
        if self.num.width > size * 0.86:
            self.num.scale_to_fit_width(size * 0.86)
        self.add(self.art, self.edge, self.num)


def block_row(values, y, size=1.0, gap=0.25, x=0.0, num_h=0.42):
    row = VGroup(*[Block(v, f"{ORE_OF[v]}_ore", size, num_h) for v in values]).arrange(RIGHT, buff=gap)
    row.move_to([x, y, 0])
    return row


def item_stack(value, count, slot_w, count_color=MC_YELLOW):
    # Inventory item: isometric block with its value in white on it; the stack count (bottom-right, like the game) is the index
    u = slot_w / 18
    icon = iso_block(f"{ORE_OF[value]}_ore", 16 * u * ISO_FILL)
    val = gui_text(str(value), MC_WHITE, u * 1.15)
    val.move_to(icon).shift(UP * 2 * u)
    cnt = gui_text(str(count), count_color, u)
    cnt.move_to(icon.get_corner(DR) + np.array([2 * u, -1 * u, 0]), aligned_edge=DR)
    return VGroup(icon, val, cnt)


class Inventory(VGroup):
    """The game's chest screen cut to one row of 9 slots. item(k, value, count) builds the stack shown in slot k."""

    def __init__(self, n=9, title="Chest", width=8.6, **kwargs):
        super().__init__(**kwargs)
        gui = _gui("generic_54")
        # Header with the first row of slots, plus the bottom border of the screen
        top, bottom = gui.crop((0, 0, 176, 35)), gui.crop((0, 215, 176, 222))
        img = PILImage.new("RGBA", (176, 42))
        img.alpha_composite(top, (0, 0))
        img.alpha_composite(bottom, (0, 35))
        u = width / 176
        self.u = u
        self.s = 18 * u
        self.panel = pixel_image(img, width, 42 * u)
        x0, y0 = -width / 2, 21 * u
        self.slots = VGroup(*[Square(16 * u, stroke_width=0, fill_opacity=0).move_to([x0 + (8 + 18 * k + 8) * u, y0 - (18 + 8) * u, 0])
                              for k in range(9)])
        self.title = gui_text(title, GUI_TITLE, u, shadow=False)
        self.title.move_to([x0 + 8 * u, y0 - 6 * u, 0], aligned_edge=UL)
        self.add(self.panel, self.slots, self.title)

    def title_for(self, text):
        return gui_text(text, GUI_TITLE, self.u, shadow=False).move_to(self.title, aligned_edge=UL)

    def item(self, k, value, count, count_color=MC_WHITE):
        return item_stack(value, count, self.s, count_color).move_to(self.slots[k])


class Hotbar(VGroup):
    def __init__(self, n=9, width=7.4, **kwargs):
        super().__init__(**kwargs)
        u = width / 182
        self.u = u
        self.s = 16 * u
        self.bar = pixel_image(_gui("hotbar"), width, 22 * u)
        self.slots = VGroup(*[Square(16 * u, stroke_width=0, fill_opacity=0).move_to([-width / 2 + (3 + 20 * k + 8) * u, 0, 0])
                              for k in range(9)])
        self.add(self.bar, self.slots)

    def selector(self, k):
        sel = pixel_image(_gui("hotbar_selection"), 24 * self.u, 23 * self.u)
        return sel.move_to(self.slots[k]).shift(DOWN * 0.5 * self.u)

    def item(self, k, value):
        icon = iso_block(f"{ORE_OF[value]}_ore", self.s * 0.95)
        val = MT(str(value), 40, MC_WHITE)
        val.scale_to_fit_height(self.u * 9)
        val.move_to(icon.get_corner(DR) + np.array([self.u * 2, -self.u * 2, 0]), aligned_edge=DR)
        return VGroup(icon, val).move_to(self.slots[k])


def toast(title, sub, icon_tex="gold_block", w=5.6):
    # The advancement toast: game sprite, item icon, yellow title and white description
    u = w / 160
    box = pixel_image(_gui("toast"), w, 32 * u)
    icon = iso_block(icon_tex, 16 * u).move_to(box.get_left() + RIGHT * 16 * u)
    t1 = gui_text(title, "#FFFF00", u)
    t2 = gui_text(sub, MC_WHITE, u)
    t1.move_to(box.get_corner(UL) + np.array([30 * u, -7 * u, 0]), aligned_edge=UL)
    t2.move_to(box.get_corner(UL) + np.array([30 * u, -18 * u, 0]), aligned_edge=UL)
    return VGroup(box, icon, t1, t2)


def xp_bar(width=7.4):
    # Experience bar sprites; fill(f) returns the progress part for a fraction f
    u = width / 182
    bg = pixel_image(_gui("xp_bg"), width, 5 * u)

    def fill(f):
        n = max(1, int(round(182 * f)))
        part = pixel_image(_gui("xp_fill").crop((0, 0, n, 5)), n * u, 5 * u)
        return part.move_to(bg.get_left(), aligned_edge=LEFT)

    return bg, fill


def level_text(s, height=0.55):
    # Level number style: green with a black outline on all four sides
    img = text_image(s, "#80FF20", shadow=False)
    out = PILImage.new("RGBA", (img.width + 2, img.height + 2))
    black = PILImage.new("RGBA", img.size, (0, 0, 0, 255))
    black.putalpha(img.getchannel("A"))
    for dx, dy in [(0, 1), (2, 1), (1, 0), (1, 2)]:
        out.alpha_composite(black, (dx, dy))
    out.alpha_composite(img, (1, 1))
    u = height / out.height
    return pixel_image(out, out.width * u, out.height * u)


def chest_icon(w=1.0):
    return pixel_image(_load("chest_front"), w, w * 15 / 14)


# ---------- code ----------
CODE_COLORS = [(Token.Keyword, "#FFAA00"), (Token.Name.Builtin, "#55FFFF"), (Token.Name.Function, "#55FF55"),
               (Token.Literal.Number, "#FF55FF"), (Token.Literal.String, "#FFFF55"), (Token.Operator, "#AAAAAA"),
               (Token.Punctuation, "#AAAAAA"), (Token.Comment, "#AAAAAA")]


def _token_color(tok):
    for t, c in CODE_COLORS:
        if tok in t:
            return c
    return "#FFFFFF"


class MCCode(VGroup):
    """Code drawn with the game font and chat colors; exposes code_lines, line_numbers and background like Code."""

    def __init__(self, src, line_h=11, **kwargs):
        super().__init__(**kwargs)
        lines = [[]]
        for tok, text in PythonLexer().get_tokens(src):
            for k, part in enumerate(text.split("\n")):
                if k:
                    lines.append([])
                if part:
                    lines[-1].append((part, _token_color(tok)))
        while lines and not lines[-1]:
            lines.pop()
        rows, nums = VGroup(), VGroup()
        for k, parts in enumerate(lines):
            img = PILImage.new("RGBA", (1, 9))
            for text, color in parts:
                piece = text_image(text, color)
                both = PILImage.new("RGBA", (img.width + piece.width - 1, 9))
                both.alpha_composite(img, (0, 0))
                both.alpha_composite(piece, (img.width - 1, 0))
                img = both
            # An invisible box spanning the whole line keeps the indentation (leading spaces have no pixels)
            span = Rectangle(width=img.width * 0.1, height=0.9, stroke_width=0, fill_opacity=0)
            row = VGroup(span, pixel_image(img, img.width * 0.1, 0.9).move_to(span))
            row.move_to([0, -k * line_h * 0.1, 0], aligned_edge=LEFT)
            rows.add(row)
            nimg = text_image(str(k + 1), "#AAAAAA")
            num = pixel_image(nimg, nimg.width * 0.1, 0.9)
            num.move_to([-0.8, -k * line_h * 0.1, 0], aligned_edge=RIGHT)
            nums.add(num)
        for row in rows:
            row.align_to(nums, LEFT).shift(RIGHT * 1.4)
        body = VGroup(nums, rows)
        self.background = Rectangle(width=body.width + 2.4, height=body.height + 1.8, fill_color="#000000",
                                    fill_opacity=0.86, stroke_width=0).move_to(body)
        self.code_lines, self.line_numbers = rows, nums
        self.add(self.background, nums, rows)


def code_panel(src, y, width=8.4, max_h=None):
    code = MCCode(src)
    code.scale_to_fit_width(width)
    if max_h and code.height > max_h:
        code.scale_to_fit_height(max_h)
    return code.move_to([0, y, 0])

FONDO = True

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
    first, last = rows[0], rows[-1]
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
