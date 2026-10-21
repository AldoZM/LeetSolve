// Minecraft theme for the three.js clips: pixel textures, blocks, chest, signs and a daytime world.
// Served as /vendor/tema/mc.js; textures and fonts come from the same folder (original art, OFL fonts).
import { THREE, prog, V } from '/vendor/lib/stage.js';

export const SKY_TOP = 0x4A7FE0;
export const SKY_BOTTOM = 0xA6C8F8;
export const MC = { white: 0xFFFFFF, gray: 0xAAAAAA, yellow: 0xFFFF55, gold: 0xFFAA00, green: 0x55FF55, aqua: 0x55FFFF,
                    red: 0xFF5555, xp: 0xB8FF3A };
const hex = (c) => '#' + c.toString(16).padStart(6, '0');

// Face shading like the game: top brightest, sides darker. BoxGeometry face order: +x, -x, +y, -y, +z, -z
const SHADE = [0.72, 0.72, 1.0, 0.5, 0.86, 0.78];

export async function loadTheme(names) {
  const fonts = [new FontFace('PressStart', 'url(/vendor/tema/fonts/PressStart2P-Regular.ttf)'),
                 new FontFace('VT323', 'url(/vendor/tema/fonts/VT323-Regular.ttf)')];
  for (const f of fonts) { await f.load(); document.fonts.add(f); }
  const imgs = {};
  await Promise.all(names.map((n) => new Promise((res, rej) => {
    const im = new Image();
    im.onload = () => { imgs[n] = im; res(); };
    im.onerror = () => rej(new Error('texture ' + n));
    im.src = `/vendor/tema/tex/${n}.png`;
  })));
  return imgs;
}

function nearest(tex) {
  tex.magFilter = THREE.NearestFilter;
  tex.minFilter = THREE.NearestMipmapLinearFilter;
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.needsUpdate = true;
  return tex;
}

// Pixel canvas: texture scaled up without smoothing, optional text drawn on top
function pixelCanvas(img, w, h, draw) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  const ctx = c.getContext('2d');
  ctx.imageSmoothingEnabled = false;
  if (img) {
    // Tile the 16px texture so it keeps square pixels on non-square canvases
    const s = h;
    for (let x = 0; x < w; x += s) ctx.drawImage(img, x, 0, s, s);
  }
  if (draw) draw(ctx);
  return c;
}

// Text with the game's hard shadow, one font pixel down and right
export function shadowText(ctx, text, x, y, px, color, font = 'PressStart') {
  const step = font === 'PressStart' ? px / 8 : px / 16;
  ctx.font = `${px}px ${font}`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  const c = new THREE.Color(color);
  ctx.fillStyle = `rgb(${c.r * 64},${c.g * 64},${c.b * 64})`;
  ctx.fillText(text, x + step, y + step);
  ctx.fillStyle = hex(color);
  ctx.fillText(text, x, y);
}

const cache = new Map();
export function tex(imgs, name) {
  if (!cache.has(name)) cache.set(name, nearest(new THREE.CanvasTexture(pixelCanvas(imgs[name], 16, 16))));
  return cache.get(name);
}

function faceMats(maps) {
  return maps.map((m, k) => {
    const mat = new THREE.MeshBasicMaterial({ map: m, transparent: true });
    mat.userData.shade = SHADE[k];
    mat.color.setScalar(SHADE[k]);
    return mat;
  });
}

// A block; `label` prints a value on the front face. set({glow, opacity}) brightens or fades it.
export function makeBlock(imgs, name, { size = 1, label = null, top = name, bottom = name, front = name } = {}) {
  let frontMap = tex(imgs, front);
  if (label !== null) {
    const c = pixelCanvas(imgs[front], 160, 160, (ctx) => {
      const s = String(label);
      const px = s.length > 1 ? 56 : 72;
      shadowText(ctx, s, 80 - px / 16, 84, px, MC.white);
    });
    frontMap = nearest(new THREE.CanvasTexture(c));
  }
  const side = tex(imgs, name);
  const mats = faceMats([side, side, tex(imgs, top), tex(imgs, bottom), frontMap, side]);
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(size, size, size), mats);
  const g = new THREE.Group();
  g.add(mesh);
  const b = { g, mesh, mats };
  b.set = ({ glow = 0, opacity = 1 } = {}) => {
    for (const m of mats) {
      m.color.setScalar(m.userData.shade * (1 + glow));
      m.opacity = opacity;
    }
    g.visible = opacity > 0.01;
  };
  return b;
}

export function makeGrass(imgs, size = 1) {
  return makeBlock(imgs, 'grass_side', { size, top: 'grass_top', bottom: 'dirt' });
}

