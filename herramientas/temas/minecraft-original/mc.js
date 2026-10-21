// Minecraft theme for the three.js clips, built from the game's own textures (copied by extraer.py).
// Served as /vendor/tema/mc.js; same API as the original-art theme (../minecraft/mc.js).
import { THREE, prog, V } from '/vendor/lib/stage.js';

export const SKY_TOP = 0x6B98F5;
export const SKY_BOTTOM = 0xB8D2FF;
export const MC = { white: 0xFFFFFF, gray: 0xAAAAAA, yellow: 0xFFFF55, gold: 0xFFAA00, green: 0x55FF55, aqua: 0x55FFFF,
                    red: 0xFF5555, black: 0x000000 };

// Face shading like the game: top brightest, sides darker. BoxGeometry face order: +x, -x, +y, -y, +z, -z
const SHADE = [0.62, 0.62, 1.0, 0.5, 0.8, 0.8];

const loadImg = (src) => new Promise((res, rej) => {
  const im = new Image();
  im.onload = () => res(im);
  im.onerror = () => rej(new Error(src));
  im.src = src;
});

// ---------- bitmap font (font/ascii.png) ----------
const font = { glyphs: new Map(), sheet: null, tinted: new Map() };

async function loadFont() {
  const sheet = await loadImg('/vendor/tema/font/ascii.png');
  const meta = await (await fetch('/vendor/tema/font/ascii.json')).json();
  const c = document.createElement('canvas');
  c.width = sheet.width; c.height = sheet.height;
  const ctx = c.getContext('2d');
  ctx.drawImage(sheet, 0, 0);
  const cell = sheet.width / 16;
  const data = ctx.getImageData(0, 0, c.width, c.height).data;
  meta.chars.forEach((row, r) => [...row].forEach((ch, col) => {
    if (ch === '\u0000') return;
    let w = 0;
    for (let x = 0; x < cell; x++) for (let y = 0; y < cell; y++) {
      if (data[((r * cell + y) * c.width + col * cell + x) * 4 + 3] > 0) w = Math.max(w, x + 1);
    }
    font.glyphs.set(ch, { sx: col * cell, sy: r * cell, w: w || 3 });
  }));
  font.glyphs.set(' ', { sx: 0, sy: 0, w: 3, blank: true });
  font.sheet = c;
  font.cell = cell;
}

function tintedSheet(color) {
  const key = color.toString(16);
  if (!font.tinted.has(key)) {
    const c = document.createElement('canvas');
    c.width = font.sheet.width; c.height = font.sheet.height;
    const ctx = c.getContext('2d');
    ctx.drawImage(font.sheet, 0, 0);
    ctx.globalCompositeOperation = 'source-in';
    ctx.fillStyle = '#' + color.toString(16).padStart(6, '0');
    ctx.fillRect(0, 0, c.width, c.height);
    font.tinted.set(key, c);
  }
  return font.tinted.get(key);
}

export function textWidth(s) {
  return [...s].reduce((a, ch) => a + (font.glyphs.get(ch) ?? font.glyphs.get('?')).w + 1, 0);
}

// Draws text centered on (x, y) with `scale` canvas pixels per font pixel and the game's hard shadow
export function drawText(ctx, s, x, y, scale, color, shadow = true) {
  ctx.imageSmoothingEnabled = false;
  const w = textWidth(s) * scale;
  const shade = new THREE.Color(color).multiplyScalar(0.25).getHex();
  const pass = (col, off) => {
    const sheet = tintedSheet(col);
    let cx = x - w / 2 + off;
    for (const ch of s) {
      const g = font.glyphs.get(ch) ?? font.glyphs.get('?');
      if (!g.blank) ctx.drawImage(sheet, g.sx, g.sy, font.cell, font.cell, cx, y - 4 * scale + off, font.cell * scale, font.cell * scale);
      cx += (g.w + 1) * scale;
    }
  };
  if (shadow) pass(shade, scale);
  pass(color, 0);
}

