# Burned-in subtitles in the game font: short blocks of 2 to 4 words that pop in as the voice says them.
# Needs words.json (palabras.py, after the voice). In video.json:
#   "subtitulos": {"cambios": {"google dot com": "google.com"}, "amarillo": ["DNS", "root library"], "verde": ["instant"]}
# "cambios" turns the words written for the voice into the ones shown; letters spelled out ("D N S") join on their own.
# Keywords are matched on the shown text, a phrase only when its words come together; with punctuation, exactly.
# "ocultar": [[a, z]] keeps those seconds without subtitles (see blocks_of).
# build.py calls burn() in the mux step; `python subtitulos.py <video folder>` prints the blocks to check them.
import json
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

S = 10                # screen pixels per font pixel (letters 70 px tall)
MAX_W = 960           # widest block on a 1080 px frame
MAX_WORDS = 4
CENTER_Y = 0.76       # block center, as a fraction of the height: under the cover sign, above the Shorts title
# Where a block goes when a tooltip of the page sits under it: the first free one wins (0.84 is low, but only for a moment)
HEIGHTS = (CENTER_Y, 0.84, 0.68)
BAND_H = 300          # height of the strip the subtitles are drawn in
OUTLINE = 9           # black outline around the letters
SHADOW = 6            # drop shadow, down and to the right
# The game's color codes §f, §e, §a, §c, §9, §6: any of these names can be a keyword list in video.json
COLORS = {'blanco': (255, 255, 255), 'amarillo': (255, 255, 85), 'verde': (85, 255, 85), 'rojo': (255, 85, 85),
          'azul': (85, 85, 255), 'dorado': (255, 170, 0)}
PUNCT = ',.;:!?'


# ---------- font (the theme's font/ascii.png, same glyphs and widths as mc.js) ----------
class Font:
    def __init__(self, tema):
        sheet = np.array(Image.open(os.path.join(tema, 'font', 'ascii.png')).convert('RGBA'))[:, :, 3]
        rows = json.load(open(os.path.join(tema, 'font', 'ascii.json'), encoding='utf-8'))['chars']
        self.cell = sheet.shape[1] // 16
        self.glyphs = {}
        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                if ch == '\0':
                    continue
                g = sheet[r * self.cell:(r + 1) * self.cell, c * self.cell:(c + 1) * self.cell] > 0
                cols = np.flatnonzero(g.any(axis=0))
                self.glyphs[ch] = (g, int(cols.max()) + 1 if len(cols) else 3)
        self.glyphs[' '] = (np.zeros((self.cell, self.cell), bool), 3)

    def glyph(self, ch):
        return self.glyphs.get(ch) or self.glyphs['?']

    def width(self, s):
        return sum(self.glyph(ch)[1] + 1 for ch in s) - 1


# ---------- words -> blocks ----------
def norm(w):
    return re.sub(r'[^a-z0-9]', '', w.lower())


def shown(w):
    # Upper case; commas and periods go, ? and ! stay
    return w.rstrip(',.;:').upper()


def units_of(words, cambios):
    # Script words -> shown words, with their times
    units = [{'t': w['w'], 'a': w['start'], 'b': w['end']} for w in words]
    keys = sorted(((k.split(), v) for k, v in cambios.items()), key=lambda kv: -len(kv[0]))
    for src, dst in keys:
        n, src = len(src), [norm(x) for x in src]
        i = 0
        while i + n <= len(units):
            if [norm(u['t']) for u in units[i:i + n]] == src:
                tail = units[i + n - 1]['t']
                end = tail[len(tail.rstrip(PUNCT)):]
                units[i:i + n] = [{'t': dst + end, 'a': units[i]['a'], 'b': units[i + n - 1]['b'], 'fixed': True}]
            i += 1
    # Spelled letters, as written for the voice: "D N S" -> "DNS"
    out = []
    for u in units:
        letter = re.fullmatch(r'[A-Z][,.;:!?]?', u['t']) and not u.get('fixed')
        prev = out[-1] if out else None
        if letter and prev and prev.get('letters') and prev['t'][-1].isalpha():
            prev.update(t=prev['t'] + u['t'], b=u['b'])
        else:
            out.append(dict(u, letters=bool(letter)))
    return out