// Flat ground of grass blocks, top surface at y = 0
export function makeGround(imgs, xs, zs) {
  const geo = new THREE.BoxGeometry(1, 1, 1);
  const mats = faceMats([tex(imgs, 'grass_side'), tex(imgs, 'grass_side'), tex(imgs, 'grass_top'), tex(imgs, 'dirt'),
                         tex(imgs, 'grass_side'), tex(imgs, 'grass_side')]);
  const g = new THREE.Group();
  for (let x = xs[0]; x <= xs[1]; x++) {
    for (let z = zs[0]; z <= zs[1]; z++) {
      const m = new THREE.Mesh(geo, mats);
      m.position.set(x, -0.5, z);
      g.add(m);
    }
  }
  return g;
}

export function makeTree(imgs, x, z, h = 4) {
  const g = new THREE.Group();
  const log = faceMats([tex(imgs, 'log_side'), tex(imgs, 'log_side'), tex(imgs, 'log_top'), tex(imgs, 'log_top'),
                        tex(imgs, 'log_side'), tex(imgs, 'log_side')]);
  const leaf = faceMats(Array(6).fill(tex(imgs, 'leaves')));
  const geo = new THREE.BoxGeometry(1, 1, 1);
  for (let y = 0; y < h; y++) { const m = new THREE.Mesh(geo, log); m.position.set(x, y + 0.5, z); g.add(m); }
  for (let dx = -2; dx <= 2; dx++) for (let dz = -2; dz <= 2; dz++) for (let dy = 0; dy < 2; dy++) {
    if (Math.abs(dx) === 2 && Math.abs(dz) === 2) continue;
    if (dx === 0 && dz === 0) continue;
    const m = new THREE.Mesh(geo, leaf); m.position.set(x + dx, h - 1 + dy + 0.5, z + dz); g.add(m);
  }
  for (let dx = -1; dx <= 1; dx++) for (let dz = -1; dz <= 1; dz++) {
    if (Math.abs(dx) + Math.abs(dz) === 2) continue;
    const m = new THREE.Mesh(geo, leaf); m.position.set(x + dx, h + 1.5, z + dz); g.add(m);
  }
  return g;
}

// Chest: body plus a lid hinged at the back edge; open(a) with a in [0, 1]
export function makeChest(imgs, size = 0.9) {
  const g = new THREE.Group();
  const bodyH = size * 0.68, lidH = size * 0.3;
  const plain = tex(imgs, 'chest_plain');
  const body = new THREE.Mesh(new THREE.BoxGeometry(size, bodyH, size), faceMats(Array(6).fill(plain)));
  body.position.y = bodyH / 2;
  const hinge = new THREE.Group();
  hinge.position.set(0, bodyH, -size / 2);
  const lid = new THREE.Mesh(new THREE.BoxGeometry(size, lidH, size), faceMats(Array(6).fill(plain)));
  lid.position.set(0, lidH / 2, size / 2);
  const latch = new THREE.Mesh(new THREE.BoxGeometry(size * 0.14, size * 0.24, size * 0.08),
                               new THREE.MeshBasicMaterial({ color: 0xc7c7c7 }));
  latch.position.set(0, 0, size + size * 0.03);
  hinge.add(lid, latch);
  // Dark inside, seen when the lid opens
  const inside = new THREE.Mesh(new THREE.PlaneGeometry(size * 0.86, size * 0.86), new THREE.MeshBasicMaterial({ color: 0x1b1006 }));
  inside.rotation.x = -Math.PI / 2;
  inside.position.y = bodyH + 0.002;
  g.add(body, inside, hinge);
  return { g, open: (a) => { hinge.rotation.x = -a * 0.9; } };
}

// Selection frame: 12 thin bars around a cube
export function makeFrame(size = 1.04, t = 0.04, color = MC.white) {
  const mat = new THREE.MeshBasicMaterial({ color, toneMapped: false, transparent: true });
  const g = new THREE.Group();
  const h = size / 2;
  const bar = (sx, sy, sz, x, y, z) => { const m = new THREE.Mesh(new THREE.BoxGeometry(sx, sy, sz), mat); m.position.set(x, y, z); g.add(m); };
  for (const a of [-h, h]) for (const b of [-h, h]) {
    bar(size + t, t, t, 0, a, b);
    bar(t, size + t, t, a, 0, b);
    bar(t, t, size + t, a, b, 0);
  }
  g.userData.mat = mat;
  return g;
}

// Wooden sign with black text; a plane that always faces +z
export function makeSign(imgs, lines, { w = 1.9, h = 0.95, px = 96, post: withPost = true } = {}) {
  const W = 320, H = Math.round(W * h / w);
  const c = pixelCanvas(imgs.planks, W, H, (ctx) => {
    ctx.strokeStyle = '#3b2410'; ctx.lineWidth = 10; ctx.strokeRect(5, 5, W - 10, H - 10);
    ctx.font = `${px}px VT323`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = '#000000';
    lines.forEach((s, k) => ctx.fillText(s, W / 2, H / 2 + (k - (lines.length - 1) / 2) * px * 0.82 + 4));
  });
  const mat = new THREE.MeshBasicMaterial({ map: nearest(new THREE.CanvasTexture(c)), transparent: true, side: THREE.DoubleSide });
  const board = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat);
  const post = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.6, 0.09), new THREE.MeshBasicMaterial({ color: 0x6b5032, transparent: true }));
  post.position.y = -h / 2 - 0.3;
  const g = new THREE.Group();
  g.add(board);
  if (withPost) g.add(post);
  g.userData.mats = [mat, post.material];
  return g;
}