// ---------- textures ----------
export async function loadTheme(names) {
  await loadFont();
  const imgs = {};
  await Promise.all(names.map(async (n) => { imgs[n] = await loadImg(`/vendor/tema/tex/${n}.png`); }));
  for (const n of ['chest_atlas', 'orb', 'clouds', 'planks_sign']) {
    try { imgs[n] = await loadImg(`/vendor/tema/gui/${n}.png`); } catch { /* optional */ }
  }
  imgs.planks = imgs.planks ?? await loadImg('/vendor/tema/tex/planks.png');
  return imgs;
}

function nearest(tex) {
  tex.magFilter = THREE.NearestFilter;
  tex.minFilter = THREE.NearestMipmapLinearFilter;
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.needsUpdate = true;
  return tex;
}

function pixelCanvas(img, w, h, draw) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  const ctx = c.getContext('2d');
  ctx.imageSmoothingEnabled = false;
  if (img) for (let x = 0; x < w; x += h) ctx.drawImage(img, x, 0, h, h);
  if (draw) draw(ctx);
  return c;
}

const cache = new Map();
export function tex(imgs, name) {
  if (!cache.has(name)) cache.set(name, nearest(new THREE.CanvasTexture(pixelCanvas(imgs[name], 16, 16))));
  return cache.get(name);
}

function faceMats(maps, shade = SHADE) {
  return maps.map((m, k) => {
    const mat = new THREE.MeshBasicMaterial({ map: m, transparent: true, alphaTest: 0.1 });
    mat.userData.shade = shade[k];
    mat.color.setScalar(shade[k]);
    return mat;
  });
}

