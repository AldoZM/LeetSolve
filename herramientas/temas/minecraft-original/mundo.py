# Reads a Java Edition world (NBT + Anvil region files) and exports the visible blocks around a point for three.js.
# Usage:
#   python mundo.py info  <world folder>                      player position, rotation and spawn
#   python mundo.py export <world folder> X Y Z RADIUS out.json  visible blocks in a square around (X, Z)
import gzip
import io
import json
import math
import os
import struct
import sys
import zlib

# ---------- NBT ----------
def _read_tag(f, t):
    if t == 1:
        return struct.unpack('>b', f.read(1))[0]
    if t == 2:
        return struct.unpack('>h', f.read(2))[0]
    if t == 3:
        return struct.unpack('>i', f.read(4))[0]
    if t == 4:
        return struct.unpack('>q', f.read(8))[0]
    if t == 5:
        return struct.unpack('>f', f.read(4))[0]
    if t == 6:
        return struct.unpack('>d', f.read(8))[0]
    if t == 7:
        n = struct.unpack('>i', f.read(4))[0]
        return f.read(n)
    if t == 8:
        n = struct.unpack('>H', f.read(2))[0]
        return f.read(n).decode('utf-8', 'replace')
    if t == 9:
        et, n = struct.unpack('>bi', f.read(5))
        return [_read_tag(f, et) for _ in range(n)]
    if t == 10:
        out = {}
        while True:
            ct = f.read(1)[0]
            if ct == 0:
                return out
            name = f.read(struct.unpack('>H', f.read(2))[0]).decode('utf-8', 'replace')
            out[name] = _read_tag(f, ct)
    if t == 11:
        n = struct.unpack('>i', f.read(4))[0]
        return list(struct.unpack(f'>{n}i', f.read(4 * n)))
    if t == 12:
        n = struct.unpack('>i', f.read(4))[0]
        return list(struct.unpack(f'>{n}q', f.read(8 * n)))
    raise ValueError(f'bad tag {t}')


def read_nbt(data):
    f = io.BytesIO(data)
    t = f.read(1)[0]
    f.read(struct.unpack('>H', f.read(2))[0])
    return _read_tag(f, t)


def read_nbt_file(path):
    raw = open(path, 'rb').read()
    return read_nbt(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw)


# ---------- regions ----------
def region_dir(world):
    for d in ('dimensions/minecraft/overworld/region', 'region'):
        p = os.path.join(world, d)
        if os.path.isdir(p):
            return p
    raise FileNotFoundError('no overworld region folder')


_regions = {}


def chunk(world, cx, cz):
    rx, rz = cx >> 5, cz >> 5
    path = os.path.join(region_dir(world), f'r.{rx}.{rz}.mca')
    if path not in _regions:
        _regions[path] = open(path, 'rb').read() if os.path.exists(path) else b''
    buf = _regions[path]
    if not buf:
        return None
    i = 4 * ((cx & 31) + (cz & 31) * 32)
    off = int.from_bytes(buf[i:i + 3], 'big') * 4096
    if off == 0:
        return None
    length = struct.unpack('>i', buf[off:off + 4])[0]
    comp = buf[off + 4]
    data = buf[off + 5:off + 4 + length]
    if comp == 2:
        data = zlib.decompress(data)
    elif comp == 1:
        data = gzip.decompress(data)
    elif comp != 3:
        raise ValueError(f'chunk compression {comp} not supported')
    return read_nbt(data)


def sections(ch):
    # y index -> (palette names, unpacked indices or None when the section is one block)
    out = {}
    for s in ch.get('sections', []):
        bs = s.get('block_states')
        if not bs:
            continue
        pal = [p['Name'].split(':', 1)[1] + _props(p) for p in bs['palette']]
        data = bs.get('data')
        if not data:
            out[s['Y']] = (pal, None)
            continue
        bits = max(4, math.ceil(math.log2(len(pal))))
        per = 64 // bits
        mask = (1 << bits) - 1
        idx = []
        for v in data:
            v &= (1 << 64) - 1
            for k in range(per):
                idx.append((v >> (k * bits)) & mask)
        out[s['Y']] = (pal, idx[:4096])
    return out


def _props(p):
    # Keep the few properties that change how a block looks
    pr = p.get('Properties', {})
    keep = [f'{k}={pr[k]}' for k in ('axis', 'half', 'type', 'facing') if k in pr]
    return ('[' + ','.join(keep) + ']') if keep else ''


