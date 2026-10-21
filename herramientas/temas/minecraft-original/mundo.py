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
def region_dir(world, kind='region'):
    # kind: 'region' (blocks) or 'entities' (mobs, saved apart since 1.17)
    for d in (f'dimensions/minecraft/overworld/{kind}', kind):
        p = os.path.join(world, d)
        if os.path.isdir(p):
            return p
    raise FileNotFoundError(f'no overworld {kind} folder')


_regions = {}


def chunk(world, cx, cz, kind='region'):
    rx, rz = cx >> 5, cz >> 5
    path = os.path.join(region_dir(world, kind), f'r.{rx}.{rz}.mca')
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
        pal = [_name(p) + _props(p) for p in bs['palette']]
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


def _name(p):
    # Up to 26.2 a palette entry is {Name, Properties}; 26.3 writes {id, properties}, a bare name, or {'': name}
    if isinstance(p, str):
        return p.split(':', 1)[1]
    return (p.get('Name') or p.get('id') or p.get('')).split(':', 1)[1]


def _props(p):
    # Keep the few properties that change how a block looks
    pr = {} if isinstance(p, str) else p.get('Properties') or p.get('properties') or {}
    keep = [f'{k}={pr[k]}' for k in ('axis', 'half', 'type', 'facing') if k in pr]
    return ('[' + ','.join(keep) + ']') if keep else ''


# ---------- export ----------
AIR = {'air', 'cave_air', 'void_air'}
# Blocks that do not hide their neighbors
SEE_THROUGH = ('leaves', 'glass', 'grass', 'fern', 'flower', 'poppy', 'dandelion', 'tulip', 'orchid', 'allium', 'bluet',
               'daisy', 'cornflower', 'lily', 'water', 'snow', 'vine', 'sapling', 'bush', 'dead_bush', 'sugar_cane',
               'kelp', 'seagrass', 'torch', 'mushroom', 'rose', 'peony', 'lilac', 'sunflower', 'petals', 'leaf_litter',
               'firefly', 'cactus', 'pumpkin', 'melon', 'carpet', 'moss_carpet', 'bamboo', 'berry', 'hanging_moss',
               'eyeblossom',
               # Village pieces that do not fill their block
               'slab', 'stairs', 'fence', 'door', 'pane', 'wheat', 'carrots', 'potatoes', 'beetroots', 'farmland',
               'dirt_path', '_bed', 'bell', 'lantern', 'sign', 'chest', 'potted', 'flower_pot', 'ladder', 'rail', 'button',
               'pressure_plate', 'lily_pad')


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
    biome = biome_at(world, X, Y, Z)
    print('biome at the center:', biome)
    looks = block_textures(names, os.path.join(os.path.dirname(os.path.abspath(out)), 'tex'), biome)
    # Blocks with no look (beds, signs, bells...) are left out
    keep = [n for n in names if looks[n]['kind'] != 'skip']
    vis = [v for v in vis if v[3] in keep]
    mobs = mobs_around(world, X, Y, Z, R)
    json.dump({'center': [X, Y, Z], 'radius': R, 'names': keep, 'looks': {n: looks[n] for n in keep},
               'blocks': [[x, y, z, keep.index(n)] for x, y, z, n in vis], 'mobs': mobs}, open(out, 'w'))
    counts = {}
    for v in vis:
        counts[v[3]] = counts.get(v[3], 0) + 1
    print(len(vis), 'visible blocks;', sorted(counts.items(), key=lambda c: -c[1])[:25])
    print(len(mobs), 'mobs;', sorted({m['id'] for m in mobs}))


# Mobs mc.js can draw (makeMobs); horses, rabbits and hostile mobs are left out
MOB_KINDS = ('villager', 'iron_golem', 'cat', 'cow', 'pig', 'sheep', 'chicken', 'wolf')


def mobs_around(world, X, Y, Z, R):
    # The mobs saved in the world around (X, Z): kind, position relative to the center, yaw and their look
    try:
        region_dir(world, 'entities')
    except FileNotFoundError:
        return []
    out = []
    for cx in range((X - R) >> 4, ((X + R) >> 4) + 1):
        for cz in range((Z - R) >> 4, ((Z + R) >> 4) + 1):
            ch = chunk(world, cx, cz, 'entities')
            for e in (ch or {}).get('Entities', []):
                kind = e['id'].split(':')[1]
                x, y, z = e['Pos']
                if kind not in MOB_KINDS or abs(x - X) > R or abs(z - Z) > R:
                    continue
                m = {'id': kind, 'p': [round(x - X, 2), round(y - Y, 2), round(z - Z, 2)],
                     'yaw': round(e.get('Rotation', [0, 0])[0], 1)}
                if e.get('Age', 0) < 0:
                    m['baby'] = 1
                if kind == 'villager':
                    vd = e.get('VillagerData', {})
                    m['type'] = vd.get('type', 'minecraft:plains').split(':')[1]
                    m['profession'] = vd.get('profession', 'minecraft:none').split(':')[1]
                elif kind == 'sheep':
                    m['color'] = e.get('Color', 0)
                elif 'variant' in e:
                    m['variant'] = str(e['variant']).split(':')[-1]
                out.append(m)
    return out