// Pixel text sprite (faces the camera)
export function pixelSprite(text, color, height, font = 'PressStart') {
  const px = 64;
  const c = document.createElement('canvas');
  const ctx = c.getContext('2d');
  ctx.font = `${px}px ${font}`;
  c.width = Math.ceil(ctx.measureText(text).width + px * 0.6);
  c.height = Math.ceil(px * 1.5);
  shadowText(ctx, text, c.width / 2, c.height / 2, px, color, font);
  const t = nearest(new THREE.CanvasTexture(c));
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthWrite: false }));
  s.scale.set(height * c.width / c.height, height, 1);
  s.userData.base = s.scale.clone();
  s.setSize = (k) => s.scale.copy(s.userData.base).multiplyScalar(Math.max(k, 1e-4));
  return s;
}

// Experience orb: a small glowing cube
export function makeOrb(size = 0.16) {
  const mat = new THREE.MeshBasicMaterial({ color: MC.xp, toneMapped: false, transparent: true });
  return new THREE.Mesh(new THREE.BoxGeometry(size, size, size), mat);
}

// Banded vertical sky gradient, same bands as the Manim theme
export function skyCanvas(bands = 28) {
  const c = document.createElement('canvas');
  c.width = 4; c.height = 1440;
  const ctx = c.getContext('2d');
  const a = new THREE.Color(SKY_TOP), b = new THREE.Color(SKY_BOTTOM);
  for (let k = 0; k < bands; k++) {
    const col = a.clone().lerp(b, k / (bands - 1));
    ctx.fillStyle = '#' + col.getHexString();
    ctx.fillRect(0, Math.floor(k * c.height / bands), 4, Math.ceil(c.height / bands) + 1);
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.magFilter = THREE.NearestFilter;
  return t;
}

// Renderer, scene, camera, sky, fog and a fade plane that dissolves into the same sky at both ends of the clip
export function makeWorld({ fov = 40, offset = 0.2, fog = [26, 60] } = {}) {
  const params = new URLSearchParams(location.search);
  const W = Number(params.get('w') || 1080);
  const H = Number(params.get('h') || 1440);
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(W, H);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  document.body.appendChild(renderer.domElement);
  {
    const gl = renderer.getContext();
    const ext = gl.getExtension('WEBGL_debug_renderer_info');
    window.gpuInfo = ext ? gl.getParameter(ext.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER);
  }
  const scene = new THREE.Scene();
  const sky = skyCanvas();
  scene.background = sky;
  scene.fog = new THREE.Fog(SKY_BOTTOM, fog[0], fog[1]);
  const camera = new THREE.PerspectiveCamera(fov, W / H, 0.1, 200);
  if (offset) camera.setViewOffset(W, H, 0, H * offset, W, H);
  const fadeMat = new THREE.MeshBasicMaterial({ map: sky, transparent: true, depthTest: false, depthWrite: false });
  const fade = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), fadeMat);
  // Covers the whole (offset) view: sized from the frustum at its distance
  const dist = 0.5;
  const fh = 2 * dist * Math.tan(THREE.MathUtils.degToRad(fov / 2));
  fade.scale.set(fh * W / H * 1.02, fh * 1.02, 1);
  fade.position.set(0, -fh * offset, -dist);
  fade.renderOrder = 999;
  camera.add(fade);
  scene.add(camera);
  const look = (pos, target) => { camera.position.copy(pos); camera.lookAt(target); };
  const draw = (t, total, fin = 0.5, fout = 0.55) => {
    fadeMat.opacity = 1 - prog(t, 0, fin) + prog(t, total - fout, total - 0.05);
    fade.visible = fadeMat.opacity > 0.001;
    renderer.render(scene, camera);
  };
  return { W, H, renderer, scene, camera, look, draw };
}

// Blocky clouds drifting slowly along +x
export function makeClouds(seed = 3) {
  let s = seed;
  const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
  const mat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.85, fog: false });
  const g = new THREE.Group();
  for (let k = 0; k < 9; k++) {
    const c = new THREE.Group();
    const w = 3 + rnd() * 5, d = 2 + rnd() * 3;
    const main = new THREE.Mesh(new THREE.BoxGeometry(w, 0.6, d), mat);
    const bump = new THREE.Mesh(new THREE.BoxGeometry(w * 0.5, 0.6, d * 0.6), mat);
    bump.position.set(w * 0.15, 0.3, 0);
    c.add(main, bump);
    c.position.set(-30 + rnd() * 60, 9 + rnd() * 3, -14 - rnd() * 22);
    g.add(c);
  }
  g.drift = (t) => { g.position.x = 0.25 * t; };
  return g;
}

export { V };
