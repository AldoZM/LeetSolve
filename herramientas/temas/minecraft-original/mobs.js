// Mobs for the world background: the game's box models with their own skins (tex/mob/, copied by extraer.py),
// placed where mundo.py found them in the world and wandering on loops that repeat every `total` seconds, so the
// clip still loops. Served as /vendor/tema/mobs.js.
//   const mobs = await makeMobs(terrain, { total: TOTAL, avoid: [[x0, x1, z0, z1]], extra: [...], max: 40 });
//   scene.add(mobs.g);  ...  mobs.update(t);
import { THREE, V } from '/vendor/lib/stage.js';

const SHADE = [0.62, 0.62, 1.0, 0.5, 0.8, 0.8];  // +x, -x, +y, -y, +z, -z like the blocks

const loadImg = (src) => new Promise((res, rej) => {
  const im = new Image();
  im.onload = () => res(im);
  im.onerror = () => rej(new Error(src));
  im.src = src;
});

// Wool colors of the 16 dyes, by the sheep's Color number
const DYES = [0xF9FFFE, 0xF9801D, 0xC74EBD, 0x3AB3DA, 0xFED83D, 0x80C71F, 0xF38BAA, 0x474F52, 0x9D9D97, 0x169C9C,
              0x8932B8, 0x3C44AA, 0x835432, 0x5E7C16, 0xB02E26, 0x1D1D21];

// Models in the game's units: pixels, y down, the mob looking toward -z, its feet at y = 24.
// part: [name, pivot, rotation x, cubes, children]; cube: [x, y, z, w, h, d, u, v, inflate]
const P = (name, pivot, rx, cubes, kids = []) => ({ name, pivot, rx, cubes, kids });
const quadLegs = (u, v, h, w, xs, zf, zb, y) => [
  P('leg0', [-xs, y, zb], 0, [[-w / 2, 0, -w / 2, w, h, w, u, v]]), P('leg1', [xs, y, zb], 0, [[-w / 2, 0, -w / 2, w, h, w, u, v]]),
  P('leg2', [-xs, y, zf], 0, [[-w / 2, 0, -w / 2, w, h, w, u, v]]), P('leg3', [xs, y, zf], 0, [[-w / 2, 0, -w / 2, w, h, w, u, v]])];
