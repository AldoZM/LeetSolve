# Generates the blocky pixel textures of the Minecraft theme (original procedural art, fixed seeds).
# Writes tex/<name>.png at 16x16 (three.js, NearestFilter) and tex/<name>@8.png upscaled 8x (Manim).
# Usage: python textures.py
import os
import random
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tex')
N = 16


def hexrgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def shade(c, k):
    return tuple(max(0, min(255, int(v * k))) for v in c)


def noise_fill(img, base, rng, spread=0.12):
    for y in range(N):
        for x in range(N):
            img.putpixel((x, y), shade(base, 1 + rng.uniform(-spread, spread)))


def stone(rng):
    img = Image.new('RGB', (N, N))
    noise_fill(img, hexrgb('#7d7d7d'), rng, 0.08)
    # Darker cracks
    for _ in range(9):
        x, y = rng.randrange(N), rng.randrange(N)
        for k in range(rng.randint(1, 3)):
            img.putpixel(((x + k) % N, y), shade(hexrgb('#7d7d7d'), 0.8))
    return img


def ore(color, rng):
    img = stone(rng)
    c = hexrgb(color)
    # A few blobs of 3-5 pixels with a light highlight and a dark edge
    spots = [(3, 3), (10, 2), (6, 8), (12, 10), (2, 12), (9, 13)]
    for sx, sy in spots:
        sx += rng.randint(-1, 1)
        sy += rng.randint(-1, 1)
        cells = [(sx, sy), (sx + 1, sy), (sx, sy + 1)]
        if rng.random() < 0.6:
            cells.append((sx + 1, sy + 1))
        for x, y in cells:
            img.putpixel((x % N, y % N), shade(c, rng.uniform(0.85, 1.05)))
        img.putpixel((sx % N, sy % N), shade(c, 1.3))
        img.putpixel(((sx + 1) % N, (sy + 2) % N), shade(c, 0.55))
    return img


def dirt(rng):
    img = Image.new('RGB', (N, N))
    noise_fill(img, hexrgb('#866043'), rng, 0.1)
    for _ in range(14):
        img.putpixel((rng.randrange(N), rng.randrange(N)), hexrgb(rng.choice(['#5d4130', '#a07a59', '#6c4c36'])))
    return img


def grass_top(rng):
    img = Image.new('RGB', (N, N))
    noise_fill(img, hexrgb('#5f9e3a'), rng, 0.14)
    return img


def grass_side(rng):
    img = dirt(rng)
    top = grass_top(rng)
    for x in range(N):
        depth = 3 + (1 if rng.random() < 0.45 else 0) + (1 if rng.random() < 0.15 else 0)
        for y in range(depth):
            img.putpixel((x, y), top.getpixel((x, y)))
    return img


