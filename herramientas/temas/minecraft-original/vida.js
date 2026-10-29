// Life for the 3D background: the game's mobs walking closed loops, and the time of day (sky, light, sun or moon, stars).
// Served as /vendor/tema/vida.js. Mob textures come from mobs/ (copied by extraer.py); models follow the game's
// entity models (boxes in 1/16 block units, the same texture layout as the game).
import { THREE, V } from '/vendor/lib/stage.js';

const loadImg = (src) => new Promise((res, rej) => {
  const im = new Image();
  im.onload = () => res(im);
  im.onerror = () => rej(new Error(src));
  im.src = src;
});

function pixelTex(img) {
  const c = document.createElement('canvas');
  c.width = img.width; c.height = img.height;
  c.getContext('2d').drawImage(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.magFilter = THREE.NearestFilter;
  t.minFilter = THREE.NearestFilter;
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

// ---------- models ----------
// A box with the game's entity texture layout. (u, v) is its texture offset, (w, h, d) its size in texture pixels.
// Faces: top (u+d, v), bottom (u+d+w, v), right side (u, v+d), front (u+d, v+d), left side (u+d+w, v+d), back (u+2d+w, v+d).
function cube(u, v, w, h, d, W, H, grow = 0) {
  const geo = new THREE.BoxGeometry((w + 2 * grow) / 16, (h + 2 * grow) / 16, (d + 2 * grow) / 16);
  const rects = [
    [u + d + w, v + d, d, h],      // +x: the model's left side
    [u, v + d, d, h],              // -x: right side
    [u + d, v, w, d],              // +y: top
    [u + d + w, v, w, d],          // -y: bottom
    [u + d, v + d, w, h],          // +z: front (models face +z)
    [u + 2 * d + w, v + d, w, h],  // -z: back
  ];
  const uv = geo.attributes.uv;
  for (let f = 0; f < 6; f++) {
    const [x, y, rw, rh] = rects[f];
    for (let k = 0; k < 4; k++) {
      const i = f * 4 + k;
      uv.setXY(i, (x + uv.getX(i) * rw) / W, 1 - (y + (1 - uv.getY(i)) * rh) / H);
    }
  }
  return geo;
}

// Model parts in the game's model space (y down, front toward -z), converted to three.js (y up, front toward +z):
// a part pivots at p, holds boxes [u, v, x0, y0, z0, w, h, d, grow], and rests at rotation r = [x, y, z]
function part(mat, W, H, p, boxes, r = [0, 0, 0]) {
  const g = new THREE.Group();
  g.position.set(p[0] / 16, (24 - p[1]) / 16, -p[2] / 16);
  // The game turns a part around z, then y, then x
  g.rotation.order = 'ZYX';
  g.rotation.set(r[0], -r[1], -r[2]);
  g.userData.rest = g.rotation.clone();
  for (const [u, v, x0, y0, z0, w, h, d, grow = 0] of boxes) {
    const m = new THREE.Mesh(cube(u, v, w, h, d, W, H, grow), mat);
    m.position.set((x0 + w / 2) / 16, -(y0 + h / 2) / 16, -(z0 + d / 2) / 16);
    g.add(m);
  }
  return g;
}

const HALF_PI = Math.PI / 2;
const quadLegs = (u, v, h, xs, y, zs) => [[xs, zs[0]], [-xs, zs[0]], [xs, zs[1]], [-xs, zs[1]]]
  .map(([x, z]) => ({ p: [x, y, z], boxes: [[u, v, -2, 0, -2, 4, h, 4]] }));

// Each kind: texture size, parts (name: {p, boxes, r}), legs (names swung while walking), and how it walks
const MODELS = {
  cow: { W: 64, H: 64, speed: 0.7, parts: {
    head: { p: [0, 4, -8], boxes: [[0, 0, -4, -4, -6, 8, 8, 6], [1, 33, -3, 1, -7, 6, 3, 1], [22, 0, -5, -5, -5, 1, 3, 1], [22, 0, 4, -5, -5, 1, 3, 1]] },
    body: { p: [0, 5, 2], boxes: [[18, 4, -6, -10, -7, 12, 18, 10], [52, 0, -2, 2, -8, 4, 6, 1]], r: [HALF_PI, 0, 0] },
  }, legs: quadLegs(0, 16, 12, -4, 12, [7, -6]) },
  pig: { W: 64, H: 64, speed: 0.7, parts: {
    head: { p: [0, 12, -6], boxes: [[0, 0, -4, -4, -8, 8, 8, 8], [16, 16, -2, 0, -9, 4, 3, 1]] },
    body: { p: [0, 11, 2], boxes: [[28, 8, -5, -10, -7, 10, 16, 8]], r: [HALF_PI, 0, 0] },
  }, legs: quadLegs(0, 16, 6, -3, 18, [7, -5]) },
  sheep: { W: 64, H: 32, speed: 0.65, wool: 'sheep_wool', parts: {
    head: { p: [0, 6, -8], boxes: [[0, 0, -3, -4, -6, 6, 6, 8]] },
    body: { p: [0, 5, 2], boxes: [[28, 8, -4, -10, -7, 8, 16, 6]], r: [HALF_PI, 0, 0] },
  }, legs: quadLegs(0, 16, 12, -3, 12, [7, -5]),
  woolParts: {
    head: { p: [0, 6, -8], boxes: [[0, 0, -3, -4, -4, 6, 6, 6, 0.6]] },
    body: { p: [0, 5, 2], boxes: [[28, 8, -4, -10, -7, 8, 16, 6, 1.75]], r: [HALF_PI, 0, 0] },
  }, woolLegs: [[-3, 7], [3, 7], [-3, -5], [3, -5]].map(([x, z]) => ({ p: [x, 12, z], boxes: [[0, 16, -2, 0, -2, 4, 6, 4, 0.5]] })) },
  chicken: { W: 64, H: 32, speed: 0.6, parts: {
    head: { p: [0, 15, -4], boxes: [[0, 0, -2, -6, -2, 4, 6, 3], [14, 0, -2, -4, -4, 4, 2, 2], [14, 4, -1, -2, -3, 2, 2, 2]] },
    body: { p: [0, 16, 0], boxes: [[0, 9, -3, -4, -3, 6, 8, 6]], r: [HALF_PI, 0, 0] },
    wingR: { p: [-4, 13, 0], boxes: [[24, 13, 0, 0, -3, 1, 4, 6]] },
    wingL: { p: [4, 13, 0], boxes: [[24, 13, -1, 0, -3, 1, 4, 6]] },
  }, legs: [{ p: [-2, 19, 1], boxes: [[26, 0, -1, 0, -3, 3, 5, 3]] }, { p: [1, 19, 1], boxes: [[26, 0, -1, 0, -3, 3, 5, 3]] }] },
  wolf: { W: 64, H: 32, speed: 1.0, parts: {
    head: { p: [-1, 13.5, -7], boxes: [[0, 0, -2, -3, -2, 6, 6, 4], [16, 14, -2, -5, 0, 2, 2, 1], [16, 14, 2, -5, 0, 2, 2, 1],
                                     [0, 10, -0.5, -0.001, -5, 3, 3, 4]] },
    body: { p: [0, 14, 2], boxes: [[18, 14, -3, -2, -3, 6, 9, 6]], r: [HALF_PI, 0, 0] },
    mane: { p: [-1, 14, -3], boxes: [[21, 0, -3, -3, -3, 8, 6, 7]], r: [HALF_PI, 0, 0] },
    tail: { p: [-1, 12, 8], boxes: [[9, 18, 0, 0, -1, 2, 8, 2]], r: [0.9, 0, 0] },
  }, legs: [[-2.5, 7], [0.5, 7], [-2.5, -4], [0.5, -4]].map(([x, z]) => ({ p: [x, 16, z], boxes: [[0, 18, 0, 0, -1, 2, 8, 2]] })) },
  squid: { W: 64, H: 32, speed: 0.5, swim: true, parts: {
    body: { p: [0, 8, 0], boxes: [[0, 0, -6, -8, -6, 12, 16, 12]] },
    ...Object.fromEntries(Array.from({ length: 8 }, (_, k) => {
      const a = k * Math.PI / 4;
      return [`t${k}`, { p: [Math.cos(a) * 5, 15, Math.sin(a) * 5], boxes: [[48, 0, -1, 0, -1, 2, 18, 2]], r: [0, -a + HALF_PI, 0] }];
    })),
  }, legs: [] },
  zombie: { W: 64, H: 64, speed: 0.55, arms: 'forward', parts: {
    head: { p: [0, 0, 0], boxes: [[0, 0, -4, -8, -4, 8, 8, 8]] },
    body: { p: [0, 0, 0], boxes: [[16, 16, -4, 0, -2, 8, 12, 4]] },
    armR: { p: [-5, 2, 0], boxes: [[40, 16, -3, -2, -2, 4, 12, 4]], r: [-HALF_PI, 0, 0] },
    armL: { p: [5, 2, 0], boxes: [[40, 16, -1, -2, -2, 4, 12, 4]], r: [-HALF_PI, 0, 0] },
  }, legs: [{ p: [-1.9, 12, 0], boxes: [[0, 16, -2, 0, -2, 4, 12, 4]] }, { p: [1.9, 12, 0], boxes: [[0, 16, -2, 0, -2, 4, 12, 4]] }] },
  skeleton: { W: 64, H: 32, speed: 0.6, arms: 'swing', parts: {
    head: { p: [0, 0, 0], boxes: [[0, 0, -4, -8, -4, 8, 8, 8]] },
    body: { p: [0, 0, 0], boxes: [[16, 16, -4, 0, -2, 8, 12, 4]] },
    armR: { p: [-5, 2, 0], boxes: [[40, 16, -1, -2, -1, 2, 12, 2]] },
    armL: { p: [5, 2, 0], boxes: [[40, 16, -1, -2, -1, 2, 12, 2]] },
  }, legs: [{ p: [-2, 12, 0], boxes: [[0, 16, -1, 0, -1, 2, 12, 2]] }, { p: [2, 12, 0], boxes: [[0, 16, -1, 0, -1, 2, 12, 2]] }] },
  creeper: { W: 64, H: 32, speed: 0.6, parts: {
    head: { p: [0, 6, 0], boxes: [[0, 0, -4, -8, -4, 8, 8, 8]] },
    body: { p: [0, 6, 0], boxes: [[16, 16, -4, 0, -2, 8, 12, 4]] },
  }, legs: quadLegs(0, 16, 6, -2, 18, [4, -4]) },
  spider: { W: 64, H: 32, speed: 0.9, eyes: 'spider_eyes', parts: {
    head: { p: [0, 15, -3], boxes: [[32, 4, -4, -4, -8, 8, 8, 8]] },
    neck: { p: [0, 15, 0], boxes: [[0, 0, -3, -3, -3, 6, 6, 6]] },
    body: { p: [0, 15, 9], boxes: [[0, 12, -5, -4, -6, 10, 8, 12]] },
  }, legs: [2, 1, 0, -1].flatMap((z, k) => {
    const yaw = [0.785, 0.39, -0.39, -0.785][k], roll = [0.785, 0.58, 0.58, 0.785][k];
    return [{ p: [-4, 15, z], boxes: [[18, 0, -15, -1, -1, 16, 2, 2]], r: [0, yaw, -roll] },
            { p: [4, 15, z], boxes: [[18, 0, -1, -1, -1, 16, 2, 2]], r: [0, -yaw, roll] }];
  }), spiderLegs: true },
};

function build(imgs, kind) {
  const M = MODELS[kind];
  const mat = new THREE.MeshBasicMaterial({ map: pixelTex(imgs[`mob_${kind}`]), transparent: true, alphaTest: 0.1 });
  const g = new THREE.Group();
  const parts = {};
  for (const [name, d] of Object.entries(M.parts)) { parts[name] = part(mat, M.W, M.H, d.p, d.boxes, d.r); g.add(parts[name]); }
  const legs = M.legs.map((d) => { const l = part(mat, M.W, M.H, d.p, d.boxes, d.r); g.add(l); return l; });
  const mats = [mat];
  if (M.wool) {
    const wm = new THREE.MeshBasicMaterial({ map: pixelTex(imgs[`mob_${M.wool}`]), transparent: true, alphaTest: 0.1 });
    mats.push(wm);
    for (const [name, d] of Object.entries(M.woolParts)) {
      parts[`wool_${name}`] = part(wm, 64, 32, d.p, d.boxes, d.r);
      g.add(parts[`wool_${name}`]);
    }
    M.woolLegs.forEach((d, k) => { const l = part(wm, 64, 32, d.p, d.boxes, d.r); g.add(l); legs[k].userData.wool = l; });
  }
  let eyes;
  if (M.eyes) {
    // Glowing eyes: the same head drawn again with the eyes texture, unaffected by night darkness
    eyes = new THREE.MeshBasicMaterial({ map: pixelTex(imgs[`mob_${M.eyes}`]), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending });
    const glow = part(eyes, M.W, M.H, [0, 24, 0], M.parts.head.boxes);
    parts.head.add(glow);
  }
  return { g, parts, legs, mats, M, kind };
}

// Walking pose at phase s (radians of leg swing); `amount` fades the swing in or out
function pose(mob, s, amount = 1, jump = 0, t = 0) {
  const { parts, legs, M } = mob;
  if (jump > 0) {
    const jf = Math.sin(Math.PI * jump);
    legs.forEach((l, k) => {
      const r = l.userData.rest;
      const isFront = (k === 0 || k === 1);
      const angle = isFront ? 0.35 * jf : -0.45 * jf;
      l.rotation.set(r.x + angle, r.y, r.z);
      if (l.userData.wool) l.userData.wool.rotation.copy(l.rotation);
    });
    if (parts.body) parts.body.rotation.x = parts.body.userData.rest.x - 0.15 * jf;
    if (parts.head) {
      parts.head.rotation.x = parts.head.userData.rest.x - 0.1 * jf;
      if (parts.wool_head) parts.wool_head.rotation.copy(parts.head.rotation);
    }
    if (parts.wingR) {
      const flap = 0.7 * Math.sin(t * 22);
      parts.wingR.rotation.z = -flap;
      parts.wingL.rotation.z = flap;
    }
  } else {
    legs.forEach((l, k) => {
      const r = l.userData.rest;
      if (M.spiderLegs) {
        const side = k % 2 ? 1 : -1;
        l.rotation.set(r.x + side * 0.3 * Math.sin(s + k) * amount, r.y, r.z + 0.25 * Math.abs(Math.sin(s + k * 1.3)) * amount * side);
      } else {
        const sign = (k === 0 || k === 3) ? 1 : -1;
        l.rotation.set(r.x + sign * 1.0 * Math.cos(s) * amount, r.y, r.z);
      }
      if (l.userData.wool) l.userData.wool.rotation.copy(l.rotation);
    });
    if (parts.body) parts.body.rotation.x = parts.body.userData.rest.x;
    if (M.arms === 'swing') {
      parts.armR.rotation.x = -0.6 * Math.sin(s) * amount;
      parts.armL.rotation.x = 0.6 * Math.sin(s) * amount;
    }
    if (parts.wingR) {
      parts.wingR.rotation.z = -0.1 * Math.abs(Math.sin(s * 2)) * amount;
      parts.wingL.rotation.z = 0.1 * Math.abs(Math.sin(s * 2)) * amount;
    }
    if (parts.head) {
      parts.head.rotation.x = parts.head.userData.rest.x + 0.05 * Math.sin(s * 2) * amount;
      if (parts.wool_head) parts.wool_head.rotation.copy(parts.head.rotation);
    }
  }
}

export async function loadMobs(imgs, kinds) {
  const need = new Set();
  for (const k of kinds) {
    need.add(k);
    if (MODELS[k]?.wool) need.add(MODELS[k].wool);  // textures without a model here (the iron golem) load too
    if (MODELS[k]?.eyes) need.add(MODELS[k].eyes);
  }
  await Promise.all([...need].map(async (k) => { imgs[`mob_${k}`] = await loadImg(`/vendor/tema/mobs/${k}.png`); }));
}

// ---------- time of day ----------
const TIMES = {
  day:   { top: 0x6B98F5, bottom: 0xB8D2FF, light: 1.0, clouds: 0xFFFFFF, sun: 'sun', elev: 0.9 },
  dawn:  { top: 0x5B76C9, bottom: 0xF6B386, light: 0.85, clouds: 0xFFE2D2, sun: 'sun', elev: 0.17 },
  dusk:  { top: 0x3E4B92, bottom: 0xEE8B60, light: 0.75, clouds: 0xF7C3B0, sun: 'sun', elev: 0.15 },
  night: { top: 0x04070F, bottom: 0x18213D, light: 0.42, clouds: 0x2C3350, sun: 'moon', elev: 0.2 },
};

function skyTexture(top, bottom, bands = 28) {
  const c = document.createElement('canvas');
  c.width = 4; c.height = 1440;
  const ctx = c.getContext('2d');
  const a = new THREE.Color(top), b = new THREE.Color(bottom);
  for (let k = 0; k < bands; k++) {
    ctx.fillStyle = '#' + a.clone().lerp(b, k / (bands - 1)).getHexString();
    ctx.fillRect(0, Math.floor(k * c.height / bands), 4, Math.ceil(c.height / bands) + 1);
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.magFilter = THREE.NearestFilter;
  return t;
}

// Darkens everything in a group by `k` (materials keep their own base color)
function light(group, k) {
  group.traverse((o) => {
    const ms = o.material ? (Array.isArray(o.material) ? o.material : [o.material]) : [];
    for (const m of ms) {
      if (!m.color || m.blending === THREE.AdditiveBlending) continue;
      if (m.userData.base === undefined) m.userData.base = m.color.clone();
      m.color.copy(m.userData.base).multiplyScalar(k);
    }
  });
}

// Sets the sky, fog, light, sun or moon, and stars. `look` is the direction the roam camera faces (toward -z)
export async function setTime(world, time, { terrain, clouds, imgs }) {
  const T = TIMES[time];
  world.scene.background = skyTexture(T.top, T.bottom);
  world.scene.fog.color.set(T.bottom);
  light(terrain, T.light);
  if (clouds) clouds.traverse((o) => { if (o.material) o.material.color.set(T.clouds); });
  const img = T.sun === 'sun' ? await loadImg('/vendor/tema/gui/sun.png') : imgs.mob_moon ?? await loadImg('/vendor/tema/mobs/moon.png');
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: pixelTex(img), transparent: true, fog: false, depthWrite: false,
                                                        blending: THREE.AdditiveBlending }));
  const dist = 200, az = 0.2;
  s.position.set(dist * Math.sin(az) * Math.cos(T.elev), dist * Math.sin(T.elev), -dist * Math.cos(az) * Math.cos(T.elev));
  s.scale.setScalar(time === 'day' ? 24 : 30);
  s.renderOrder = -1;
  world.scene.add(s);
  if (time === 'night') {
    // Stars: a fixed random dome (seeded), like the game's star field
    let seed = 7;
    const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
    const pos = [];
    for (let k = 0; k < 700; k++) {
      const a = rnd() * Math.PI * 2, e = 0.05 + rnd() * 1.4;
      pos.push(230 * Math.cos(e) * Math.sin(a), 230 * Math.sin(e), 230 * Math.cos(e) * Math.cos(a));
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    world.scene.add(new THREE.Points(geo, new THREE.PointsMaterial({ color: 0xffffff, size: 2.2, sizeAttenuation: false, fog: false })));
  }
  return T.light;
}

// ---------- mobs on the terrain ----------
// Ground height under (x, z), blended between columns so mobs step smoothly over the blocks
function groundY(terrain, x, z) {
  const x0 = Math.floor(x), z0 = Math.floor(z), fx = x - x0, fz = z - z0;
  const h = (a, b) => terrain.groundAt(a, b);
  const y = h(x0, z0) * (1 - fx) * (1 - fz) + h(x0 + 1, z0) * fx * (1 - fz) + h(x0, z0 + 1) * (1 - fx) * fz + h(x0 + 1, z0 + 1) * fx * fz;
  return y;
}

// Finds a closed loop for each mob where it can really walk: on land with no step higher than one block, away from
// water, trees and the lot of the walk (or all on water, for swimmers). The search is seeded, so every render is the same.
// groups: [{ kind, count, graze (how many of them stand still) }]; area = [x0, x1, z0, z1] in scene coordinates
export function planLife(terrain, groups, { area = [-16, 16, -32, -6], seed = 3, avoid = [[-7, 7, -4, 30]] } = {}) {
  let s = seed;
  const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
  const blocked = (x, z) => avoid.some(([x0, x1, z0, z1]) => x >= x0 && x <= x1 && z >= z0 && z <= z1);
  const specs = [], taken = [];
  for (const grp of groups) {
    const swim = MODELS[grp.kind].swim;
    let placed = 0;
    for (let tries = 0; tries < 3000 && placed < grp.count; tries++) {
      const cx = area[0] + rnd() * (area[1] - area[0]), cz = area[2] + rnd() * (area[3] - area[2]);
      // The roam camera sees a wedge that widens with distance
      if (Math.abs(cx) > 5 + 0.55 * Math.abs(cz)) continue;
      if (taken.some(([x, z]) => Math.hypot(x - cx, z - cz) < 4)) continue;
      const still = placed < (grp.graze ?? 0);
      // Big loops first; after many misses, smaller ones fit between trees and terraces
      const scale = tries < 1000 ? 1 : tries < 2000 ? 0.6 : 0.35;
      const w = still ? 0 : (2.5 + rnd() * 4) * scale, h = still ? 0 : (1 + rnd() * 2.5) * scale, a = rnd() * Math.PI;
      const ca = Math.cos(a), sa = Math.sin(a);
      const loop = [[-w, -h], [w, -h], [w, h], [-w, h]].map(([u, v]) => [cx + u * ca - v * sa, cz + u * sa + v * ca]);
      // Walk the loop in small steps and check every spot
      const pts = [];
      for (let k = 0; k < 4; k++) {
        const p = loop[k], q = loop[(k + 1) % 4];
        const n = Math.max(1, Math.ceil(Math.hypot(q[0] - p[0], q[1] - p[1]) / 0.4));
        for (let j = 0; j < n; j++) pts.push([p[0] + (q[0] - p[0]) * j / n, p[1] + (q[1] - p[1]) * j / n]);
      }
      if (still) pts.push([cx, cz]);
      let ok = true, prevY = null, level = null;
      for (const [x, z] of pts) {
        const sf = terrain.surfaceAt(x, z);
        if (!sf || blocked(x, z)) { ok = false; break; }
        if (swim ? sf.kind !== 'water' : ['water', 'leaves', 'log'].includes(sf.kind)) { ok = false; break; }
        // Also keep one block of room from trees and water around land mobs
        if (!swim && [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dz]) => ['water', 'leaves', 'log'].includes(terrain.surfaceAt(x + dx, z + dz)?.kind))) { ok = false; break; }
        if (prevY !== null && Math.abs(sf.y - prevY) > 1) { ok = false; break; }
        prevY = sf.y;
        level = sf.y;
      }
      if (!ok) continue;
      taken.push([cx, cz]);
      const spec = { kind: grp.kind, offset: rnd() };
      if (still) Object.assign(spec, { at: [cx, cz], face: rnd() * Math.PI * 2 });
      else spec.path = rnd() < 0.5 ? loop : loop.slice().reverse();
      // Swimmers float with their top just under the water surface (the model reaches 1.5 blocks above its origin)
      if (swim) spec.y = level - 0.75;
      specs.push(spec);
      placed++;
    }
  }
  return specs;
}