// A block; `label` prints a value on the front face with the game font
export function makeBlock(imgs, name, { size = 1, label = null, top = name, bottom = name, front = name } = {}) {
  let frontMap = tex(imgs, front);
  if (label !== null) {
    const c = pixelCanvas(imgs[front], 160, 160, (ctx) => {
      const s = String(label);
      drawText(ctx, s, 80 - 4, 84, s.length > 1 ? 8 : 10, MC.white);
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
    for (const m of mats) { m.color.setScalar(m.userData.shade * (1 + glow)); m.opacity = opacity; }
    g.visible = opacity > 0.01;
  };
  return b;
}

export function makeGround(imgs, xs, zs) {
  const geo = new THREE.BoxGeometry(1, 1, 1);
  const mats = faceMats([tex(imgs, 'grass_side'), tex(imgs, 'grass_side'), tex(imgs, 'grass_top'), tex(imgs, 'dirt'),
                         tex(imgs, 'grass_side'), tex(imgs, 'grass_side')]);
  const count = (xs[1] - xs[0] + 1) * (zs[1] - zs[0] + 1);
  const inst = new THREE.InstancedMesh(geo, mats, count);
  const m = new THREE.Matrix4();
  let k = 0;
  for (let x = xs[0]; x <= xs[1]; x++) for (let z = zs[0]; z <= zs[1]; z++) inst.setMatrixAt(k++, m.makeTranslation(x, -0.5, z));
  return inst;
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

// Box with the entity texture's box-UV layout (u, v = texture offset; w, h, d in texture pixels)
function boxUV(atlas, size, u, v, w, h, d, unit) {
  const geo = new THREE.BoxGeometry(w * unit, h * unit, d * unit);
  const S = size;
  // Entity models are y-down: the "top" strip of the layout is the underside, so top and bottom swap
  const rects = [
    [u + d + w, v + d, d, h],        // +x
    [u, v + d, d, h],                // -x
    [u + d + w, v, w, d],            // +y (top)
    [u + d, v, w, d],                // -y (bottom)
    [u + d, v + d, w, h],            // +z (front, toward the camera)
    [u + 2 * d + w, v + d, w, h],    // -z
  ];
  const uv = geo.attributes.uv;
  for (let f = 0; f < 6; f++) {
    const [x, y, rw, rh] = rects[f];
    for (let k = 0; k < 4; k++) {
      const i = f * 4 + k;
      const U = uv.getX(i), Vv = uv.getY(i);
      uv.setXY(i, (x + U * rw) / S, 1 - (y + (1 - Vv) * rh) / S);
    }
  }
  return geo;
}

// The chest entity: body, lid hinged at the back, latch; open(a) with a in [0, 1]
export function makeChest(imgs, size = 0.9) {
  const map = nearest(new THREE.CanvasTexture(pixelCanvas(null, 64, 64, (ctx) => ctx.drawImage(imgs.chest_atlas, 0, 0))));
  const unit = size / 14;
  const mats = () => faceMats(Array(6).fill(map));
  const g = new THREE.Group();
  const body = new THREE.Mesh(boxUV(imgs.chest_atlas, 64, 0, 19, 14, 10, 14, unit), mats());
  body.position.y = 5 * unit;
  const hinge = new THREE.Group();
  hinge.position.set(0, 10 * unit, -7 * unit);
  const lid = new THREE.Mesh(boxUV(imgs.chest_atlas, 64, 0, 0, 14, 5, 14, unit), mats());
  lid.position.set(0, 2.5 * unit, 7 * unit);
  const latch = new THREE.Mesh(boxUV(imgs.chest_atlas, 64, 0, 0, 2, 4, 1, unit), mats());
  latch.position.set(0, 0, 14.5 * unit);
  hinge.add(lid, latch);
  g.add(body, hinge);
  return { g, open: (a) => { hinge.rotation.x = -a * 0.95; } };
}

// The block outline the game draws around the targeted block: thin dark lines
export function makeFrame(size = 1.004, t = 0.022, color = MC.black) {
  const mat = new THREE.MeshBasicMaterial({ color, toneMapped: false, transparent: true, opacity: 0.75 });
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

// Oak sign board with black game-font text
export function makeSign(imgs, lines, { w = 1.9, h = 0.95, post: withPost = true } = {}) {
  const W = 384, H = Math.round(W * h / w);
  const c = pixelCanvas(imgs.planks, W, H, (ctx) => {
    ctx.fillStyle = 'rgba(0,0,0,0.12)'; ctx.fillRect(0, 0, W, H);
    ctx.strokeStyle = '#4a3418'; ctx.lineWidth = 12; ctx.strokeRect(6, 6, W - 12, H - 12);
    lines.forEach((s, k) => drawText(ctx, s, W / 2, H / 2 + (k - (lines.length - 1) / 2) * 60, 7, 0x000000, false));
  });
  const mat = new THREE.MeshBasicMaterial({ map: nearest(new THREE.CanvasTexture(c)), transparent: true, side: THREE.DoubleSide });
  const g = new THREE.Group();
  g.add(new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat));
  if (withPost) {
    const post = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.6, 0.09), faceMats(Array(6).fill(tex(imgs, 'log_side'))));
    post.position.y = -h / 2 - 0.3;
    g.add(post);
  }
  return g;
}

// Game-font sprite that faces the camera
export function pixelSprite(text, color, height) {
  const scale = 8;
  const c = document.createElement('canvas');
  c.width = (textWidth(text) + 2) * scale;
  c.height = 10 * scale;
  drawText(c.getContext('2d'), text, c.width / 2 - scale / 2, c.height / 2, scale, color);
  const t = nearest(new THREE.CanvasTexture(c));
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthWrite: false }));
  s.scale.set(height * c.width / c.height, height, 1);
  s.userData.base = s.scale.clone();
  s.setSize = (k) => s.scale.copy(s.userData.base).multiplyScalar(Math.max(k, 1e-4));
  return s;
}

