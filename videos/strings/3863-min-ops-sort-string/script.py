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