const MODELS = {
  pig: { size: [64, 64], speed: 0.8, roam: 3, parts: [
    P('head', [0, 12, -6], 0, [[-4, -4, -8, 8, 8, 8, 0, 0], [-2, 0, -9, 4, 3, 1, 16, 16]]),
    P('body', [0, 11, 2], Math.PI / 2, [[-5, -10, -7, 10, 16, 8, 28, 8]]),
    ...quadLegs(0, 16, 6, 4, 3, -5, 7, 18)] },
  cow: { size: [64, 64], speed: 0.7, roam: 3, parts: [
    P('head', [0, 4, -8], 0, [[-4, -4, -6, 8, 8, 6, 0, 0], [-5, -5, -5, 1, 3, 1, 22, 0], [4, -5, -5, 1, 3, 1, 22, 0]]),
    P('body', [0, 5, 2], Math.PI / 2, [[-6, -10, -7, 12, 18, 10, 18, 4], [-2, 2, -8, 4, 6, 1, 52, 0]]),
    ...quadLegs(0, 16, 12, 4, 4, -6, 7, 12)] },
  sheep: { size: [64, 32], speed: 0.7, roam: 3, graze: true, parts: [
    P('head', [0, 6, -8], 0, [[-3, -4, -6, 6, 6, 8, 0, 0]]),
    P('body', [0, 5, 2], Math.PI / 2, [[-4, -10, -7, 8, 16, 6, 28, 8]]),
    ...quadLegs(0, 16, 12, 4, 3, -5, 7, 12)],
    // The wool coat, a second skin over the same skeleton
    coat: [
      P('head', [0, 6, -8], 0, [[-3, -4, -4, 6, 6, 6, 0, 0, 0.6]]),
      P('body', [0, 5, 2], Math.PI / 2, [[-4, -10, -7, 8, 16, 6, 28, 8, 1.75]]),
      ...quadLegs(0, 16, 6, 4, 3, -5, 7, 12).map((p) => ({ ...p, cubes: p.cubes.map((c) => [...c.slice(0, 8), 0.5]) }))] },
  chicken: { size: [64, 32], speed: 0.9, roam: 2.5, parts: [
    P('head', [0, 15, -4], 0, [[-2, -6, -2, 4, 6, 3, 0, 0], [-2, -4, -4, 4, 2, 2, 14, 0], [-1, -2, -3, 2, 2, 2, 14, 4]]),
    P('body', [0, 16, 0], Math.PI / 2, [[-3, -4, -3, 6, 8, 6, 0, 9]]),
    P('leg0', [-2, 19, 1], 0, [[-1, 0, -3, 3, 5, 3, 26, 0]]), P('leg1', [1, 19, 1], 0, [[-1, 0, -3, 3, 5, 3, 26, 0]]),
    P('wing0', [-4, 13, 0], 0, [[0, 0, -3, 1, 4, 6, 24, 13]]), P('wing1', [4, 13, 0], 0, [[-1, 0, -3, 1, 4, 6, 24, 13]])] },
  villager: { size: [64, 64], speed: 0.9, roam: 5, parts: [
    P('head', [0, 0, 0], 0, [[-4, -10, -4, 8, 10, 8, 0, 0], [-4, -10, -4, 8, 10, 8, 32, 0, 0.5]],
      [P('nose', [0, -2, 0], 0, [[-1, -1, -6, 2, 4, 2, 24, 0]])]),
    P('body', [0, 0, 0], 0, [[-4, 0, -3, 8, 12, 6, 16, 20], [-4, 0, -3, 8, 20, 6, 0, 38, 0.5]]),
    P('arms', [0, 3, -1], -0.75, [[-8, -2, -2, 4, 8, 4, 44, 22], [4, -2, -2, 4, 8, 4, 44, 22], [-4, 2, -2, 8, 4, 4, 40, 38]]),
    P('leg0', [-2, 12, 0], 0, [[-2, 0, -2, 4, 12, 4, 0, 22]]), P('leg1', [2, 12, 0], 0, [[-2, 0, -2, 4, 12, 4, 0, 22]])] },
  iron_golem: { size: [128, 128], speed: 0.45, roam: 4, parts: [
    P('head', [0, -7, -2], 0, [[-4, -12, -5.5, 8, 10, 8, 0, 0], [-1, -5, -7.5, 2, 4, 2, 24, 0]]),
    P('body', [0, -7, 0], 0, [[-9, -2, -6, 18, 12, 11, 0, 40], [-4.5, 10, -3, 9, 5, 6, 0, 70, 0.5]]),
    P('arm0', [0, -7, 0], 0, [[-13, -2.5, -3, 4, 30, 6, 60, 21]]), P('arm1', [0, -7, 0], 0, [[9, -2.5, -3, 4, 30, 6, 60, 58]]),
    P('leg0', [-4, 11, 0], 0, [[-3.5, -3, -3, 6, 16, 5, 37, 0]]), P('leg1', [5, 11, 0], 0, [[-3.5, -3, -3, 6, 16, 5, 60, 0]])] },
  cat: { size: [64, 32], speed: 0.9, roam: 3, parts: [
    P('head', [0, 15, -9], 0, [[-2.5, -2, -3, 5, 4, 5, 0, 0], [-1.5, 0, -4, 3, 2, 2, 0, 24], [-2, -3, 0, 1, 1, 2, 0, 10],
                              [1, -3, 0, 1, 1, 2, 6, 10]]),
    P('body', [0, 12, -10], Math.PI / 2, [[-2, 3, -8, 4, 16, 6, 20, 0]]),
    P('tail', [0, 15, 8], 0.9, [[-0.5, 0, 0, 1, 8, 1, 0, 15]]),
    P('leg0', [-1.1, 18, 5], 0, [[-1, 0, 1, 2, 6, 2, 8, 13]]), P('leg1', [1.1, 18, 5], 0, [[-1, 0, 1, 2, 6, 2, 8, 13]]),
    P('leg2', [-1.2, 14.1, -5], 0, [[-1, 0, 0, 2, 10, 2, 40, 0]]), P('leg3', [1.2, 14.1, -5], 0, [[-1, 0, 0, 2, 10, 2, 40, 0]])] },
  wolf: { size: [64, 32], speed: 1.1, roam: 5, parts: [
    P('head', [-1, 13.5, -7], 0, [[-2, -3, -2, 6, 6, 4, 0, 0], [-2, -5, 0, 2, 2, 1, 16, 14], [2, -5, 0, 2, 2, 1, 16, 14],
                                  [-0.5, 0, -5, 3, 3, 4, 0, 10]]),
    P('body', [0, 14, 2], Math.PI / 2, [[-3, -2, -3, 6, 9, 6, 18, 14]]),
    P('mane', [-1, 14, -3], Math.PI / 2, [[-3, -3, -3, 8, 6, 7, 21, 0]]),
    P('tail', [-1, 12, 8], 0.6, [[0, 0, -1, 2, 8, 2, 9, 18]]),
    P('leg0', [-2.5, 16, 7], 0, [[0, 0, -1, 2, 8, 2, 0, 18]]), P('leg1', [0.5, 16, 7], 0, [[0, 0, -1, 2, 8, 2, 0, 18]]),
    P('leg2', [-2.5, 16, -4], 0, [[0, 0, -1, 2, 8, 2, 0, 18]]), P('leg3', [0.5, 16, -4], 0, [[0, 0, -1, 2, 8, 2, 0, 18]])] },
};