// Experience orb sprite (frame k of the 4x4 atlas); tint(t) cycles its color like the game
export function makeOrb(imgs, size = 0.32, frame = 5) {
  const c = pixelCanvas(null, 16, 16, (ctx) => ctx.drawImage(imgs.orb, (frame % 4) * 16, Math.floor(frame / 4) * 16, 16, 16, 0, 0, 16, 16));
  const mat = new THREE.SpriteMaterial({ map: nearest(new THREE.CanvasTexture(c)), transparent: true, depthWrite: false });
  const s = new THREE.Sprite(mat);
  s.scale.set(size, size, 1);
  s.tint = (t) => {
    const f = t * 9;
    mat.color.setRGB((Math.sin(f) + 1) * 0.5, 1, (Math.sin(f + 4.19) + 1) * 0.1);
  };
  return s;
}

export function skyCanvas(bands = 28) {
  const c = document.createElement('canvas');
  c.width = 4; c.height = 1440;
  const ctx = c.getContext('2d');
  const a = new THREE.Color(SKY_TOP), b = new THREE.Color(SKY_BOTTOM);
  for (let k = 0; k < bands; k++) {
    ctx.fillStyle = '#' + a.clone().lerp(b, k / (bands - 1)).getHexString();
    ctx.fillRect(0, Math.floor(k * c.height / bands), 4, Math.ceil(c.height / bands) + 1);
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.magFilter = THREE.NearestFilter;
  return t;
}

export function makeWorld({ fov = 40, offset = 0.2, fog = [30, 70] } = {}) {
  const params = new URLSearchParams(location.search);
  const W = Number(params.get('w') || 1080);
  const HR = Number(params.get('h') || 1440);
  // Pages are laid out for a 3:4 picture (W x H). A taller render (9:16) keeps that picture as its middle band and
  // shows more world above and below: the view offsets the pages ask for are widened by `pad` on each side
  const H = Math.min(HR, Math.round(W * 4 / 3));
  const pad = (HR - H) / 2;
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(W, HR);
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
  const camera = new THREE.PerspectiveCamera(fov, W / H, 0.1, 300);
  if (pad) {
    const setView = camera.setViewOffset.bind(camera);
    camera.setViewOffset = (fw, fh, x, y, w, h) => setView(fw, fh, x, y - pad * fh / H, w, h + 2 * pad * fh / H);
  }
  if (offset || pad) camera.setViewOffset(W, H, 0, H * offset, W, H);
  const fadeMat = new THREE.MeshBasicMaterial({ map: sky, transparent: true, depthTest: false, depthWrite: false });
  const fade = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), fadeMat);
  const dist = 0.5;
  const fh = 2 * dist * Math.tan(THREE.MathUtils.degToRad(fov / 2));
  fade.scale.set(fh * W / H * 1.02, fh * 1.02, 1);
  fade.position.set(0, -fh * offset, -dist);
  fade.renderOrder = 999;
  camera.add(fade);
  scene.add(camera);
  const look = (pos, target) => { camera.position.copy(pos); camera.lookAt(target); };
  // Fades in at the start and out at the end of the clip; fin = fout = 0 for a clip that covers the whole video
  const draw = (t, total, fin = 0.5, fout = 0.55) => {
    fadeMat.opacity = fin > 0 || fout > 0 ? 1 - prog(t, 0, fin) + prog(t, total - fout, total - 0.05) : 0;
    fade.visible = fadeMat.opacity > 0.001;
    renderer.render(scene, camera);
  };
  // ndcY: how a y of the 3:4 picture shrinks in normalized device coordinates when the render is taller
  return { W, H, renderer, scene, camera, look, draw, ndcY: H / HR };
}