// specs: [{ kind, path: [[x, z], ...] (closed loop, scene coordinates), y (fixed height, for swimmers), offset (0..1) }]
// or { kind, at: [x, z], face (radians) } for a mob that stands still. Every loop is walked a whole number of times
// in `total` seconds, so the last frame matches the first one.
export function makeLife(imgs, terrain, specs, total, lightK = 1) {
  const g = new THREE.Group();
  const mobs = specs.map((sp) => {
    const mob = build(imgs, sp.kind);
    g.add(mob.g);
    let len = 0, segs = [];
    if (sp.path) {
      for (let k = 0; k < sp.path.length; k++) {
        const a = sp.path[k], b = sp.path[(k + 1) % sp.path.length];
        const l = Math.hypot(b[0] - a[0], b[1] - a[1]);
        segs.push({ a, b, l, s0: len });
        len += l;
      }
    }
    const laps = sp.path ? Math.max(1, Math.round(total * mob.M.speed / len)) : 0;

    // Precompute Minecraft step transitions along the closed loop
    const transitions = [];
    if (sp.path) {
      const ds = 0.05;
      const nSamples = Math.ceil(len / ds);
      let prevH = null;
      for (let i = 0; i <= nSamples; i++) {
        const dist = (i % nSamples) * ds;
        const seg = segs.find((q) => dist >= q.s0 && dist < q.s0 + q.l) ?? segs[segs.length - 1];
        const f = (dist - seg.s0) / seg.l;
        const sx = seg.a[0] + (seg.b[0] - seg.a[0]) * f;
        const sz = seg.a[1] + (seg.b[1] - seg.a[1]) * f;
        const h = terrain.groundAt(sx, sz);
        if (prevH !== null && h !== prevH && i > 0 && i < nSamples) {
          transitions.push({ s: dist, from: prevH, to: h });
        }
        prevH = h;
      }
    }

    return { mob, sp, segs, len, laps, transitions };
  });

  light(g, lightK);

  const at = (m, u) => {
    const d = (((u % 1) + 1) % 1) * m.len;
    const s = m.segs.find((q) => d >= q.s0 && d < q.s0 + q.l) ?? m.segs[m.segs.length - 1];
    const f = (d - s.s0) / s.l;
    return { x: s.a[0] + (s.b[0] - s.a[0]) * f, z: s.a[1] + (s.b[1] - s.a[1]) * f, dx: s.b[0] - s.a[0], dz: s.b[1] - s.a[1] };
  };

  const update = (t) => {
    for (const m of mobs) {
      const { mob, sp } = m;
      if (sp.at) {
        mob.g.position.set(sp.at[0], sp.y ?? terrain.groundAt(sp.at[0], sp.at[1]), sp.at[1]);
        const cycle = ((t * 0.7 + (sp.offset ?? 0) * 10) % 6);
        let headDip = 0;
        let lookYaw = sp.face ?? 0;
        if (cycle < 2.0) {
          headDip = 0.75 + 0.04 * Math.sin(t * 12);
        } else if (cycle < 2.6) {
          headDip = 0.75 * (1 - (cycle - 2.0) / 0.6);
        } else if (cycle > 4.2) {
          lookYaw += 0.2 * Math.sin((cycle - 4.2) * Math.PI);
        }
        mob.g.rotation.y = lookYaw;
        if (mob.parts.head) {
          mob.parts.head.rotation.x = mob.parts.head.userData.rest.x + headDip;
          if (mob.parts.wool_head) mob.parts.wool_head.rotation.copy(mob.parts.head.rotation);
        }
        pose(mob, 0, 0, 0, t);
        continue;
      }

      const u = m.laps * t / total + (sp.offset ?? 0);
      const p = at(m, u), q = at(m, u + 0.004);
      const yaw = Math.atan2(q.x - p.x + p.dx * 0.02, q.z - p.z + p.dz * 0.02);

      const d = (((u % 1) + 1) % 1) * m.len;
      let y = terrain.groundAt(p.x, p.z);
      let jumpProg = 0;

      if (!mob.M.swim) {
        for (const tr of m.transitions) {
          if (tr.to > tr.from) {
            let diff = d - (tr.s - 0.40);
            while (diff < -m.len / 2) diff += m.len;
            while (diff > m.len / 2) diff -= m.len;
            if (diff >= 0 && diff <= 0.75) {
              const w = diff / 0.75;
              y = tr.from + (tr.to - tr.from) * w + 0.52 * Math.sin(Math.PI * w);
              jumpProg = w;
              break;
            }
          } else if (tr.to < tr.from) {
            let diff = d - tr.s;
            while (diff < -m.len / 2) diff += m.len;
            while (diff > m.len / 2) diff -= m.len;
            if (diff >= 0 && diff <= 0.35) {
              const w = diff / 0.35;
              y = tr.from - (tr.from - tr.to) * (w * w);
              break;
            }
          }
        }
        if (jumpProg === 0) {
          y += 0.035 * Math.abs(Math.sin(d * 4.5));
        }
      } else {
        y = sp.y ?? (terrain.groundAt(p.x, p.z) - 0.75);
      }

      mob.g.position.set(p.x, y + (mob.M.swim ? 0.15 * Math.sin(t * 1.3 + u * 20) : 0), p.z);
      mob.g.rotation.y = yaw;
      pose(mob, u * m.len * 2.6, 1, jumpProg, t);
      if (mob.M.swim) mob.parts.body.rotation.x = 0.3 * Math.sin(t * 1.3);
    }
  };
  return { g, update };
}
