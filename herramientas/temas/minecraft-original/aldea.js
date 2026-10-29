// Village pieces for the all-3D videos, built by code from the game's block textures (tex/, copied by extraer.py):
// libraries with a lectern, the root tower, destination sites, the barrier room, the TNT bank and a small home.
// Also the in-world UI: tooltip bubbles, flying items and lectern books. Served as /vendor/tema/aldea.js.
// Every builder returns { g, ... } with its origin on the ground at the middle of its open front, facing +z.
import { THREE, V, lerp, prog, easeInOut, easeOutBack, mixPose } from '/vendor/lib/stage.js';
import { tex, makeSign, drawText, textWidth } from '/vendor/tema/mc.js';

// Face shading like the game (BoxGeometry order +x, -x, +y, -y, +z, -z)
const SHADE = [0.62, 0.62, 1.0, 0.5, 0.8, 0.8];
const cube = new THREE.BoxGeometry(1, 1, 1);
const matCache = new Map();

function pixelTex(c) {
  const t = new THREE.CanvasTexture(c);
  t.magFilter = THREE.NearestFilter;
  t.minFilter = THREE.NearestFilter;
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

// Shared materials for a block: side texture, optional top and bottom
function blockMats(imgs, side, top = side, bottom = top) {
  const key = `${side}|${top}|${bottom}`;
  if (!matCache.has(key)) {
    const maps = [side, side, top, bottom, side, side].map((n) => tex(imgs, n));
    matCache.set(key, maps.map((m, k) => {
      const mat = new THREE.MeshBasicMaterial({ map: m, transparent: true, alphaTest: 0.1 });
      mat.color.setScalar(SHADE[k]);
      return mat;
    }));
  }
  return matCache.get(key);
}

// Places one block (center at x + 0.5 above y); kinds name a texture set
const KINDS = {
  log: ['log_side', 'log_top'], tnt: ['tnt_side', 'tnt_top', 'tnt_bottom'], quartz: ['quartz_block_side', 'quartz_block_top'],
  path: ['dirt_path_side', 'dirt_path_top', 'dirt'],
};
export function put(imgs, group, name, x, y, z) {
  const m = new THREE.Mesh(cube, blockMats(imgs, ...(KINDS[name] ?? [name])));
  m.position.set(x, y + 0.5, z);
  group.add(m);
  return m;
}
const fill = (imgs, g, name, [x0, x1], [y0, y1], [z0, z1], skip = () => false) => {
  for (let x = x0; x <= x1; x++) for (let y = y0; y <= y1; y++) for (let z = z0; z <= z1; z++) {
    if (!skip(x, y, z)) put(imgs, g, name, x, y, z);
  }
};

// ---------- lectern and its book ----------
// Book pages: lines are strings or { s, color, alpha, strike }; textures are cached by content
const bookCache = new Map();
function bookTexture(lines) {
  const key = JSON.stringify(lines);
  if (!bookCache.has(key)) {
    const c = document.createElement('canvas');
    c.width = 512; c.height = 320;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#e9dcb8'; ctx.fillRect(0, 0, 512, 320);
    ctx.fillStyle = '#c9b78e'; ctx.fillRect(252, 0, 8, 320);
    ctx.strokeStyle = '#6b4a2b'; ctx.lineWidth = 10; ctx.strokeRect(5, 5, 502, 310);
    lines.forEach((ln, k) => {
      const L = typeof ln === 'string' ? { s: ln } : ln;
      const y = 160 + (k - (lines.length - 1) / 2) * 62;
      ctx.globalAlpha = L.alpha ?? 1;
      // Long lines take both pages; short ones the right page
      const x = textWidth(L.s) * 4 > 230 ? 256 : 384;
      const scale = textWidth(L.s) * 4 > 480 ? 3 : 4;
      drawText(ctx, L.s, x, y, scale, L.color ?? 0x3a2a14, false);
      if (L.strike) {
        ctx.fillStyle = '#c0302a';
        const w = textWidth(L.s) * scale;
        ctx.fillRect(x - w / 2 - 6, y - 4, w + 12, 7);
      }
      ctx.globalAlpha = 1;
    });
    bookCache.set(key, pixelTex(c));
  }
  return bookCache.get(key);
}

// Lectern with an open book facing the visitor (+z). setBook(lines), open(k) with k in 0..1
export function makeLectern(imgs) {
  const g = new THREE.Group();
  const base = new THREE.Mesh(new THREE.BoxGeometry(1, 2 / 16, 1), blockMats(imgs, 'oak_planks'));
  base.position.y = 1 / 16;
  const col = new THREE.Mesh(new THREE.BoxGeometry(8 / 16, 13 / 16, 8 / 16), blockMats(imgs, 'lectern_front', 'oak_planks'));
  col.position.y = 8.5 / 16;
  const top = new THREE.Mesh(new THREE.BoxGeometry(1, 4 / 16, 1), blockMats(imgs, 'oak_planks', 'lectern_top'));
  top.position.y = 0.95;
  top.rotation.x = 0.39;
  const page = new THREE.Mesh(new THREE.PlaneGeometry(0.95, 0.6), new THREE.MeshBasicMaterial({ transparent: true, side: THREE.DoubleSide }));
  page.rotation.x = -Math.PI / 2;
  page.position.y = 0.135;
  top.add(page);
  g.add(base, col, top);
  const l = { g, page };
  l.setBook = (lines) => { page.material.map = bookTexture(lines); page.material.needsUpdate = true; };
  l.open = (k) => { const s = Math.max(easeOutBack(k), 1e-4); page.scale.set(s, 1, 1); page.visible = k > 0.01; };
  l.setBook([]);
  return l;
}

// ---------- buildings ----------
// Library with an open front: bookshelf back wall, plank walls with log corners, glass windows, a two-step roof,
// the lectern in the middle and a sign over the front. keeper and visitor are where the librarian and the guest stand.
export function makeLibrary(imgs, { label = null, wall = 'oak_planks' } = {}) {
  const g = new THREE.Group();
  fill(imgs, g, 'cobble', [-2, 2], [0, 0], [-6, -6]);
  fill(imgs, g, 'bookshelf', [-2, 2], [1, 2], [-6, -6]);
  for (const sx of [-3, 3]) {
    for (const z of [-6, -1]) fill(imgs, g, 'log', [sx, sx], [0, 2], [z, z]);
    fill(imgs, g, 'cobble', [sx, sx], [0, 0], [-5, -2]);
    fill(imgs, g, wall, [sx, sx], [1, 2], [-5, -2], (x, y, z) => y === 1 && (z === -4 || z === -3));
    fill(imgs, g, 'glass', [sx, sx], [1, 1], [-4, -3]);
  }
  fill(imgs, g, 'log', [-3, 3], [3, 3], [-1, -1]);
  fill(imgs, g, wall, [-3, 3], [3, 3], [-6, -2]);
  fill(imgs, g, wall, [-2, 2], [4, 4], [-5, -2]);
  fill(imgs, g, 'log', [-1, 1], [5, 5], [-4, -3]);
  // Plank floor laid just above the grass
  const c = document.createElement('canvas');
  c.width = 80; c.height = 64;
  const ctx = c.getContext('2d');
  ctx.imageSmoothingEnabled = false;
  for (let x = 0; x < 80; x += 16) for (let y = 0; y < 64; y += 16) ctx.drawImage(imgs.oak_planks, x, y);
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(5, 4).rotateX(-Math.PI / 2), new THREE.MeshBasicMaterial({ map: pixelTex(c) }));
  floor.material.color.setScalar(0.85);
  floor.position.set(0, 0.01, -3.5);
  g.add(floor);
  const lectern = makeLectern(imgs);
  lectern.g.position.set(0, 0, -3);
  g.add(lectern.g);
  if (label) addLabel(imgs, g, label, V(0, 3.5, -0.42));
  return { g, lectern, keeper: V(0, 0, -4.3), visitor: V(0, 0, -1.6) };
}

