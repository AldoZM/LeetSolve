// Game objects and their in-game animations, for the all-3D videos (first used by the Git short, 2026-10-31).
// Served as /vendor/tema/objetos.js. Each one copies what the game does (renderer and model of the game's code),
// with the game's textures from tex/ (copied by extraer.py):
//   makeBanner   standing banner (BannerRenderer): pole, bar and flag, the flag sways with a 100-tick period
//   makeLead     lead between two points (LeashRenderer): 24 segments, alternating brown, the game's sag formula
//   makeKnot     lead knot on a fence post (LeashKnotModel, 6 x 8 x 6 px)
//   makeFencePost a fence post (4 x 16 x 4 px) of any planks texture
//   makeDrop     a dropped block item (ItemEntityRenderer): a 1/4 block cube that bobs and spins
//   makeCracks   block breaking overlay (destroy_stage_0..9) drawn with the game's 2x multiply blend
//   swingArm     the player's arm swing when placing or hitting (6 ticks)
//   shakeNo      the villager's head shake when it says no (VillagerModel: zRot = 0.3 sin(0.45 ticks))
import { THREE, V } from '/vendor/lib/stage.js';
import { tex, faceMatsFor } from '/vendor/tema/mc.js';
import { entityPart } from '/vendor/tema/gente.js';

const TICK = 20;  // game ticks per second

function pixelTex(c) {
  const t = new THREE.CanvasTexture(c);
  t.magFilter = THREE.NearestFilter;
  t.minFilter = THREE.NearestFilter;
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

// The dye colors the game uses to tint banner patterns (DyeColor.getTextureDiffuseColor)
export const DYE = { white: 0xF9FFFE, orange: 0xF9801D, magenta: 0xC74EBD, light_blue: 0x3AB3DA, yellow: 0xFED83D,
  lime: 0x80C71F, pink: 0xF38BAA, gray: 0x474F52, light_gray: 0x9D9D97, cyan: 0x169C9C, purple: 0x8932B8, blue: 0x3C44AA,
  brown: 0x835432, green: 0x5E7C16, red: 0xB02E26, black: 0x1D1D21 };

// ---------- banner ----------
// Standing banner, origin on the ground at the pole, flag facing +z. sway(t) moves the flag like the game:
// xRot = (-0.0125 + 0.01 cos(2 pi f)) pi with f = ((ticks + seed) mod 100) / 100. Model scaled 2/3 like the renderer.
export function makeBanner(imgs, color = 'white', { seed = 0 } = {}) {
  const c = document.createElement('canvas');
  c.width = 64; c.height = 64;
  const ctx = c.getContext('2d');
  ctx.drawImage(imgs.banner_base, 0, 0);
  // base pattern layer tinted with the dye, drawn where the pattern has pixels
  const p = document.createElement('canvas');
  p.width = 64; p.height = 64;
  const pc = p.getContext('2d');
  pc.drawImage(imgs.banner_pattern_base, 0, 0);
  const pd = pc.getImageData(0, 0, 64, 64), od = ctx.getImageData(0, 0, 64, 64);
  const col = [(DYE[color] >> 16) & 255, (DYE[color] >> 8) & 255, DYE[color] & 255];
  for (let i = 0; i < pd.data.length; i += 4) {
    const a = pd.data[i + 3] / 255;
    if (!a) continue;
    for (let k = 0; k < 3; k++) od.data[i + k] = od.data[i + k] * (1 - a) + pd.data[i + k] * col[k] / 255 * a;
  }
  ctx.putImageData(od, 0, 0);
  const mat = new THREE.MeshBasicMaterial({ map: pixelTex(c), transparent: true, alphaTest: 0.1 });
  const g = new THREE.Group();
  const model = new THREE.Group();
  // BannerModel: pole (44, 0) 2 x 42 x 2, bar (0, 42) 20 x 2 x 2, flag (0, 0) 20 x 40 x 1 hanging from the bar
  const pole = entityPart(mat, [0, 24, 0], [[44, 0, -1, -42, -1, 2, 42, 2]]);
  const bar = entityPart(mat, [0, 24, 0], [[0, 42, -10, -44, -1, 20, 2, 2]]);
  const flag = entityPart(mat, [0, -20, 0], [[0, 0, -10, 0, -2, 20, 40, 1]]);
  model.add(pole, bar, flag);
  model.scale.setScalar(2 / 3);
  g.add(model);
  const sway = (t) => {
    const f = (((t * TICK + seed) % 100) + 100) % 100 / 100;
    flag.rotation.x = -(-0.0125 + 0.01 * Math.cos(2 * Math.PI * f)) * Math.PI;
  };
  sway(0);
  return { g, flag, sway };
}

// ---------- leads ----------
// LeashRenderer: 24 segments from a to b; y follows dy f^2 (rising) or dy - dy (1 - f)^2 (falling); every other
// segment is darker (0.7). Colors (0.5, 0.4, 0.3). Drawn as two crossed ribbons so it reads from any side.
export function makeLead({ width = 0.05 } = {}) {
  const N = 24;
  const pos = new Float32Array(N * 2 * 4 * 3), col = new Float32Array(N * 2 * 4 * 3), idx = [];
  for (let s = 0; s < N * 2; s++) {
    const b = s * 4;
    idx.push(b, b + 1, b + 2, b + 1, b + 3, b + 2);
    const k = (s % N) % 2 ? 1 : 0.7;
    for (let v = 0; v < 4; v++) col.set([0.5 * k, 0.4 * k, 0.3 * k], (b + v) * 3);
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
  geo.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(pos.length).map((_, i) => (i % 3 === 1 ? 1 : 0)), 3));
  geo.setIndex(idx);
  const mesh = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.DoubleSide }));
  mesh.frustumCulled = false;
  const at = (a, b, f) => {
    const d = b.clone().sub(a);
    const y = d.y > 0 ? d.y * f * f : d.y - d.y * (1 - f) * (1 - f);
    return V(a.x + d.x * f, a.y + y, a.z + d.z * f);
  };
  // set(a, b, k): lead from a to b, drawn up to k (0..1) so it can be tied in
  mesh.set = (a, b, k = 1) => {
    const d = b.clone().sub(a);
    const side = V(-d.z, 0, d.x).normalize().multiplyScalar(width / 2);
    const up = V(0, width / 2, 0);
    for (let r = 0; r < 2; r++) {
      const off = r ? up : side;
      for (let i = 0; i < N; i++) {
        const p0 = at(a, b, (i / N) * k), p1 = at(a, b, ((i + 1) / N) * k);
        const base = ((r * N + i) * 4) * 3;
        pos.set([p0.x - off.x, p0.y - off.y, p0.z - off.z, p0.x + off.x, p0.y + off.y, p0.z + off.z,
                 p1.x - off.x, p1.y - off.y, p1.z - off.z, p1.x + off.x, p1.y + off.y, p1.z + off.z], base);
      }
    }
    geo.attributes.position.needsUpdate = true;
    mesh.visible = k > 0.001;
  };
  mesh.visible = false;
  return mesh;
}

