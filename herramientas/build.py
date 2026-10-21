# Builds one LeetCode video in the current session folder.
# Needs video.json: {"groups": [["Scene1_Hook", [0]], ...], "three": {"scene": "Scene5_Walk", "page": "three/walk.html"}}
# or, for one 3D world behind the whole video: "fondo": {"page": "three/mundo.html", "sharp": ["Scene5_Walk"]}
#   ("formato": "9:16" with "fondo" gives a 1080 x 1920 video; the scenes stay 1080 x 1440 in the middle)
#   (every scene renders transparent over its slice of that clip; scenes not listed in "sharp" get the world blurred)
# Usage: python build.py [script] [lint] [render [Scene ...]] [three] [composite] [sync [Scene ...]] [mux]   (no args = all)
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))
# tts-generate.py and lint-subtitles.py from github.com/Yusuke710/manim-skill (override with MANIM_SKILL_TOOLS)
TOOLS = os.environ.get('MANIM_SKILL_TOOLS', os.path.expanduser('~/.manim-skill-src/skills/manim-skill/tools'))
RENDER3D = os.path.join(HERE, 'three', 'render.mjs')  # needs `npm ci` in herramientas/three
LIB3D = os.path.join(HERE, 'three')  # stage.js, served as /vendor/lib/
OUT = 'media/videos/script/1440p30'

cfg = json.load(open('video.json'))
groups = cfg['groups']
three = cfg.get('three')
fondo = cfg.get('fondo')
# Optional visual theme: herramientas/temas/<name>/ with tema.py (Manim) and assets for the 3D page
TEMA = os.path.join(HERE, 'temas', cfg['tema']) if cfg.get('tema') else None
names = [g[0] for g in groups]
# "formato": "9:16" makes a 1080 x 1920 video: the 3D world is rendered taller and every 1080 x 1440 scene sits centered on it
TALL = cfg.get('formato') == '9:16'
SIZE3D = ['--width', '1080', '--height', '1920'] if TALL else []
TOP = 240 if TALL else 0


def run(cmd, **kw):
    print('>', ' '.join(cmd) if isinstance(cmd, list) else cmd, flush=True)
    subprocess.run(cmd, check=True, **kw)


def frame_bounds():
    # Same quantization for every step: scene k covers frames [round(cum_{k-1}*FPS), round(cum_k*FPS))
    ts = json.load(open('timestamps.json'))['subtitles']
    cum, prev, out = 0.0, 0, {}
    for name, ix in groups:
        cum += sum(ts[i]['duration_s'] for i in ix)
        end = round(cum * FPS)
        out[name] = (prev, end)
        prev = end
    return out


def count_frames(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries',
                        'stream=nb_read_frames', '-of', 'csv=p=0', path], capture_output=True, text=True)
    return int(r.stdout.strip())


def step_script():
    body = open('scenes.py', encoding='utf-8').read()
    pre = open(os.path.join(HERE, 'prelude.py'), encoding='utf-8').read()
    if TEMA:
        tema = open(os.path.join(TEMA, 'tema.py'), encoding='utf-8').read()
        # A theme can build on another one with a first line "# extends: <name>"; the base goes in first
        first = tema.splitlines()[0]
        if first.startswith('# extends:'):
            base_dir = os.path.join(HERE, 'temas', first.split(':', 1)[1].strip())
            base = open(os.path.join(base_dir, 'tema.py'), encoding='utf-8').read()
            pre += f'\nTEMA_DIR = {base_dir.replace(os.sep, "/")!r}\n' + base
        pre += f'\nTEMA_DIR = {TEMA.replace(os.sep, "/")!r}\n' + tema
    if fondo:
        pre += '\nFONDO = True\n'
    open('script.py', 'w', encoding='utf-8').write(pre + '\n' + body)


def step_lint():
    run([sys.executable, os.path.join(TOOLS, 'lint-subtitles.py'), 'script.py'])


