# Copies the textures, GUI sprites, font and sounds this theme needs from the local Minecraft Java install.
# The game's files are not redistributable: the generated folders (tex/, gui/, font/, sounds/) stay out of any repo.
# Usage: python extraer.py [version]   (default: the newest version folder with a jar)
import json
import os
import sys
import zipfile
from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
MC = os.path.expandvars(r'%APPDATA%\.minecraft')
A = 'assets/minecraft/'

GRASS_TINT = (145, 189, 89)    # plains grass
FOLIAGE_TINT = (119, 171, 47)  # plains foliage

BLOCKS = {  # output name -> texture inside the jar
    'coal_ore': 'block/coal_ore', 'iron_ore': 'block/iron_ore', 'gold_ore': 'block/gold_ore',
    'diamond_ore': 'block/diamond_ore', 'lapis_ore': 'block/lapis_ore', 'redstone_ore': 'block/redstone_ore',
    'emerald_ore': 'block/emerald_ore', 'stone': 'block/stone', 'dirt': 'block/dirt', 'planks': 'block/oak_planks',
    'gold_block': 'block/gold_block', 'log_side': 'block/oak_log', 'log_top': 'block/oak_log_top',
    'cobble': 'block/cobblestone', 'barrier': 'item/barrier', 'writable_book': 'item/writable_book',
}
GUI = {
    'generic_54': 'gui/container/generic_54', 'hotbar': 'gui/sprites/hud/hotbar',
    'hotbar_selection': 'gui/sprites/hud/hotbar_selection', 'xp_bg': 'gui/sprites/hud/experience_bar_background',
    'xp_fill': 'gui/sprites/hud/experience_bar_progress', 'toast': 'gui/sprites/toast/advancement',
    'slot': 'gui/sprites/container/slot', 'pickaxe': 'item/diamond_pickaxe', 'orb': 'entity/experience/experience_orb',
    'clouds': 'environment/clouds', 'sun': 'environment/celestial/sun', 'chest_atlas': 'entity/chest/normal',
}
SOUNDS = {
    'chestopen': 'random/chestopen', 'chestclosed': 'random/chestclosed', 'pop': 'random/pop', 'orb': 'random/orb',
    'levelup': 'random/levelup', 'break': 'random/break', 'click': 'random/click',
    'challenge': 'ui/toast/challenge_complete', 'toast_in': 'ui/toast/in',
    **{f'stone_dig{k}': f'dig/stone{k}' for k in range(1, 5)}, **{f'stone_step{k}': f'step/stone{k}' for k in range(1, 7)},
    **{f'wood_dig{k}': f'dig/wood{k}' for k in range(1, 5)},
    **{f'book_flip{k}': f'item/book/open_flip{k}' for k in range(1, 4)}, 'book_put': 'item/book/close_put1',
    **{f'villager_no{k}': f'mob/villager/no{k}' for k in range(1, 4)},
}
# Background music (video.json "musica"); C418's tracks get copyright claims on YouTube, see GUIA.md
MUSIC = {'subwoofer_lullaby': 'music/game/subwoofer_lullaby'}


def newest_version():
    vs = []
    for v in os.listdir(os.path.join(MC, 'versions')):
        jar = os.path.join(MC, 'versions', v, v + '.jar')
        if os.path.exists(jar) and not v.startswith(('fabric', 'forge', 'quilt')):
            vs.append((os.path.getmtime(jar), v))
    return max(vs)[1]


def tint(img, rgb):
    # Multiplies a grayscale texture by a biome color, keeping its alpha
    img = img.convert('RGBA')
    color = Image.new('RGBA', img.size, rgb + (255,))
    out = ImageChops.multiply(img, color)
    out.putalpha(img.getchannel('A'))
    return out


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else newest_version()
    jar = zipfile.ZipFile(os.path.join(MC, 'versions', version, version + '.jar'))
    tex = lambda p: Image.open(jar.open(f'{A}textures/{p}.png')).convert('RGBA')
    for d in ('tex', 'gui', 'font', 'sounds', 'music'):
        os.makedirs(os.path.join(HERE, d), exist_ok=True)

    for name, p in BLOCKS.items():
        tex(p).save(os.path.join(HERE, 'tex', f'{name}.png'))
    tint(tex('block/grass_block_top'), GRASS_TINT).save(os.path.join(HERE, 'tex', 'grass_top.png'))
    side = tex('block/grass_block_side')
    side.alpha_composite(tint(tex('block/grass_block_side_overlay'), GRASS_TINT))
    side.save(os.path.join(HERE, 'tex', 'grass_side.png'))
    tint(tex('block/oak_leaves'), FOLIAGE_TINT).save(os.path.join(HERE, 'tex', 'leaves.png'))
    for name, p in GUI.items():
        tex(p).save(os.path.join(HERE, 'gui', f'{name}.png'))

    # Chest front for 2D icons: lid front + body front + latch, from the entity atlas (box UV layout)
    atlas = tex('entity/chest/normal')
    front = Image.new('RGBA', (14, 15), (0, 0, 0, 0))
    lid = atlas.crop((14, 14, 28, 19))
    body = atlas.crop((14, 33, 28, 43))
    latch = atlas.crop((1, 1, 3, 5))
    front.paste(lid, (0, 0))
    front.paste(body, (0, 5))
    front.alpha_composite(latch, (6, 2))
    front.save(os.path.join(HERE, 'tex', 'chest_front.png'))

    # Font: ascii.png and the character rows from the default font definition
    jar_font = json.loads(jar.read(f'{A}font/include/default.json'))
    prov = next(p for p in jar_font['providers'] if p.get('file', '').endswith('font/ascii.png'))
    tex('font/ascii').save(os.path.join(HERE, 'font', 'ascii.png'))
    json.dump({'chars': prov['chars'], 'ascent': prov.get('ascent', 7), 'height': prov.get('height', 8)},
              open(os.path.join(HERE, 'font', 'ascii.json'), 'w', encoding='utf-8'), ensure_ascii=False)

    # Sounds live outside the jar, in the hashed object store of the matching asset index
    index_id = json.load(open(os.path.join(MC, 'versions', version, version + '.json')))['assetIndex']['id']
    objects = json.load(open(os.path.join(MC, 'assets', 'indexes', index_id + '.json')))['objects']
    missing = []
    for folder, table in (('sounds', SOUNDS), ('music', MUSIC)):
        for name, p in table.items():
            entry = objects.get(f'minecraft/sounds/{p}.ogg')
            if not entry:
                missing.append(p)
                continue
            h = entry['hash']
            with open(os.path.join(MC, 'assets', 'objects', h[:2], h), 'rb') as src:
                open(os.path.join(HERE, folder, f'{name}.ogg'), 'wb').write(src.read())
    print(f'version {version}: {len(BLOCKS) + 3} block textures, {len(GUI)} gui images, font, '
          f'{len(SOUNDS) + len(MUSIC) - len(missing)} sounds and music' + (f' (missing: {missing})' if missing else ''))


if __name__ == '__main__':
    main()