def planks(rng):
    img = Image.new('RGB', (N, N))
    base = hexrgb('#a2824e')
    for y in range(N):
        band = shade(base, 1 + 0.05 * ((y // 4) % 2))
        for x in range(N):
            img.putpixel((x, y), shade(band, 1 + rng.uniform(-0.06, 0.06)))
    for y in range(3, N, 4):
        for x in range(N):
            img.putpixel((x, y), shade(base, 0.62))
    # Plank joints, offset on every other row
    for row in range(4):
        jx = 5 if row % 2 else 12
        for y in range(row * 4, row * 4 + 3):
            img.putpixel((jx, y), shade(base, 0.7))
    return img


def gold_block(rng):
    img = Image.new('RGB', (N, N))
    noise_fill(img, hexrgb('#f8d33a'), rng, 0.05)
    for i in range(N):
        img.putpixel((i, 0), hexrgb('#fff59e'))
        img.putpixel((0, i), hexrgb('#fff59e'))
        img.putpixel((i, N - 1), hexrgb('#c69414'))
        img.putpixel((N - 1, i), hexrgb('#c69414'))
    return img


def chest_face(rng, front, seam=True):
    img = Image.new('RGB', (N, N))
    noise_fill(img, hexrgb('#a86d2b'), rng, 0.07)
    edge = hexrgb('#3b2410')
    for i in range(N):
        for p in [(i, 0), (0, i), (i, N - 1), (N - 1, i)]:
            img.putpixel(p, edge)
    if not seam:
        return img
    # Seam between lid and body
    for x in range(N):
        img.putpixel((x, 5), edge)
    if front:
        for x in range(7, 9):
            for y in range(4, 8):
                img.putpixel((x, y), hexrgb('#c7c7c7') if y > 4 else hexrgb('#ffffff'))
        img.putpixel((7, 7), hexrgb('#5a5a5a'))
        img.putpixel((8, 7), hexrgb('#5a5a5a'))
    return img


def cobble(rng):
    img = Image.new('RGB', (N, N))
    noise_fill(img, hexrgb('#6f6f6f'), rng, 0.06)
    for _ in range(12):
        x, y = rng.randrange(N), rng.randrange(N)
        w, h = rng.randint(2, 4), rng.randint(2, 3)
        c = shade(hexrgb('#8a8a8a'), rng.uniform(0.9, 1.15))
        for i in range(w):
            for j in range(h):
                img.putpixel(((x + i) % N, (y + j) % N), c)
        for i in range(w):
            img.putpixel(((x + i) % N, (y + h) % N), hexrgb('#4a4a4a'))
    return img


def leaves(rng):
    img = Image.new('RGB', (N, N))
    for y in range(N):
        for x in range(N):
            r = rng.random()
            img.putpixel((x, y), hexrgb('#2f6b1f') if r < 0.22 else shade(hexrgb('#4a9a2c'), rng.uniform(0.8, 1.15)))
    return img


def log_side(rng):
    img = Image.new('RGB', (N, N))
    base = hexrgb('#6b5032')
    for x in range(N):
        stripe = 0.8 if x % 4 == 0 else (1.08 if x % 4 == 2 else 1.0)
        for y in range(N):
            img.putpixel((x, y), shade(base, stripe * rng.uniform(0.92, 1.06)))
    return img


def log_top(rng):
    img = Image.new('RGB', (N, N))
    for y in range(N):
        for x in range(N):
            d = max(abs(x - 7.5), abs(y - 7.5))
            img.putpixel((x, y), hexrgb('#6b5032') if d > 6.5 else shade(hexrgb('#b8945a'), 0.88 if int(d) % 2 else 1.0))
    return img


ORES = {'coal': '#2a2a2a', 'iron': '#d9b49a', 'gold': '#fbe14a', 'diamond': '#5fe8f0', 'emerald': '#2fd968',
        'redstone': '#e3221c', 'lapis': '#2b57c9'}


def main():
    os.makedirs(OUT, exist_ok=True)
    make = {'stone': stone, 'dirt': dirt, 'grass_top': grass_top, 'grass_side': grass_side, 'planks': planks,
            'gold_block': gold_block, 'cobble': cobble,
            'chest_front': lambda r: chest_face(r, True), 'chest_side': lambda r: chest_face(r, False)}
    for name, color in ORES.items():
        make[f'{name}_ore'] = lambda r, c=color: ore(c, r)
    # Added later; appended so the seeds of the textures above do not change
    make.update({'chest_plain': lambda r: chest_face(r, False, seam=False), 'leaves': leaves, 'log_side': log_side,
                 'log_top': log_top})
    for k, (name, fn) in enumerate(make.items()):
        img = fn(random.Random(1000 + k))
        img = img.convert('RGBA')
        img.save(os.path.join(OUT, f'{name}.png'))
        img.resize((N * 8, N * 8), Image.NEAREST).save(os.path.join(OUT, f'{name}@8.png'))
    print('textures:', ', '.join(make))


if __name__ == '__main__':
    main()
