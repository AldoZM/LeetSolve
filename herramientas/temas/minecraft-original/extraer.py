# Copies the textures, GUI sprites, font and sounds this theme needs from the local Minecraft Java install.
# The game's files are not redistributable: the generated folders (tex/, gui/, font/, sounds/) stay out of any repo.
# Usage: python extraer.py [version]   (default: the newest version folder with a jar)
import json
import os
import sys
import zipfile
from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
MC = os.path.expandvars(r'%APPDATA%\.minecraft') if os.name == 'nt' else os.path.expanduser(
    '~/Library/Application Support/minecraft' if sys.platform == 'darwin' else '~/.minecraft')
A = 'assets/minecraft/'

GRASS_TINT = (145, 189, 89)    # plains grass
FOLIAGE_TINT = (119, 171, 47)  # plains foliage

BLOCKS = {  # output name -> texture inside the jar
    'coal_ore': 'block/coal_ore', 'iron_ore': 'block/iron_ore', 'gold_ore': 'block/gold_ore',
    'diamond_ore': 'block/diamond_ore', 'lapis_ore': 'block/lapis_ore', 'redstone_ore': 'block/redstone_ore',
    'emerald_ore': 'block/emerald_ore', 'stone': 'block/stone', 'dirt': 'block/dirt', 'planks': 'block/oak_planks',
    'gold_block': 'block/gold_block', 'log_side': 'block/oak_log', 'log_top': 'block/oak_log_top',
    'cobble': 'block/cobblestone', 'barrier': 'item/barrier', 'writable_book': 'item/writable_book',
    'redstone_lamp': 'block/redstone_lamp', 'redstone_lamp_on': 'block/redstone_lamp_on',  # bits (#3644)
    'lever': 'block/lever',  # the two moves (#3942)
    'clock': 'item/clock_00',  # dates (#2409)
    'shears': 'item/shears', 'lead': 'item/lead', 'hopper': 'item/hopper',  # cut a subtree, DFS rope, BST funnel
    'oak_sapling': 'block/oak_sapling', 'compass': 'item/compass_16',  # tree basics
    # DNS village (videos/tech/dns): buildings, the lectern and the items that travel between libraries
    **{n: f'block/{n}' for n in ('bookshelf', 'oak_planks', 'glass', 'dirt_path_top', 'dirt_path_side', 'stone_bricks',
                                 'chiseled_stone_bricks', 'smooth_stone', 'lectern_base', 'lectern_front', 'lectern_sides',
                                 'lectern_top', 'tnt_side', 'tnt_top', 'tnt_bottom', 'white_wool', 'red_wool', 'blue_wool',
                                 'yellow_wool', 'lime_wool', 'gray_wool', 'black_wool', 'quartz_block_side',
                                 'quartz_block_top', 'iron_block', 'emerald_block', 'oak_trapdoor')},
    'written_book': 'item/written_book', 'paper': 'item/paper', 'filled_map': 'item/filled_map',
    'enchanted_book': 'item/enchanted_book', 'glint': 'misc/enchanted_glint_item',
    # HTTPS and TLS (videos/tech/https-tls): paint mixing for the key exchange, the name tag and the padlock
    **{n: f'block/{n}' for n in ('orange_wool', 'green_wool', 'brown_wool', 'cauldron_side', 'cauldron_top')},
    **{n: f'item/{n}' for n in ('name_tag', 'red_dye', 'blue_dye', 'yellow_dye', 'orange_dye', 'green_dye', 'brown_dye',
                               'emerald')},
    'padlock': 'gui/sprites/container/cartography_table/locked',
    # Packets (videos/tech/packets): rails, the minecart entity (64 x 32) and the 2 x 2 painting cut into four packets
    'rail': 'block/rail', 'rail_corner': 'block/rail_corner', 'minecart': 'entity/minecart/minecart',
    'painting_bust': 'painting/bust', 'painting_back': 'painting/back',
    # Server (videos/tech/server): the hopper line, the worker's furnace (500) and its fire
    **{n: f'block/{n}' for n in ('hopper_outside', 'hopper_top', 'hopper_inside', 'furnace_front', 'furnace_front_on',
                                 'furnace_side', 'furnace_top')},
    'fire': 'block/fire_0',
    # Kafka (videos/tech/kafka): the sword Steve buys, the event of the shop
    'iron_sword': 'item/iron_sword',
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
    'shear': 'mob/sheep/shear', 'lead_tie': 'entity/leashknot/leash1',  # tree basics: shears and lead
    # DNS village
    **{f'villager_yes{k}': f'mob/villager/yes{k}' for k in range(1, 4)},
    **{f'villager_idle{k}': f'mob/villager/idle{k}' for k in range(1, 4)},
    **{f'explode{k}': f'random/explode{k}' for k in range(1, 5)}, 'fuse': 'random/fuse',
    'illusioner_idle': 'mob/illusion_illager/idle1', 'illusioner_mirror': 'mob/illusion_illager/prepare_mirror',
    'trader_idle': 'mob/wandering_trader/idle1', 'door_open': 'random/door_open', 'chest_locked': 'block/chest/close_locked',
    # Packets: minecarts rolling, a cart thrown away, the painting pieces put on the wall, the station bell
    'minecart_roll': 'minecart/base', 'fizz': 'random/fizz', 'painting_place': 'entity/painting/place1',
    'frame_add': 'entity/itemframe/add_item1', 'bell': 'note/bell',
    # Server: the golem that stops a flood of notes, the status stamp, the broken furnace
    'golem_hit': 'mob/irongolem/hit1', 'anvil_land': 'random/anvil_land', 'fire': 'fire/fire',
}
# Mobs walking around the 3D background (vida.js), plus the moon for night scenes
MOBS = {
    'cow': 'entity/cow/cow_temperate', 'pig': 'entity/pig/pig_temperate', 'sheep': 'entity/sheep/sheep',
    'sheep_wool': 'entity/sheep/sheep_wool', 'chicken': 'entity/chicken/chicken_temperate', 'wolf': 'entity/wolf/wolf',
    'squid': 'entity/squid/squid', 'zombie': 'entity/zombie/zombie', 'skeleton': 'entity/skeleton/skeleton',
    'creeper': 'entity/creeper/creeper', 'spider': 'entity/spider/spider', 'spider_eyes': 'entity/spider/spider_eyes',
    'iron_golem': 'entity/iron_golem/iron_golem',  # the rate limiter of the server short (128 x 128)
    'moon': 'environment/celestial/moon/full_moon',
}
# People for the all-3D videos (gente.js): villager layers (base, biome type, profession), players, illagers, trader
GENTE = {
    'villager': 'entity/villager/villager',
    **{f'type_{n}': f'entity/villager/type/{n}' for n in ('plains', 'desert', 'taiga', 'snow', 'savanna')},
    **{f'prof_{n}': f'entity/villager/profession/{n}' for n in ('librarian', 'cartographer', 'cleric', 'mason', 'nitwit')},
    'steve': 'entity/player/wide/steve', 'alex': 'entity/player/wide/alex',
    'illusioner': 'entity/illager/illusioner', 'vindicator': 'entity/illager/vindicator',
    'wandering_trader': 'entity/wandering_trader/wandering_trader',
}
# Block models drawn as 2D icons by model_icon() in tema.py: the model json and every texture it uses go to models/<name>/
MODELS = {'lever': 'block/lever', 'lever_on': 'block/lever_on'}
# Background music (video.json "musica"); C418's tracks get copyright claims on YouTube, see GUIA.md
MUSIC = {n: f'music/game/{n}' for n in ('subwoofer_lullaby', 'sweden', 'mice_on_venus', 'haggstrom', 'wet_hands', 'danny',
                                         'clark', 'minecraft', 'dry_hands', 'living_mice')}


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
    for d in ('tex', 'gui', 'font', 'sounds', 'music', 'mobs', 'models', 'gente'):
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
    for name, p in MOBS.items():
        tex(p).save(os.path.join(HERE, 'mobs', f'{name}.png'))
    for name, p in GENTE.items():
        tex(p).save(os.path.join(HERE, 'gente', f'{name}.png'))

    # Models, resolving the parent chain; textures keep their game names ("block/cobblestone" -> cobblestone.png)
    for name, p in MODELS.items():
        model, cur = {}, p
        while cur:
            m = json.loads(jar.read(f'{A}models/{cur.split(":")[-1]}.json'))
            model = {**m, **model, 'textures': {**m.get('textures', {}), **model.get('textures', {})}}
            cur = m.get('parent') if 'elements' not in model else None
        out = os.path.join(HERE, 'models', name)
        os.makedirs(out, exist_ok=True)
        for ref in model['textures'].values():
            if not ref.startswith('#'):
                path = ref.split(':')[-1]
                tex(path).save(os.path.join(out, path.split('/')[-1] + '.png'))
        json.dump(model, open(os.path.join(out, 'model.json'), 'w'), indent=1)

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
    print(f'version {version}: {len(BLOCKS) + 3} block textures, {len(GUI)} gui images, {len(MOBS)} mob textures, font, '
          f'{len(SOUNDS) + len(MUSIC) - len(missing)} sounds and music' + (f' (missing: {missing})' if missing else ''))


if __name__ == '__main__':
    main()