// A cube with the game's box-UV layout on a TW x TH skin; game units -> blocks, y up, the mob looking toward +z
function cubeMesh(mats, TW, TH, [x, y, z, w, h, d, u, v, g = 0]) {
  const k = 1 / 16;
  const geo = new THREE.BoxGeometry((w + 2 * g) * k, (h + 2 * g) * k, (d + 2 * g) * k);
  const rects = [
    [u + d + w, v + d, d, h],      // +x (the mob's left side)
    [u, v + d, d, h],              // -x
    [u + d, v, w, d],              // +y (top)
    [u + d + w, v, w, d],          // -y
    [u + d, v + d, w, h],          // +z (face)
    [u + 2 * d + w, v + d, w, h],  // -z
  ];
  const uv = geo.attributes.uv;
  for (let f = 0; f < 6; f++) {
    const [rx, ry, rw, rh] = rects[f];
    for (let q = 0; q < 4; q++) {
      const i = f * 4 + q;
      uv.setXY(i, (rx + uv.getX(i) * rw) / TW, 1 - (ry + (1 - uv.getY(i)) * rh) / TH);
    }
  }
  const m = new THREE.Mesh(geo, mats);
  m.position.set((x + w / 2) * k, -(y + h / 2) * k, -(z + d / 2) * k);
  return m;
}

function build(def, mats, coat) {
  const [TW, TH] = def.size;
  const root = new THREE.Group();
  const parts = {};
  const make = (p, parent, base) => {
    const g = new THREE.Group();
    // Pivots are absolute for top-level parts and relative for children
    g.position.set(p.pivot[0] / 16, (base - p.pivot[1]) / 16, -p.pivot[2] / 16);
    g.rotation.x = p.rx;
    g.userData.rx = p.rx;
    for (const c of p.cubes) g.add(cubeMesh(mats, TW, TH, c));
    for (const kid of p.kids) make(kid, g, 0);
    parent.add(g);
    parts[p.name] = g;
  };
  for (const p of def.parts) make(p, root, 24);
  if (coat) {
    // The coat parts follow the body parts they cover
    for (const p of def.coat) {
      const g = new THREE.Group();
      for (const c of p.cubes) {
        g.add(cubeMesh(coat, TW, TH, c));
      }
      parts[p.name].add(g);
    }
  }
  return { root, parts };
}

function skinMats(canvas) {
  const t = new THREE.CanvasTexture(canvas);
  t.magFilter = THREE.NearestFilter;
  t.minFilter = THREE.NearestFilter;
  t.colorSpace = THREE.SRGBColorSpace;
  return SHADE.map((s) => {
    const m = new THREE.MeshBasicMaterial({ map: t, transparent: true, alphaTest: 0.1 });
    m.color.setScalar(s);
    return m;
  });
}

async function skin(layers, tint = null) {
  const imgs = await Promise.all(layers.map((p) => loadImg(`/vendor/tema/tex/mob/${p}.png`).catch(() => null)));
  const base = imgs[0];
  const c = document.createElement('canvas');
  c.width = base.width; c.height = base.height;
  const ctx = c.getContext('2d');
  for (const im of imgs) if (im) ctx.drawImage(im, 0, 0);
  if (tint !== null) {
    ctx.globalCompositeOperation = 'multiply';
    ctx.fillStyle = '#' + tint.toString(16).padStart(6, '0');
    ctx.fillRect(0, 0, c.width, c.height);
    ctx.globalCompositeOperation = 'destination-in';
    ctx.drawImage(base, 0, 0);
  }
  return c;
}