// A wooden sign hung on a front (no post)
function addLabel(imgs, g, text, at, w = null) {
  const width = w ?? Math.max(1.6, textWidth(text) * 0.075 + 0.5);
  const s = makeSign(imgs, [text], { w: width, h: 0.75, post: false });
  s.position.copy(at);
  g.add(s);
  return s;
}

// Root tower: stone bricks, 5 x 5, a tall doorway in front, battlements on top, a lectern inside
export function makeTower(imgs, { label = 'ROOT', h = 10 } = {}) {
  const g = new THREE.Group();
  fill(imgs, g, 'stone_bricks', [-2, 2], [0, h - 1], [-5, -1], (x, y, z) =>
    (Math.abs(x) <= 1 && z >= -4 && z <= -2) || (z === -1 && Math.abs(x) <= 1 && y <= 2));
  fill(imgs, g, 'chiseled_stone_bricks', [-2, 2], [h, h], [-5, -1], (x, y, z) => (x + z) % 2 !== 0);
  fill(imgs, g, 'smooth_stone', [-1, 1], [h - 1, h - 1], [-4, -2]);
  const lectern = makeLectern(imgs);
  lectern.g.position.set(0, 0, -2.4);
  g.add(lectern.g);
  addLabel(imgs, g, label, V(0, 3.6, -0.42));
  return { g, lectern, keeper: V(0, 0, -3.5), visitor: V(0, 0, -0.6) };
}