GRASS_TINT, FOLIAGE_TINT, WATER_TINT = (145, 189, 89), (119, 171, 47), (63, 118, 228)
# Biomes whose grass and foliage colors are not the plains ones: (grass, foliage)
BIOME_TINTS = {'pale_garden': ((119, 130, 114), (135, 141, 118)), 'cherry_grove': ((182, 219, 97), (182, 219, 97)),
               'meadow': ((131, 187, 109), (99, 169, 72)), 'taiga': ((134, 183, 131), (104, 164, 100)),
               'birch_forest': ((136, 187, 103), (107, 169, 65)), 'old_growth_birch_forest': ((136, 187, 103), (107, 169, 65)),
               'river': ((142, 185, 113), (113, 167, 71))}
# Leaves with a fixed color in every biome
LEAF_TINTS = {'birch_leaves': (128, 167, 85), 'spruce_leaves': (97, 153, 97)}
CROSS = ('short_grass', 'tall_grass', 'fern', 'bush', 'dandelion', 'poppy', 'cornflower', 'azure_bluet', 'oxeye_daisy',
         'allium', 'tulip', 'orchid', 'lily_of_the_valley', 'sapling', 'dead_bush', 'sugar_cane', 'sweet_berry', 'mushroom',
         'firefly_bush', 'pink_petals', 'wildflowers', 'leaf_litter', 'pale_hanging_moss', 'eyeblossom')