// Clouds from the game's cloud map: every white pixel is a flat cloud cell
export function makeClouds(imgs, { cell = 6, y = 16, x0 = 96, z0 = 40, nx = 36, nz = 22 } = {}) {
  const c = pixelCanvas(null, 256, 256, (ctx) => ctx.drawImage(imgs.clouds, 0, 0));
  const data = c.getContext('2d').getImageData(0, 0, 256, 256).data;
  const cells = [];
  for (let i = 0; i < nx; i++) for (let j = 0; j < nz; j++) {
    if (data[((z0 + j) * 256 + x0 + i) * 4 + 3] > 0) cells.push([i, j]);
  }
  const mat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.82, fog: false });
  const inst = new THREE.InstancedMesh(new THREE.BoxGeometry(cell, cell / 3, cell), mat, cells.length);
  const m = new THREE.Matrix4();
  cells.forEach(([i, j], k) => inst.setMatrixAt(k, m.makeTranslation((i - nx / 2) * cell, y, -12 - j * cell)));
  const g = new THREE.Group();
  g.add(inst);
  g.drift = (t) => { g.position.x = 0.3 * t; };
  return g;
}

// Terrain exported from a real world by mundo.py: one instanced mesh per block type.
// Block (x, y, z) relative to the export center sits at (x, y + 0.5, z): the center column's ground top is y = 0.
export async function makeTerrain(url, { turn = 0, plot = null, clear = null } = {}) {
  const d = await (await fetch(url)).json();
  // clear = [x0, x1, z0, z1] in scene coordinates: trees and plants there are removed (where the camera stands)
  if (clear) {
    const c = Math.cos(turn), s = Math.sin(turn);
    const tree = d.names.map((n) => d.looks[n].cutout || d.looks[n].kind === 'cross' || /_log|_wood/.test(n));
    d.blocks = d.blocks.filter(([x, , z, n]) => {
      const sx = c * x + s * z, sz = -s * x + c * z;
      return !(tree[n] && sx >= clear[0] && sx <= clear[1] && sz >= clear[2] && sz <= clear[3]);
    });
  }
  // plot = [x0, x1, z0, z1] in scene coordinates: leveled to a grass floor whose top is y = 0, like a player would build
  if (plot) {
    const c = Math.cos(turn), s = Math.sin(turn);
    const inPlot = (x, z) => {
      const sx = c * x + s * z, sz = -s * x + c * z;  // terrain -> scene coordinates
      return sx >= plot[0] && sx <= plot[1] && sz >= plot[2] && sz <= plot[3];
    };
    const idx = (n) => d.names.indexOf(n);
    const grass = idx('grass_block'), dirt = idx('dirt');
    const low = new Map();
    d.blocks = d.blocks.filter(([x, y, z]) => {
      if (!inPlot(x, z)) return true;
      low.set(`${x},${z}`, Math.min(low.get(`${x},${z}`) ?? y, y));
      return y < -1;
    });
    for (const [key, yMin] of low) {
      const [x, z] = key.split(',').map(Number);
      d.blocks.push([x, -1, z, grass]);
      for (let y = -2; y >= Math.min(yMin, -2) && y >= -6; y--) d.blocks.push([x, y, z, dirt]);
    }
  }
  const dir = url.replace(/[^/]*$/, '') + 'tex/';
  const maps = {};
  const map = async (k) => (maps[k] ??= nearest(new THREE.CanvasTexture(pixelCanvas(await loadImg(dir + k + '.png'), 16, 16))));
  const byName = d.names.map(() => []);
  for (const [x, y, z, n] of d.blocks) byName[n].push([x, y, z]);
  const g = new THREE.Group();
  const cube = new THREE.BoxGeometry(1, 1, 1);
  const cross = (() => {
    const a = new THREE.PlaneGeometry(1, 1).rotateY(Math.PI / 4);
    const b = new THREE.PlaneGeometry(1, 1).rotateY(-Math.PI / 4);
    const geo = new THREE.BufferGeometry();
    for (const key of ['position', 'uv']) {
      const arr = [...a.attributes[key].array, ...b.attributes[key].array];
      geo.setAttribute(key, new THREE.Float32BufferAttribute(arr, key === 'uv' ? 2 : 3));
    }
    geo.setIndex([...a.index.array, ...[...b.index.array].map((i) => i + 4)]);
    return geo;
  })();
  const water = new THREE.PlaneGeometry(1, 1).rotateX(-Math.PI / 2).translate(0, 0.38, 0);
  // Layers lying on the block below (leaf litter)
  const flat = new THREE.PlaneGeometry(1, 1).rotateX(-Math.PI / 2).translate(0, -0.47, 0);
  const m = new THREE.Matrix4();
  const q = new THREE.Quaternion();
  for (const [n, list] of byName.entries()) {
    if (!list.length) continue;
    const look = d.looks[d.names[n]];
    let geo, mats;
    if (look.kind === 'cross') {
      geo = cross;
      mats = new THREE.MeshBasicMaterial({ map: await map(look.side), alphaTest: 0.5, side: THREE.DoubleSide });
      mats.color.setScalar(0.9);
    } else if (look.kind === 'flat') {
      geo = flat;
      mats = new THREE.MeshBasicMaterial({ map: await map(look.top), alphaTest: 0.5, side: THREE.DoubleSide });
    } else if (look.kind === 'water') {
      geo = water;
      mats = new THREE.MeshBasicMaterial({ map: await map(look.top), transparent: true, opacity: 0.78, depthWrite: false });
    } else {
      const side = await map(look.side);
      const top = look.top ? await map(look.top) : side;
      const bottom = look.bottom ? await map(look.bottom) : top;
      geo = cube;
      mats = faceMats([side, side, top, bottom, side, side]);
      if (look.cutout) mats.forEach((mt) => { mt.transparent = false; mt.alphaTest = 0.5; mt.side = THREE.DoubleSide; });
    }
    const inst = new THREE.InstancedMesh(geo, mats, list.length);
    // Logs lying along x or z turn their rings sideways
    if (look.axis === 'x') q.setFromAxisAngle(V(0, 0, 1), Math.PI / 2);
    else if (look.axis === 'z') q.setFromAxisAngle(V(1, 0, 0), Math.PI / 2);
    else q.identity();
    list.forEach(([x, y, z], k) => inst.setMatrixAt(k, m.compose(V(x, y + 0.5, z), q, V(1, 1, 1))));
    g.add(inst);
  }
  // Height of the ground top at a column (for placing things on the terrain)
  const tops = new Map();
  d.blocks.forEach(([x, y, z, n]) => {
    const look = d.looks[d.names[n]];
    if (look.kind === 'cube' && !look.cutout && (!tops.has(`${x},${z}`) || y + 1 > tops.get(`${x},${z}`))) tops.set(`${x},${z}`, y + 1);
  });
  // turn rotates the whole terrain around the center column; groundAt takes scene coordinates
  g.rotation.y = turn;
  const c = Math.cos(turn), s = Math.sin(turn);
  g.groundAt = (x, z) => tops.get(`${Math.round(c * x - s * z)},${Math.round(s * x + c * z)}`) ?? 0;
  // What a mob would stand on: the highest block of the column that is not a plant ('water', 'leaves', 'log' or the
  // block name), and how high it is; null outside the export
  const surf = new Map();
  d.blocks.forEach(([x, y, z, n]) => {
    const name = d.names[n], look = d.looks[name];
    if (look.kind === 'cross' || look.kind === 'flat') return;
    const key = `${x},${z}`;
    if (!surf.has(key) || y > surf.get(key).y) {
      const kind = look.kind === 'water' ? 'water' : look.cutout ? 'leaves' : /_log|_wood/.test(name) ? 'log' : name.split('[')[0];
      surf.set(key, { y, kind });
    }
  });
  g.surfaceAt = (x, z) => surf.get(`${Math.round(c * x - s * z)},${Math.round(s * x + c * z)}`) ?? null;
  return g;
}

export { V };