// LeashKnotModel: a 6 x 8 x 6 box (texture 32 x 32); origin at the bottom of the knot
export function makeKnot(imgs) {
  const mat = new THREE.MeshBasicMaterial({ map: pixelTex(imgs.lead_knot), transparent: true, alphaTest: 0.1 });
  const g = entityPart(mat, [0, 24, 0], [[0, 0, -3, -8, -3, 6, 8, 6]], [0, 0, 0], [32, 32]);
  const w = new THREE.Group();
  w.add(g);
  return w;
}

// A fence post (4 x 16 x 4 px, the game's fence_post model) of a planks texture; origin on the ground
export function makeFencePost(imgs, planks = 'acacia_planks') {
  const geo = new THREE.BoxGeometry(0.25, 1, 0.25);
  // crop the texture to the post's 4 x 16 strip, like the model's uv
  const uv = geo.attributes.uv;
  for (let i = 0; i < uv.count; i++) {
    const f = Math.floor(i / 4);
    const vScale = f === 2 || f === 3 ? 0.25 : 1;
    uv.setXY(i, 0.375 + uv.getX(i) * 0.25, uv.getY(i) * vScale);
  }
  const m = new THREE.Mesh(geo, faceMatsFor(tex(imgs, planks)));
  m.position.y = 0.5;
  const g = new THREE.Group();
  g.add(m);
  return g;
}

// ---------- dropped item ----------
// ItemEntityRenderer for a block item: a quarter-size block that bobs (sin(age / 10 + o) * 0.1 + 0.1) and spins
// (age / 20 + o radians). place(t, at) puts it at `at` (the ground under it).
export function makeDrop(imgs, side, { top = side, offset = 0 } = {}) {
  const mats = faceMatsFor(tex(imgs, side), tex(imgs, top));
  const m = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.25, 0.25), mats);
  const g = new THREE.Group();
  g.add(m);
  g.place = (t, at) => {
    const age = t * TICK;
    g.position.set(at.x, at.y + 0.125 + Math.sin(age / 10 + offset) * 0.1 + 0.1, at.z);
    m.rotation.y = age / 20 + offset;
  };
  g.visible = false;
  return g;
}

// ---------- breaking a block ----------
// The cracks texture over the block with the game's blend (dst * src * 2): darkens the block where the crack is.
// set(k): k in 0..1 is the breaking progress (stage = floor(k * 10)); 0 or 1 hides it.
export function makeCracks(imgs) {
  const maps = Array.from({ length: 10 }, (_, i) => tex(imgs, `destroy_stage_${i}`));
  // alphaTest: the empty pixels of the texture are cut out, like the game's cutout (they would brighten the block)
  const mat = new THREE.MeshBasicMaterial({ map: maps[0], transparent: true, alphaTest: 0.1, depthWrite: false, toneMapped: false, fog: false,
    blending: THREE.CustomBlending, blendSrc: THREE.DstColorFactor, blendDst: THREE.SrcColorFactor,
    polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1 });
  const m = new THREE.Mesh(new THREE.BoxGeometry(1.002, 1.002, 1.002), mat);
  m.set = (k) => {
    m.visible = k > 0 && k < 1;
    if (m.visible) mat.map = maps[Math.min(9, Math.floor(k * 10))];
  };
  m.visible = false;
  return m;
}

// ---------- people ----------
// The player's swing (attackAnim over 6 ticks): the right arm goes up and comes down. p = makePlayer(...) from gente.js;
// k in 0..1 is the progress of one swing.
export function swingArm(p, k) {
  const arm = p.arms[1];
  if (k <= 0 || k >= 1) return;
  const s = Math.sin(Math.sqrt(k) * Math.PI);
  arm.rotation.x = -(s * 1.2 + 0.4 * Math.sin(k * Math.PI));
  arm.rotation.y = -0.4 * Math.sin(Math.sqrt(k) * Math.PI * 2) * 0.5;
}

// The villager's "no": head roll 0.3 sin(0.45 ticks) and looking down (xRot 0.4) while unhappy (VillagerModel)
export function shakeNo(v, t, on) {
  v.head.rotation.z = on ? 0.3 * Math.sin(0.45 * t * TICK) : 0;
  v.head.rotation.x = on ? -0.4 : v.head.rotation.x;
}