// A destination: quartz hall with a glass front and a big name sign (google.com and its copies)
export function makeSite(imgs, { label = 'google.com' } = {}) {
  const g = new THREE.Group();
  fill(imgs, g, 'quartz', [-3, 3], [0, 0], [-5, 0]);
  fill(imgs, g, 'quartz', [-3, 3], [1, 4], [-5, -1], (x, y, z) => Math.abs(x) <= 2 && z >= -4);
  fill(imgs, g, 'glass', [-2, 2], [1, 3], [-1, -1], (x, y) => x === 0 && y <= 2);
  fill(imgs, g, 'quartz', [-3, 3], [5, 5], [-5, -1]);
  addLabel(imgs, g, label, V(0, 5.0, -0.42), 3.2);
  return { g, door: V(0, 1, -0.4) };
}

// A closed room of barrier blocks with a dark floor, open in front
export function makeBarrierRoom(imgs) {
  const g = new THREE.Group();
  fill(imgs, g, 'black_wool', [-2, 2], [0, 0], [-4, -1]);
  fill(imgs, g, 'barrier', [-2, 2], [1, 3], [-4, -1], (x, y, z) => Math.abs(x) <= 1 && z >= -3 && z <= -1 || (z === -1 && y < 3 && Math.abs(x) <= 1));
  return { g, inside: V(0, 1, -2) };
}

// The fake bank: iron front with the bank's name, and TNT stacked inside. tnt: the blocks, for the blast
export function makeBank(imgs, { label = 'mybank.com' } = {}) {
  const g = new THREE.Group();
  fill(imgs, g, 'iron_block', [-3, 3], [0, 3], [-5, -1], (x, y, z) => Math.abs(x) <= 2 && z >= -4 && y >= 1 || (z === -1 && Math.abs(x) <= 1 && y >= 1 && y <= 2));
  const tnt = [];
  for (const [x, y, z] of [[-1, 1, -4], [0, 1, -4], [1, 1, -4], [-1, 1, -3], [1, 1, -3], [0, 2, -4], [-1, 2, -4], [1, 2, -4]]) {
    tnt.push(put(imgs, g, 'tnt', x, y, z));
  }
  addLabel(imgs, g, label, V(0, 3.4, -0.42), 2.6);
  return { g, tnt };
}

// Steve's small home with its own lectern outside (the resolver he runs himself)
export function makeHome(imgs) {
  const g = new THREE.Group();
  fill(imgs, g, 'cobble', [-2, 2], [0, 0], [-5, -1]);
  fill(imgs, g, 'oak_planks', [-2, 2], [1, 2], [-5, -1], (x, y, z) => Math.abs(x) <= 1 && z >= -4 && z <= -2 || (z === -1 && x === 0));
  fill(imgs, g, 'log', [-2, 2], [3, 3], [-5, -1]);
  fill(imgs, g, 'oak_planks', [-1, 1], [4, 4], [-4, -2]);
  const lectern = makeLectern(imgs);
  lectern.g.position.set(3.2, 0, -0.6);
  g.add(lectern.g);
  return { g, lectern, keeper: V(3.2, 0, -1.8), door: V(0, 0, 0.4) };
}

// ---------- in-world UI ----------
// Bubbles and labels keep the same size on screen and stay inside the picture: placeUI(camera) runs after the camera
// is set each frame. A registered sprite has userData.base (its scale at distance `ref`), anchor and k (pop scale).
const UI = [];
export function uiSprite(s) {
  s.userData.base = s.userData.base ?? s.scale.clone();
  s.userData.k = 1;
  s.userData.anchor = s.position.clone();
  UI.push(s);
  return s;
}
export function placeUI(camera, { ref = 7, margin = 0.06 } = {}) {
  const right = V(1, 0, 0).applyQuaternion(camera.quaternion), up = V(0, 1, 0).applyQuaternion(camera.quaternion);
  for (const s of UI) {
    if (!s.visible) continue;
    const a = s.userData.anchor;
    // Depth along the view, not the distance: clamping keeps the depth, so the size on screen stays the same
    const depth = -a.clone().applyMatrix4(camera.matrixWorldInverse).z;
    const p = a.clone().project(camera);
    // Behind the camera or far outside the picture: hidden. Pulled in, it would sit next to the lens and fill the frame
    if (depth < 0.5 || Math.abs(p.x) > 1.5 || Math.abs(p.y) > 1.5) { s.visible = false; continue; }
    s.scale.copy(s.userData.base).multiplyScalar(Math.max(s.userData.k, 1e-4) * depth / ref);
    // Half size of the box on screen, from two projected corners; a box wider than the picture shrinks to fit (9:16)
    let hx = Math.abs(a.clone().addScaledVector(right, s.scale.x / 2).project(camera).x - p.x);
    let hy = Math.abs(a.clone().addScaledVector(up, s.scale.y / 2).project(camera).y - p.y);
    const fit = Math.min(1, (1 - margin) / hx, (1 - margin) / hy);
    s.scale.multiplyScalar(fit);
    hx *= fit; hy *= fit;
    p.x = Math.min(1 - margin - hx, Math.max(-1 + margin + hx, p.x));
    p.y = Math.min(1 - margin - hy, Math.max(-1 + margin + hy, p.y));
    s.position.copy(p.unproject(camera));
  }
}