def color_units(units, cfg):
    for u in units:
        u['color'], u['phrase'] = 'blanco', None
    for color in (c for c in COLORS if c != 'blanco'):
        for phrase in cfg.get(color, []):
            # With punctuation ("from:") only that exact spelling counts, to pick one use of a common word
            key = (lambda w: w.lower()) if any(ch in PUNCT for ch in phrase) else norm
            p = [key(x) for x in phrase.split()]
            for i in range(len(units) - len(p) + 1):
                if [key(u['t']) for u in units[i:i + len(p)]] == p:
                    for u in units[i:i + len(p)]:
                        u['color'], u['phrase'] = color, (i, phrase)
            # A shown word made by "cambios" can have spaces ("OR 1=1"): it is one piece
            for i, u in enumerate(units):
                if ' ' in u['t'] and key(u['t']) == key(phrase):
                    u['color'], u['phrase'] = color, (i, phrase)


def blocks_of(lines, cfg, font, total):
    blocks = []
    for line in lines:
        units = units_of(line['words'], cfg.get('cambios', {}))
        color_units(units, cfg)
        cur = []
        for u in units:
            text = ' '.join(shown(x['t']) for x in cur + [u])
            if cur and (len(cur) >= MAX_WORDS or font.width(text) * S > MAX_W or u['a'] - cur[-1]['b'] > 0.35):
                # A highlighted phrase is not split: its first words move to the next block with it
                k = len(cur)
                while u['phrase'] and k > 1 and cur[k - 1]['phrase'] == u['phrase']:
                    k -= 1
                blocks.append(cur[:k])
                cur = cur[k:]
            cur.append(u)
            if u['t'][-1] in PUNCT:
                blocks.append(cur)
                cur = []
        if cur:
            blocks.append(cur)
    # On screen from just before the first word until the next block, or a moment after the last word in a pause
    out = []
    for k, b in enumerate(blocks):
        a = max(0.0, b[0]['a'] - 0.04)
        nxt = blocks[k + 1][0]['a'] - 0.04 if k + 1 < len(blocks) else total
        z = nxt if nxt - b[-1]['b'] < 0.5 else b[-1]['b'] + 0.3
        out.append({'a': a, 'z': min(z, total), 'units': b})
    # "ocultar": [[a, z], ...] keeps that time clear, for what the tooltip check cannot see (the cover sign rising
    # through the subtitles at the end). A block that starts inside waits for the end of it, or is dropped.
    for o0, o1 in cfg.get('ocultar', []):
        for b in out:
            if o0 <= b['a'] < o1:
                b['a'] = o1
            elif b['a'] < o0 < b['z']:
                b['z'] = o0
        out = [b for b in out if b['z'] - b['a'] > 0.1]
    return out