def step_render(only):
    todo = only or names
    overlay = three['scene'] if three else None

    def one(name):
        flags = ['-t'] if name == overlay or fondo else []
        # The scene rewrites its own cues while rendering; drop stale ones first
        if os.path.exists(f'media/sfx/{name}.json'):
            os.remove(f'media/sfx/{name}.json')
        log = open(f'media/log_{name}.txt', 'w')
        r = subprocess.run(['manim', *flags, 'script.py', name], stdout=log, stderr=subprocess.STDOUT)
        print(name, 'ok' if r.returncode == 0 else f'FAILED (see media/log_{name}.txt)', flush=True)
        return r.returncode

    os.makedirs('media', exist_ok=True)
    with ThreadPoolExecutor(3) as ex:
        codes = list(ex.map(one, todo))
    # Parallel renders can race on Manim's shared text cache; retry failures one at a time
    codes = [one(n) if c else 0 for n, c in zip(todo, codes)]
    if any(codes):
        sys.exit(1)


def step_three():
    os.makedirs('media/three', exist_ok=True)
    extra = ['--tema', TEMA] if TEMA else []
    if fondo:
        total = frame_bounds()[names[-1]][1]
        run(['node', RENDER3D, '--page', fondo['page'], '--lib', LIB3D, *extra, *SIZE3D, '--frames', str(total), '--out',
             'media/three/fondo.mp4'])
        return
    a, b = frame_bounds()[three['scene']]
    run(['node', RENDER3D, '--page', three['page'], '--lib', LIB3D, *extra, '--frames', str(b - a), '--out', 'media/three/clip3d.mp4'])


def step_composite_fondo(only):
    # Each scene over its own slice of the world clip; blurred and dimmed unless the scene is listed as sharp
    for name in only or names:
        a, b = frame_bounds()[name]
        n = b - a
        ov = f'{OUT}/{name}.mov'
        pad = max(0, n - count_frames(ov))
        look = '' if name in fondo.get('sharp', []) else ',gblur=sigma=5,colorchannelmixer=rr=0.82:gg=0.82:bb=0.82'
        run(['ffmpeg', '-v', 'error', '-y', '-i', 'media/three/fondo.mp4', '-i', ov, '-filter_complex',
             f'[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS{look}[bg];'
             f'[1:v]tpad=stop_mode=clone:stop={pad + 2}[ov];[bg][ov]overlay=x=0:y={TOP}:format=auto:eof_action=repeat,format=yuv420p[v]',
             '-map', '[v]', '-frames:v', str(n), '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-r', str(FPS),
             f'{OUT}/{name}.mp4'])


def step_composite():
    name = three['scene']
    a, b = frame_bounds()[name]
    n = b - a
    ov = f'{OUT}/{name}.mov'
    pad = max(0, n - count_frames(ov))
    run(['ffmpeg', '-v', 'error', '-y', '-i', 'media/three/clip3d.mp4', '-i', ov, '-filter_complex',
         f'[1:v]tpad=stop_mode=clone:stop={pad + 2}[ov];[0:v][ov]overlay=format=auto:eof_action=repeat,format=yuv420p[v]',
         '-map', '[v]', '-frames:v', str(n), '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-r', str(FPS),
         f'{OUT}/{name}.mp4'])


def step_sync(only):
    bounds = frame_bounds()
    os.makedirs('media/synced', exist_ok=True)
    lines = []
    for name in names:
        dst = f'media/synced/{name}.mp4'
        lines.append(f"file '{dst}'")
        if only and name not in only:
            continue
        src = f'{OUT}/{name}.mp4'
        a, b = bounds[name]
        n = count_frames(src)
        pad = (b - a) - n
        vf = f'tpad=stop_mode=clone:stop={pad}' if pad > 0 else 'null'
        run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', vf, '-frames:v', str(b - a), '-c:v', 'libx264', '-crf', '16',
             '-preset', 'slow', '-pix_fmt', 'yuv420p', '-r', str(FPS), dst])
        srt = src.replace('.mp4', '.srt')
        if os.path.exists(srt):
            open(dst.replace('.mp4', '.srt'), 'wb').write(open(srt, 'rb').read())
        print(name, 'frames', n, 'pad', pad)
    open('concat.txt', 'w').write('\n'.join(lines) + '\n')