# ---------- export ----------
AIR = {'air', 'cave_air', 'void_air'}
# Blocks that do not hide their neighbors
SEE_THROUGH = ('leaves', 'glass', 'grass', 'fern', 'flower', 'poppy', 'dandelion', 'tulip', 'orchid', 'allium', 'bluet',
               'daisy', 'cornflower', 'lily', 'water', 'snow', 'vine', 'sapling', 'bush', 'dead_bush', 'sugar_cane',
               'kelp', 'seagrass', 'torch', 'mushroom', 'rose', 'peony', 'lilac', 'sunflower', 'petals', 'leaf_litter',
               'firefly', 'cactus', 'pumpkin', 'melon', 'carpet', 'moss_carpet', 'bamboo', 'berry')


def see_through(name):
    return name in AIR or any(w in name for w in SEE_THROUGH)


def export(world, X, Y, Z, R, out, depth=40):
    # All blocks of the columns around (X, Z) from Y + 48 down to Y - depth, keeping only the ones touching air
    y0, y1 = Y - depth, Y + 48
    grid = {}
    for cx in range((X - R) >> 4, ((X + R) >> 4) + 1):
        for cz in range((Z - R) >> 4, ((Z + R) >> 4) + 1):
            ch = chunk(world, cx, cz)
            if ch is None:
                continue
            for sy, (pal, idx) in sections(ch).items():
                if (sy + 1) * 16 <= y0 or sy * 16 > y1:
                    continue
                for i in range(4096):
                    name = pal[idx[i]] if idx else pal[0]
                    if name in AIR:
                        continue
                    lx, lz, ly = i & 15, (i >> 4) & 15, i >> 8
                    x, y, z = cx * 16 + lx, sy * 16 + ly, cz * 16 + lz
                    if abs(x - X) <= R and abs(z - Z) <= R and y0 <= y <= y1:
                        grid[(x, y, z)] = name
    # Surface height per column (highest block that hides what is below); caves under it are never seen
    top = {}
    for (x, y, z), name in grid.items():
        if not see_through(name) and y > top.get((x, z), -10 ** 6):
            top[(x, z)] = y
    vis = []
    for (x, y, z), name in grid.items():
        floor = min(top.get((x + dx, z + dz), top.get((x, z), y)) for dx, dz in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)))
        if y < floor - 1 and not see_through(name):
            continue
        if y < top.get((x, z), y) and see_through(name):
            continue
        for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            nb = grid.get((x + d[0], y + d[1], z + d[2]), 'air')
            if see_through(nb) and nb != name:
                vis.append([x - X, y - Y, z - Z, name])
                break
    names = sorted({v[3] for v in vis})
    looks = block_textures(names, os.path.join(os.path.dirname(os.path.abspath(out)), 'tex'))
    json.dump({'center': [X, Y, Z], 'radius': R, 'names': names, 'looks': looks,
               'blocks': [[x, y, z, names.index(n)] for x, y, z, n in vis]}, open(out, 'w'))
    counts = {}
    for v in vis:
        counts[v[3]] = counts.get(v[3], 0) + 1
    print(len(vis), 'visible blocks;', sorted(counts.items(), key=lambda c: -c[1])[:25])


GRASS_TINT, FOLIAGE_TINT, WATER_TINT = (145, 189, 89), (119, 171, 47), (63, 118, 228)
# Birch and spruce leaves ignore the biome and always use the same color in the game
FIXED_LEAF_TINT = {'birch_leaves': (128, 167, 85), 'spruce_leaves': (97, 153, 97)}
DRY_FOLIAGE_TINT = (164, 122, 74)
CROSS = ('short_grass', 'tall_grass', 'fern', 'bush', 'dandelion', 'poppy', 'cornflower', 'azure_bluet', 'oxeye_daisy',
         'allium', 'tulip', 'orchid', 'lily_of_the_valley', 'sapling', 'dead_bush', 'sugar_cane', 'sweet_berry', 'mushroom',
         'firefly_bush', 'pink_petals', 'wildflowers', 'leaf_litter')
TINTED_PLANTS = ('short_grass', 'tall_grass', 'fern', 'bush', 'sugar_cane')