# ---------- drawing ----------
def draw_block(font, units):
    parts = [(shown(u['t']), COLORS[u['color']]) for u in units]
    text_w = sum(font.width(t) + 4 for t, _ in parts) - 4  # a space between words is 3 + 1 font pixels
    scale = min(S, MAX_W // max(1, text_w))
    pad = OUTLINE + SHADOW + 2
    W, H = text_w * scale + 2 * pad, font.cell * scale + 2 * pad
    rgb = np.zeros((H, W, 3), np.uint8)
    mask = np.zeros((H, W), bool)
    x = pad
    for t, col in parts:
        for ch in t:
            g, w = font.glyph(ch)
            big = np.kron(g[:, :w], np.ones((scale, scale), bool))  # the cell past the glyph width is empty
            mask[pad:pad + big.shape[0], x:x + big.shape[1]] |= big
            rgb[pad:pad + big.shape[0], x:x + big.shape[1]][big] = col
            x += (w + 1) * scale
        x += 3 * scale  # with the +1 after the last letter, a space is 3 + 1 font pixels
    # Square outline keeps the pixel look; the shadow is the outline moved down and right
    outline = np.array(Image.fromarray(mask.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(2 * OUTLINE + 1))) > 0
    shadow = np.zeros_like(outline)
    shadow[SHADOW:, SHADOW:] = outline[:-SHADOW, :-SHADOW]
    out = np.zeros((H, W, 4), np.uint8)
    out[shadow, 3] = 150
    out[outline, 3] = 255
    out[mask, :3] = rgb[mask]
    return Image.fromarray(out, 'RGBA')


def pop(dt):
    # 85 % -> 105 % in 0.09 s (ease out), back to 100 % by 0.15 s
    if dt < 0.09:
        x = dt / 0.09
        return 0.85 + 0.20 * (1 - (1 - x) ** 2)
    if dt < 0.15:
        return 1.05 - 0.05 * (dt - 0.09) / 0.06
    return 1.0


def band_frame(img, s, width, band_h, cy):
    band = Image.new('RGBA', (width, band_h))
    if s != 1.0:
        img = img.resize((round(img.width * s), round(img.height * s)), Image.BILINEAR)
    band.alpha_composite(img, ((width - img.width) // 2, round(cy - img.height / 2)))
    return band.tobytes()


def tooltip_cells(src, fps=6, W=540, H=960, cell=10):
    # Where the page's tooltips are, frame by frame: pixels of their purple border, counted on a 54 x 96 grid
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'fps={fps},scale={W}:{H}', '-f', 'rawvideo',
                          '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    out, size = [], W * H * 3
    while len(buf := p.stdout.read(size)) == size:
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.int16)
        r, g, b = f[..., 0], f[..., 1], f[..., 2]
        m = (g < 20) & (b > 100) & (b > 1.7 * r) & (r > 20)  # stricter green: Steve's pants passed as a tooltip
        out.append(m.reshape(H // cell, cell, W // cell, cell).sum(axis=(1, 3)) >= 3)
    p.wait()
    return np.array(out), fps


def place(block, img, cells, cfps, W, H):
    # First height where no tooltip shows under the block while it is on screen; else the one with the least overlap
    rows, cols = cells.shape[1:]
    i0, i1 = int(block['a'] * cfps), int(block['z'] * cfps) + 1
    c0, c1 = int((0.5 - img.width / W / 2) * cols), int((0.5 + img.width / W / 2) * cols) + 1
    scores = []
    for y in HEIGHTS:
        r0, r1 = int((y - img.height / H / 2) * rows), int((y + img.height / H / 2) * rows) + 1
        scores.append(int(cells[i0:i1, r0:r1, c0:c1].sum()))
        if scores[-1] == 0:
            return y
    return HEIGHTS[scores.index(min(scores))]


def load(folder, cfg, tema, fps):
    font = Font(tema)
    lines = json.load(open(os.path.join(folder, 'words.json'), encoding='utf-8'))['lines']
    total = json.load(open(os.path.join(folder, 'timestamps.json'), encoding='utf-8'))['total_duration_s']
    return font, blocks_of(lines, cfg, font, total), total


def burn(src, dst, cfg, tema, fps):
    if not os.path.exists('words.json'):
        sys.exit('subtitles need words.json: run herramientas/palabras.py <video folder> with the .venv-tts Python')
    font, blocks, total = load('.', cfg, tema, fps)
    W, H = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                                    '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip().split(','))
    n = round(total * fps)
    imgs = [draw_block(font, b['units']) for b in blocks]
    cells, cfps = tooltip_cells(src)
    ys = [place(b, im, cells, cfps, W, H) for b, im in zip(blocks, imgs)]
    top = round(H * min(HEIGHTS) - BAND_H / 2)
    band_h = round(H * (max(HEIGHTS) - min(HEIGHTS))) + BAND_H
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{band_h}',
                           '-r', str(fps), '-i', '-', '-filter_complex', f'[0:v][1:v]overlay=0:{top}:eof_action=pass[v]',
                           '-map', '[v]', '-frames:v', str(n), '-c:v', 'libx264', '-crf', '16', '-preset', 'slow',
                           '-pix_fmt', 'yuv420p', '-movflags', '+faststart', dst], stdin=subprocess.PIPE)
    empty = bytes(W * band_h * 4)
    cache, k = {}, 0
    for i in range(n):
        t = i / fps
        while k < len(blocks) and blocks[k]['z'] <= t:
            k += 1
        b = blocks[k] if k < len(blocks) and blocks[k]['a'] <= t else None
        if b is None:
            ff.stdin.write(empty)
            continue
        s = round(pop(t - b['a']), 3)
        if (k, s) not in cache:
            cache = {kk: v for kk, v in cache.items() if kk[0] == k}  # only the current block's frames stay
            cache[(k, s)] = band_frame(imgs[k], s, W, band_h, H * ys[k] - top)
        ff.stdin.write(cache[(k, s)])
    ff.stdin.close()
    if ff.wait():
        sys.exit('ffmpeg failed burning the subtitles')
    moved = [(round(b['a'], 1), y) for b, y in zip(blocks, ys) if y != CENTER_Y]
    print(len(blocks), 'subtitle blocks;', len(moved), 'moved away from tooltips:', moved)
    json.dump([{'a': b['a'], 'z': b['z'], 'y': y} for b, y in zip(blocks, ys)], open('media/subtitulos.json', 'w'))


if __name__ == '__main__':
    folder = sys.argv[1]
    cfg = json.load(open(os.path.join(folder, 'video.json'), encoding='utf-8'))
    tema = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temas', cfg.get('tema', 'minecraft-original'))
    font, blocks, _ = load(folder, cfg.get('subtitulos', {}), tema, 30)
    for b in blocks:
        print(f"{b['a']:7.2f} {b['z']:7.2f}  " + ' '.join(
            (shown(u['t']) if u['color'] == 'blanco' else f"[{shown(u['t'])}]") for u in b['units']))