function skinLayers(m) {
  const v = m.variant ?? 'temperate';
  switch (m.id) {
    case 'villager': return ['villager/villager', `villager/type/${m.type ?? 'plains'}`,
      ...(m.profession && m.profession !== 'none' ? [`villager/profession/${m.profession}`] : [])];
    case 'iron_golem': return ['iron_golem/iron_golem'];
    case 'cat': return [`cat/cat_${m.variant ?? 'tabby'}`];
    case 'wolf': return [v === 'pale' || v === 'temperate' ? 'wolf/wolf' : `wolf/wolf_${v}`];
    case 'sheep': return ['sheep/sheep'];
    default: return [`${m.id}/${m.id}_${v}`];
  }
}

// jobs: professions handed in turn to the villagers that have none (a new world's villagers are often jobless)
export async function makeMobs(terrain, { total, avoid = [], extra = [], max = 40, seed = 7, center = [0, 0], jobs = [] } = {}) {
  let s = seed;
  const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
  const inAvoid = (x, z) => avoid.some((r) => x >= r[0] && x <= r[1] && z >= r[2] && z <= r[3]);
  const lim = (terrain.radius ?? 64) - 4;
  const ok = (x, z) => Math.abs(x) < lim && Math.abs(z) < lim && terrain.hasGround(x, z) && !terrain.waterAt(x, z) &&
    !terrain.fencedAt(x, z) && !inAvoid(x, z);
  // The world's mobs nearest to the center first, then the extra ones the page asks for
  // Mobs saved indoors (under a roof) are left out: the ground there is the roof
  const outdoors = (m) => terrain.groundAt(m.x, m.z) - m.p[1] < 1.5;
  const list = [...terrain.mobs.filter((m) => MODELS[m.id] && ok(m.x, m.z) && outdoors(m))
    .sort((a, b) => Math.hypot(a.x - center[0], a.z - center[1]) - Math.hypot(b.x - center[0], b.z - center[1])),
  ...extra.map((m) => ({ yaw: 0, ...m }))].slice(0, max);
  let job = 0;
  for (const m of list) if (m.id === 'villager' && (!m.profession || m.profession === 'none') && jobs.length) m.profession = jobs[job++ % jobs.length];

  const skins = new Map();
  const g = new THREE.Group();
  const mobs = [];
  for (const m of list) {
    const def = MODELS[m.id];
    const layers = skinLayers(m);
    const key = layers.join('+');
    if (!skins.has(key)) skins.set(key, skinMats(await skin(layers)));
    let coat = null;
    if (m.id === 'sheep') {
      const ck = `wool${m.color ?? 0}`;
      if (!skins.has(ck)) skins.set(ck, skinMats(await skin(['sheep/sheep_wool'], DYES[m.color ?? 0])));
      coat = skins.get(ck);
    }
    const { root, parts } = build(def, skins.get(key), coat);
    const scale = m.baby ? 0.55 : 1;
    root.scale.setScalar(scale);
    g.add(root);

    // A loop of waypoints around home: each leg is a pause and then a walk to the next point; the last leg returns
    // home, so the walk repeats every `total` seconds
    const home = V(m.x, 0, m.z);
    const legs = Math.max(3, Math.round(total / (7 + 6 * rnd())));
    const L = total / legs;
    const pts = [home];
    const h0 = terrain.groundAt(home.x, home.z);
    for (let k = 1; k < legs; k++) {
      const prev = pts[k - 1];
      let next = prev;
      // still: stays at home (an extra mob that is part of the scene), only looking around
      for (let tries = 0; tries < (m.still ? 0 : 24); tries++) {
        const a = rnd() * 2 * Math.PI, r = (0.4 + 0.6 * rnd()) * def.roam;
        const cand = V(home.x + r * Math.sin(a), 0, home.z + r * Math.cos(a));
        const dist = cand.distanceTo(prev);
        if (dist < 1 || dist / def.speed > L * 0.7 || !ok(cand.x, cand.z)) continue;
        // Walkable: no step higher than one block along the way, and close to home's height
        let good = Math.abs(terrain.groundAt(cand.x, cand.z) - h0) <= 1;
        for (let f = 0.1; good && f < 1; f += 0.1) {
          const p = prev.clone().lerp(cand, f), q = prev.clone().lerp(cand, f - 0.1);
          good = Math.abs(terrain.groundAt(p.x, p.z) - terrain.groundAt(q.x, q.z)) <= 1 && ok(p.x, p.z);
        }
        if (good) { next = cand; break; }
      }
      pts.push(next);
    }
    pts.push(home);
    const walks = pts.slice(0, -1).map((p, k) => {
      const q = pts[k + 1];
      const dur = p.distanceTo(q) / def.speed;
      return { p, q, dur, yaw: dur > 0 ? Math.atan2(q.x - p.x, q.z - p.z) : null };
    });
    // Facing while still: the last direction walked (the loop's last walk for the first leg); the saved yaw if none
    const facing = walks.map((_, k) => {
      for (let j = 1; j <= legs; j++) {
        const w = walks[(k - j + legs) % legs];
        if (w.yaw !== null) return w.yaw;
      }
      return m.yaw;
    });
    mobs.push({ m, def, root, parts, walks, facing, L, off: rnd() * total, look: 1 + Math.floor(rnd() * 3),
                lookPh: rnd() * 6.28, graze: def.graze && rnd() < 0.7 });
  }

  const smooth = (x) => x * x * (3 - 2 * x);
  const angDiff = (a, b) => Math.atan2(Math.sin(b - a), Math.cos(b - a));
  const ground = (p, dir) => {
    // Average of the ground just behind and ahead, so a one-block step becomes a short ramp
    const a = terrain.groundAt(p.x - dir.x * 0.25, p.z - dir.z * 0.25), b = terrain.groundAt(p.x + dir.x * 0.25, p.z + dir.z * 0.25);
    return (a + b) / 2;
  };

  function update(t) {
    for (const o of mobs) {
      const u = (t + o.off) % total;
      const k = Math.min(Math.floor(u / o.L), o.walks.length - 1);
      const w = o.walks[k];
      const tl = u - k * o.L;
      const start = o.L - w.dur - 0.2;  // the walk ends a moment before the leg does
      const f = w.dur > 0 ? Math.min(1, Math.max(0, (tl - start) / w.dur)) : 0;
      const pos = w.p.clone().lerp(w.q, f);
      const dir = w.dur > 0 ? w.q.clone().sub(w.p).normalize() : V(0, 0, 1);
      const moving = f > 0 && f < 1;
      // Turns toward the next point in the 0.35 s before walking
      const turn = smooth(Math.min(1, Math.max(0, (tl - start + 0.35) / 0.35)));
      const yaw = w.yaw === null ? o.facing[k] : o.facing[k] + angDiff(o.facing[k], w.yaw) * turn;
      o.root.position.set(pos.x, ground(pos, dir), pos.z);
      o.root.rotation.y = yaw;
      // Legs swing with the distance walked; amplitude eases in and out
      const swing = Math.min(1, f * w.dur * 3, (1 - f) * w.dur * 3) * (moving ? 1 : 0);
      const ph = f * w.dur * o.def.speed * 2.7 * 2;
      const P = o.parts;
      for (const [n, sgn] of [['leg0', 1], ['leg1', -1], ['leg2', -1], ['leg3', 1]]) {
        if (P[n]) P[n].rotation.x = P[n].userData.rx + sgn * Math.cos(ph) * 0.9 * swing;
      }
      if (P.arm0) { P.arm0.rotation.x = -Math.cos(ph) * 0.5 * swing; P.arm1.rotation.x = Math.cos(ph) * 0.5 * swing; }
      if (P.wing0) { const fl = moving ? 0.5 + 0.5 * Math.sin(t * 30) : 0; P.wing0.rotation.z = fl * 0.6; P.wing1.rotation.z = -fl * 0.6; }
      if (P.tail && o.m.id === 'wolf') P.tail.rotation.z = 0.25 * Math.sin(t * 6 + o.lookPh);
      // Head: looks around while still (whole cycles over the loop), sheep lower it to eat grass
      const idle = 1 - turn;
      const h = P.head;
      h.rotation.y = idle * 0.6 * Math.sin(2 * Math.PI * o.look * u / total + o.lookPh);
      let pitch = 0;
      if (o.graze) {
        const e = tl - 1.0;  // eats for 2 s early in the pause
        pitch = (e > 0 && e < 2 && e < start - 1.0) ? Math.sin(Math.PI * e / 2) : 0;
      }
      h.rotation.x = h.userData.rx + 0.9 * pitch;
      h.position.y = (24 - o.def.parts[0].pivot[1]) / 16 - 0.28 * pitch;
    }
  }
  update(0);
  return { g, update, list: mobs };
}