def biome_at(world, x, y, z):
    # Biome of the 4x4x4 cell holding (x, y, z)
    ch = chunk(world, x >> 4, z >> 4)
    for s in ch.get('sections', []) if ch else []:
        if s['Y'] != y >> 4 or 'biomes' not in s:
            continue
        pal, data = s['biomes']['palette'], s['biomes'].get('data')
        if not data:
            return pal[0].split(':', 1)[1]
        bits = max(1, (len(pal) - 1).bit_length())
        per = 64 // bits
        i = ((y & 15) >> 2) * 16 + ((z & 15) >> 2) * 4 + ((x & 15) >> 2)
        v = data[i // per] & ((1 << 64) - 1)
        return pal[(v >> ((i % per) * bits)) & ((1 << bits) - 1)].split(':', 1)[1]
    return 'plains'


TINTED_PLANTS = ('short_grass', 'tall_grass', 'fern', 'bush', 'sugar_cane')
# Plants that lie flat on the ground, and the dry foliage color of leaf litter
FLAT = ('pink_petals', 'wildflowers', 'leaf_litter')
DRY_FOLIAGE = (160, 110, 60)
# Village crops drawn grown, as the game's cross plants
CROPS = {'wheat': 'wheat_stage7', 'carrots': 'carrots_stage3', 'potatoes': 'potatoes_stage3', 'beetroots': 'beetroots_stage3'}
# Small blocks without a block texture (entities, models): left out instead of drawn as stone
NO_LOOK = ('_bed', 'bell', 'lantern', 'sign', 'chest', 'potted', 'flower_pot', 'ladder', 'vine', 'rail', 'button',
           'pressure_plate', 'banner', 'head', 'skull', 'lichen', 'chain', 'candle', 'campfire', 'lectern',
           'brewing_stand', 'grindstone', 'anvil', 'cauldron', 'water_cauldron', 'trapdoor', 'item_frame', 'hopper')


def material(base, get):
    # Texture of the full block a slab, stair, fence or wall is made of: oak_slab -> oak_planks
    stem = base
    for suffix in ('_slab', '_stairs', '_fence_gate', '_fence', '_wall'):
        stem = stem.removesuffix(suffix)
    for name in (stem, stem + '_planks', stem + 's', stem + '_block', stem.replace('smooth_', '') + '_top'):
        img = get(name)
        if img:
            return name, img
    return None


def block_textures(names, out_dir, biome='plains'):
    # Copies the textures each block needs from the newest game jar; returns name -> {kind, top, side, bottom}
    # Grass and foliage take the colors of the center's biome; those textures get the biome in their file name,
    # so worlds sharing tex/ do not overwrite each other's plains ones
    grass, foliage = BIOME_TINTS.get(biome, (GRASS_TINT, FOLIAGE_TINT))
    sfx = f'_{biome}' if biome in BIOME_TINTS else ''
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
        # 26.3 leaves out properties at their default value, and the default half is the lower one
        lower = 'half=upper' not in full
        if base == 'grass_block':
            top = save('grass_block_top' + sfx, extraer.tint(get('grass_block_top'), grass))
            side = get('grass_block_side')
            side.alpha_composite(extraer.tint(get('grass_block_side_overlay'), grass))
            looks[full] = {'kind': 'cube', 'top': top, 'side': save('grass_block_side' + sfx, side),
                           'bottom': save('dirt', get('dirt'))}
        elif base == 'water' or base == 'bubble_column':
            looks[full] = {'kind': 'water', 'top': save('water', extraer.tint(get('water_still'), WATER_TINT))}
        elif base in FLAT:
            # Lying on the ground: petals and flowers over their tinted stems, gray leaf litter in its dry color
            img = get(base)
            if base == 'leaf_litter':
                img = extraer.tint(img, DRY_FOLIAGE)
            else:
                stem = extraer.tint(get(base + '_stem'), grass)
                stem.alpha_composite(img)
                img = stem
            looks[full] = {'kind': 'cube', 'side': save(base + sfx, img), 'cutout': True, 'h': 1 / 16}
        elif any(base.startswith(c) or base.endswith(c) for c in CROSS):
            name = base
            if base == 'tall_grass':
                name = 'tall_grass_bottom' if lower else 'tall_grass_top'
            img = get(name) or get(base + ('_bottom' if lower else '_top')) or get('short_grass')
            if base.startswith(TINTED_PLANTS):
                img = extraer.tint(img, grass)
                name += sfx
            looks[full] = {'kind': 'cross', 'side': save(name, img)}
        elif base.endswith('_log') or base.endswith('_wood'):
            # Wood blocks are bark on every face: oak_wood uses oak_log's side texture
            name = base if get(base) else base.replace('_wood', '_log')
            top = (get(base + '_top') or get(base)) if name == base else get(name)
            looks[full] = {'kind': 'cube', 'axis': full.split('axis=')[1][0] if 'axis=' in full else 'y',
                           'top': save(name + ('_top' if name == base else ''), top), 'side': save(name, get(name))}
        elif base.endswith('leaves'):
            img, key = get(base), base
            if base in ('oak_leaves', 'jungle_leaves', 'acacia_leaves', 'dark_oak_leaves', 'mangrove_leaves'):
                img, key = extraer.tint(img, foliage), base + sfx
            elif base in LEAF_TINTS:
                img = extraer.tint(img, LEAF_TINTS[base])
            looks[full] = {'kind': 'cube', 'side': save(key, img), 'cutout': True}
        elif base.endswith('carpet'):
            # A thin layer on the ground
            looks[full] = {'kind': 'cube', 'side': save(base, get(base) or get(base.replace('_carpet', '_block'))), 'h': 1 / 16}
        elif base in CROPS or base.endswith('torch'):
            name = CROPS.get(base, 'torch')
            looks[full] = {'kind': 'cross', 'side': save(name, get(name))}
        elif base in ('farmland', 'dirt_path'):
            top = save(base + '_top', get(base + '_moist') or get(base + '_top'))
            looks[full] = {'kind': 'cube', 'top': top, 'side': save('dirt', get('dirt')), 'h': 15 / 16}
            if base == 'dirt_path':
                looks[full]['side'] = save('dirt_path_side', get('dirt_path_side'))
        elif base.endswith('_slab') and material(base, get):
            key, img = material(base, get)
            looks[full] = {'kind': 'cube', 'side': save(key, img)}
            if 'type=double' not in full:
                looks[full]['h'] = 0.5
                if 'type=top' in full:
                    looks[full]['y0'] = 0.5
        elif base.endswith('_stairs') and material(base, get):
            key, img = material(base, get)
            looks[full] = {'kind': 'cube', 'side': save(key, img)}
        elif (base.endswith('_fence') or base.endswith('_fence_gate') or base.endswith('_wall')) and material(base, get):
            key, img = material(base, get)
            w = 0.5 if base.endswith('_wall') else 0.25
            looks[full] = {'kind': 'cube', 'side': save(key, img), 'box': [w, 1, w]}
        elif base.endswith('_door') and get(base + ('_top' if 'half=upper' in full else '_bottom')):
            half = '_top' if 'half=upper' in full else '_bottom'
            # A closed door is a 3/16 panel across its facing axis
            along_x = 'facing=north' in full or 'facing=south' in full
            looks[full] = {'kind': 'cube', 'side': save(base + half, get(base + half)), 'cutout': True,
                           'box': [1, 1, 3 / 16] if along_x else [3 / 16, 1, 1]}
        elif base.endswith('glass_pane') or base.endswith('glass'):
            name = base.replace('_pane', '')
            looks[full] = {'kind': 'cube', 'side': save(name, get(name) or get('glass')), 'cutout': True}
        elif base == 'lily_pad':
            looks[full] = {'kind': 'cube', 'side': save(base, extraer.tint(get(base), (32, 128, 48))), 'cutout': True,
                           'h': 1 / 16}
        elif any(w in base for w in NO_LOOK) and base != 'jack_o_lantern':
            looks[full] = {'kind': 'skip'}
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