def block_textures(names, out_dir):
    # Copies the textures each block needs from the newest game jar; returns name -> {kind, top, side, bottom}
    from PIL import Image, ImageChops
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import extraer
    import zipfile
    jar = zipfile.ZipFile(os.path.join(extraer.MC, 'versions', extraer.newest_version(), extraer.newest_version() + '.jar'))
    have = set(jar.namelist())
    os.makedirs(out_dir, exist_ok=True)

    def get(path):
        p = f'assets/minecraft/textures/block/{path}.png'
        if p not in have:
            return None
        img = Image.open(jar.open(p)).convert('RGBA')
        return img.crop((0, 0, img.width, img.width))  # animated strips: first frame

    def save(key, img):
        img.save(os.path.join(out_dir, key + '.png'))
        return key

    looks = {}
    for full in names:
        base = full.split('[')[0]
        lower = 'half=lower' in full
        if base == 'grass_block':
            top = save('grass_block_top', extraer.tint(get('grass_block_top'), GRASS_TINT))
            side = get('grass_block_side')
            side.alpha_composite(extraer.tint(get('grass_block_side_overlay'), GRASS_TINT))
            looks[full] = {'kind': 'cube', 'top': top, 'side': save('grass_block_side', side), 'bottom': save('dirt', get('dirt'))}
        elif base == 'leaf_litter':
            # A flat layer on the ground, colored like dry foliage (a gray cross without it)
            looks[full] = {'kind': 'flat', 'top': save('leaf_litter', extraer.tint(get('leaf_litter'), DRY_FOLIAGE_TINT))}
        elif base == 'water' or base == 'bubble_column':
            looks[full] = {'kind': 'water', 'top': save('water', extraer.tint(get('water_still'), WATER_TINT))}
        elif any(base.startswith(c) or base.endswith(c) for c in CROSS):
            name = base
            if base == 'tall_grass':
                name = 'tall_grass_bottom' if lower else 'tall_grass_top'
            img = get(name) or get(base + ('_bottom' if lower else '_top')) or get('short_grass')
            if base.startswith(TINTED_PLANTS):
                img = extraer.tint(img, GRASS_TINT)
            looks[full] = {'kind': 'cross', 'side': save(name, img)}
        elif base.endswith('_log') or base.endswith('_wood'):
            looks[full] = {'kind': 'cube', 'axis': full.split('axis=')[1][0] if 'axis=' in full else 'y',
                           'top': save(base + '_top', get(base + '_top') or get(base)), 'side': save(base, get(base))}
        elif base.endswith('leaves'):
            img = get(base)
            if base in ('oak_leaves', 'jungle_leaves', 'acacia_leaves', 'dark_oak_leaves', 'mangrove_leaves'):
                img = extraer.tint(img, FOLIAGE_TINT)
            elif base in FIXED_LEAF_TINT:
                img = extraer.tint(img, FIXED_LEAF_TINT[base])
            looks[full] = {'kind': 'cube', 'side': save(base, img), 'cutout': True}
        else:
            img = get(base) or get(base + '_side') or get('stone')
            top = get(base + '_top')
            looks[full] = {'kind': 'cube', 'side': save(base, img)}
            if top:
                looks[full]['top'] = save(base + '_top', top)
    return looks


def info(world):
    lvl = read_nbt_file(os.path.join(world, 'level.dat'))
    d = lvl.get('Data', lvl)
    print('name:', d.get('LevelName'), '| version:', d.get('Version', {}).get('Name'), '| data version:', d.get('DataVersion'))
    sp = d.get('spawn') or {k: d.get(k) for k in ('SpawnX', 'SpawnY', 'SpawnZ')}
    print('spawn:', sp)
    pdir = os.path.join(world, 'players', 'data')
    if not os.path.isdir(pdir):
        pdir = os.path.join(world, 'playerdata')
    for fn in os.listdir(pdir):
        if fn.endswith('.dat'):
            p = read_nbt_file(os.path.join(pdir, fn))
            yaw, pitch = p.get('Rotation', [0, 0])
            facing = ['south', 'west', 'north', 'east'][int(((yaw % 360) + 45) // 90) % 4]
            print('player', fn[:8], 'pos:', [round(v, 2) for v in p.get('Pos', [])], 'yaw:', round(yaw, 1),
                  'pitch:', round(pitch, 1), 'facing:', facing)


if __name__ == '__main__':
    cmd, world = sys.argv[1], sys.argv[2]
    if cmd == 'info':
        info(world)
    else:
        X, Y, Z, R = map(int, sys.argv[3:7])
        export(world, X, Y, Z, R, sys.argv[7])