// The game's tooltip: dark purple box with a gradient border. First line in `color`, the rest gray.
// show(t, a, z, at): pops in at a, fades out before z, placed at `at`. Drawn over walls (depthTest off).
export function bubble(lines, { color = 0xFFFFFF, size = 0.024 } = {}) {
  const scale = 6, pad = 4;
  const w = Math.max(...lines.map(textWidth)) + 2 * pad, h = lines.length * 11 + 2 * pad - 2;
  const c = document.createElement('canvas');
  c.width = (w + 2) * scale; c.height = (h + 2) * scale;
  const ctx = c.getContext('2d');
  ctx.fillStyle = 'rgba(16,0,16,0.94)';
  ctx.fillRect(scale, 0, w * scale, (h + 2) * scale);
  ctx.fillRect(0, scale, (w + 2) * scale, h * scale);
  const grad = ctx.createLinearGradient(0, 0, 0, c.height);
  grad.addColorStop(0, '#5000FF'); grad.addColorStop(1, '#28007F');
  ctx.strokeStyle = grad; ctx.lineWidth = scale;
  ctx.strokeRect(scale * 1.5, scale * 1.5, (w - 1) * scale, (h - 1) * scale);
  lines.forEach((s, k) => drawText(ctx, s, c.width / 2, (pad + 5 + k * 11) * scale, scale, k === 0 ? color : 0xAAAAAA));
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: pixelTex(c), transparent: true, depthWrite: false, depthTest: false }));
  const H = size * (h + 2);
  s.scale.set(H * c.width / c.height, H, 1);
  s.renderOrder = 30;
  uiSprite(s);
  s.show = (t, a, z, at) => {
    const o = prog(t, a, a + 0.35) * (1 - prog(t, z - 0.3, z));
    s.visible = o > 0.01;
    s.userData.k = easeOutBack(Math.min(1, prog(t, a, a + 0.35)));
    s.material.opacity = o;
    if (at) s.userData.anchor.copy(at);
  };
  s.visible = false;
  return s;
}

// An item icon (written_book, compass, clock, filled_map, enchanted_book...) as a sprite; glow(k) adds the
// enchantment shimmer (purple, pulsing) for sealed answers
export function makeItem(imgs, name, size = 0.6) {
  const c = document.createElement('canvas');
  c.width = 16; c.height = 16;
  c.getContext('2d').drawImage(imgs[name], 0, 0, 16, 16);
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: pixelTex(c), transparent: true, depthWrite: false }));
  s.scale.set(size, size, 1);
  s.renderOrder = 25;
  const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: pixelTex(c), color: 0xB070FF, transparent: true, depthWrite: false,
                                                            blending: THREE.AdditiveBlending }));
  halo.renderOrder = 26;
  halo.visible = false;
  s.add(halo);
  s.glow = (k, t = 0) => {
    halo.visible = k > 0.01;
    halo.material.opacity = k * (0.55 + 0.35 * Math.sin(t * 7));
    halo.scale.setScalar(1.12 + 0.06 * Math.sin(t * 5));
  };
  s.visible = false;
  return s;
}

// Point on a hop from a to b at k (0..1), rising `height` in the middle
export function arc(a, b, k, height = 1.5) {
  return V(lerp(a.x, b.x, k), lerp(a.y, b.y, k) + height * Math.sin(Math.PI * k), lerp(a.z, b.z, k));
}

// Camera from keys [time, pose or function of t, blend seconds]: each key blends in from the previous one
export function cameraAt(CAM, t) {
  const P0 = (k) => (typeof k[1] === 'function' ? k[1](t) : k[1]);
  let p = P0(CAM[0]);
  for (const k of CAM.slice(1)) {
    const x = easeInOut(prog(t, k[0], k[0] + k[2]));
    if (x > 0) p = mixPose(p, P0(k), x);
  }
  return p;
}