def sfx_cues():
    # Sound effects queued by the scenes with self.sfx(); files come from the theme's sounds/ folder
    cues = []
    for name in names:
        p = f'media/sfx/{name}.json'
        if os.path.exists(p):
            cues += json.load(open(p))
    if cues and not TEMA:
        sys.exit('sfx cues need a theme with a sounds/ folder')
    return cues


def step_mux():
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'concat.txt', '-c', 'copy', '-movflags', '+faststart',
         'video_silent.mp4'])
    cues = sfx_cues()
    # Optional background music from the theme: "musica": {"pista": "<name>", "volumen": 0.45} (music/<name>.ogg)
    musica = cfg.get('musica')
    if not cues and not musica:
        run(['ffmpeg', '-v', 'error', '-y', '-i', 'video_silent.mp4', '-i', 'voiceover.mp3', '-map', '0:v:0', '-map', '1:a:0',
             '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', 'video.mp4'])
    else:
        # Voice plus every cue delayed to its time; amix without normalizing keeps the voice level unchanged.
        # Mono throughout: upmixing the mono voice to stereo would lower it by 3 dB
        ins, parts = [], []
        for k, (t, sound, gain) in enumerate(cues):
            ins += ['-i', os.path.join(TEMA, 'sounds', f'{sound}.ogg')]
            ms = max(0, int(t * 1000))
            parts.append(f'[{k + 2}:a]aresample=44100,aformat=channel_layouts=mono,adelay={ms},volume={gain}[s{k}]')
        mix = ''.join(f'[s{k}]' for k in range(len(cues)))
        if musica:
            # Fades in and out so the video still loops without a jump in the music
            total = json.load(open('timestamps.json'))['total_duration_s']
            k = len(cues)
            ins += ['-i', os.path.join(TEMA, 'music', f"{musica['pista']}.ogg")]
            parts.append(f"[{k + 2}:a]aresample=44100,aformat=channel_layouts=mono,atrim=0:{total},afade=t=in:d=2,"
                         f"afade=t=out:st={total - 3}:d=3,volume={musica.get('volumen', 0.45)}[s{k}]")
            mix += f'[s{k}]'
        n = len(cues) + (1 if musica else 0)
        graph = ';'.join(parts) + f';[1:a]aresample=44100,aformat=channel_layouts=mono[v];[v]{mix}amix=inputs={n + 1}:normalize=0:duration=first[a]'
        open('media/sfx_graph.txt', 'w').write(graph)
        run(['ffmpeg', '-v', 'error', '-y', '-i', 'video_silent.mp4', '-i', 'voiceover.mp3', *ins, '-filter_complex_script',
             'media/sfx_graph.txt', '-map', '0:v:0', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
             '-movflags', '+faststart', 'video.mp4'])
        print(len(cues), 'sound effects mixed' + (f", music {musica['pista']}" if musica else ''))
    v = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'video.mp4'],
                       capture_output=True, text=True).stdout.strip()
    print('video.mp4 duration', v, 'audio', json.load(open('timestamps.json'))['total_duration_s'])


args = sys.argv[1:] or ['script', 'lint', 'render', 'three', 'composite', 'sync', 'mux']
steps = {'script', 'lint', 'render', 'three', 'composite', 'sync', 'mux'}
i = 0
while i < len(args):
    s = args[i]
    extra = []
    while i + 1 < len(args) and args[i + 1] not in steps:
        i += 1
        extra.append(args[i])
    if s == 'script':
        step_script()
    elif s == 'lint':
        step_lint()
    elif s == 'render':
        step_render(extra)
    elif s == 'three':
        step_three()
    elif s == 'composite':
        step_composite_fondo(extra) if fondo else step_composite()
    elif s == 'sync':
        step_sync(extra)
    elif s == 'mux':
        step_mux()
    i += 1
