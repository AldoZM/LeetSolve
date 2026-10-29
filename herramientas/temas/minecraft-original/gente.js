// People for the all-3D videos: villagers (with biome and profession layers), players and illagers.
// Served as /vendor/tema/gente.js. Textures come from gente/ (copied by extraer.py); models follow the game's entity
// models (boxes in 1/16 block units, the game's 64 x 64 texture layout), scaled like the game renders them.
import { THREE, prog, easeInOut } from '/vendor/lib/stage.js';

const loadImg = (src) => new Promise((res, rej) => {
  const im = new Image();
  im.onload = () => res(im);
  im.onerror = () => rej(new Error(src));
  im.src = src;
});

// Loads gente/<name>.png into imgs[`gente_<name>`]
export async function loadPeople(imgs, names) {
  await Promise.all(names.map(async (n) => { imgs[`gente_${n}`] = await loadImg(`/vendor/tema/gente/${n}.png`); }));
}

// A box with the entity texture layout: (u, v) texture offset, (w, h, d) size in texture pixels, [tw, th] texture size
function cube(u, v, w, h, d, grow = 0, [tw, th] = [64, 64]) {
  const geo = new THREE.BoxGeometry((w + 2 * grow) / 16, (h + 2 * grow) / 16, (d + 2 * grow) / 16);
  const rects = [[u + d + w, v + d, d, h], [u, v + d, d, h], [u + d, v, w, d], [u + d + w, v, w, d], [u + d, v + d, w, h],
                 [u + 2 * d + w, v + d, w, h]];
  const uv = geo.attributes.uv;
  for (let f = 0; f < 6; f++) {
    const [x, y, rw, rh] = rects[f];
    for (let k = 0; k < 4; k++) {
      const i = f * 4 + k;
      uv.setXY(i, (x + uv.getX(i) * rw) / tw, 1 - (y + (1 - uv.getY(i)) * rh) / th);
    }
  }
  return geo;
}

// A part in game model space (y down, front toward -z) converted to three.js (y up, front toward +z):
// pivot p, boxes [u, v, x0, y0, z0, w, h, d, grow], rest rotation r = [x, y, z], texture size (64 x 32 for a minecart).
// Exported as entityPart for other entities (rieles.js)
export function entityPart(mat, p, boxes, r = [0, 0, 0], size = [64, 64]) {
  const g = new THREE.Group();
  g.position.set(p[0] / 16, (24 - p[1]) / 16, -p[2] / 16);
  g.rotation.order = 'ZYX';
  g.rotation.set(r[0], -r[1], -r[2]);
  g.userData.rest = g.rotation.clone();
  for (const [u, v, x0, y0, z0, w, h, d, grow = 0] of boxes) {
    const m = new THREE.Mesh(cube(u, v, w, h, d, grow, size), mat);
    m.position.set((x0 + w / 2) / 16, -(y0 + h / 2) / 16, -(z0 + d / 2) / 16);
    g.add(m);
  }
  return g;
}
const part = entityPart;

// One material from stacked skin layers (the game draws them as separate passes on the same model).
// mat.userData.rim: the skin has a hat brim (its top face at 31..47 x 48..64 is not empty). Also used for the minecart.
export function skinMat(layers) {
  const c = document.createElement('canvas');
  c.width = layers[0].width; c.height = layers[0].height;
  const ctx = c.getContext('2d');
  for (const im of layers) ctx.drawImage(im, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.magFilter = THREE.NearestFilter;
  t.minFilter = THREE.NearestFilter;
  t.colorSpace = THREE.SRGBColorSpace;
  const mat = new THREE.MeshBasicMaterial({ map: t, transparent: true, alphaTest: 0.1 });
  mat.userData.rim = ctx.getImageData(31, 48, 16, 16).data.some((v, i) => i % 4 === 3 && v > 0);
  return mat;
}

// Shared pose controls. walk(s, amount): leg swing at phase s; look(yaw, pitch): head turn (radians, pitch > 0 = down)
function person(g, head, legs, arms = null) {
  const walk = (s, amount = 1) => {
    legs[0].rotation.x = 0.9 * Math.cos(s) * amount;
    legs[1].rotation.x = -0.9 * Math.cos(s) * amount;
    if (arms) {
      arms[0].rotation.x = -0.7 * Math.cos(s) * amount;
      arms[1].rotation.x = 0.7 * Math.cos(s) * amount;
    }
  };
  const look = (yaw = 0, pitch = 0) => { head.rotation.y = yaw; head.rotation.x = -pitch; };
  return { g, head, legs, arms, walk, look };
}

// Villager body: head with nose and hat, robe, crossed arms (VillagerModel). Also used by the wandering trader.
function villagerBody(mat, { hat = true } = {}) {
  const g = new THREE.Group();
  const head = part(mat, [0, 0, 0], [[0, 0, -4, -10, -4, 8, 10, 8], [24, 0, -1, -3, -6, 2, 4, 2],
                                      ...(hat ? [[32, 0, -4, -10, -4, 8, 10, 8, 0.51]] : [])]);
  if (hat && mat.userData.rim) {
    const rim = part(mat, [0, 0, 0], [[30, 47, -8, -8, -6, 16, 16, 1]], [-Math.PI / 2, 0, 0]);
    rim.position.set(0, 0, 0);
    head.add(rim);
  }
  const body = part(mat, [0, 0, 0], [[16, 20, -4, 0, -3, 8, 12, 6], [0, 38, -4, 0, -3, 8, 20, 6, 0.5]]);
  const arms = part(mat, [0, 3, -1], [[44, 22, -8, -2, -2, 4, 8, 4], [44, 22, 4, -2, -2, 4, 8, 4], [40, 38, -4, 2, -2, 8, 4, 4]],
                    [-0.75, 0, 0]);
  const legs = [part(mat, [-2, 12, 0], [[0, 22, -2, 0, -2, 4, 12, 4]]), part(mat, [2, 12, 0], [[0, 22, -2, 0, -2, 4, 12, 4]])];
  g.add(head, body, arms, ...legs);
  g.scale.setScalar(0.9375);
  const p = person(g, head, legs);
  p.crossed = arms;
  return p;
}

// Villager: base skin + biome type + profession (librarian, cartographer, cleric, mason, nitwit), or a whole skin
// ('wandering_trader')
export function makeVillager(imgs, { profession = 'librarian', type = 'plains', skin = null } = {}) {
  const layers = skin ? [imgs[`gente_${skin}`]]
    : [imgs.gente_villager, imgs[`gente_type_${type}`], profession ? imgs[`gente_prof_${profession}`] : null].filter(Boolean);
  return villagerBody(skinMat(layers));
}

// Illager (IllagerModel): the villager shape without hat, arms crossed; kind = 'illusioner' or 'vindicator'
export function makeIllager(imgs, { kind = 'illusioner' } = {}) {
  return villagerBody(skinMat([imgs[`gente_${kind}`]]), { hat: false });
}

// Player with wide arms and the outer layer (PlayerModel); skin = 'steve' or 'alex'
export function makePlayer(imgs, { skin = 'steve' } = {}) {
  const mat = skinMat([imgs[`gente_${skin}`]]);
  const g = new THREE.Group();
  const head = part(mat, [0, 0, 0], [[0, 0, -4, -8, -4, 8, 8, 8], [32, 0, -4, -8, -4, 8, 8, 8, 0.5]]);
  const body = part(mat, [0, 0, 0], [[16, 16, -4, 0, -2, 8, 12, 4], [16, 32, -4, 0, -2, 8, 12, 4, 0.25]]);
  const arms = [part(mat, [-5, 2, 0], [[40, 16, -3, -2, -2, 4, 12, 4], [40, 32, -3, -2, -2, 4, 12, 4, 0.25]]),
                part(mat, [5, 2, 0], [[32, 48, -1, -2, -2, 4, 12, 4], [48, 48, -1, -2, -2, 4, 12, 4, 0.25]])];
  const legs = [part(mat, [-1.9, 12, 0], [[0, 16, -2, 0, -2, 4, 12, 4], [0, 32, -2, 0, -2, 4, 12, 4, 0.25]]),
                part(mat, [1.9, 12, 0], [[16, 48, -2, 0, -2, 4, 12, 4], [0, 48, -2, 0, -2, 4, 12, 4, 0.25]])];
  g.add(head, body, ...arms, ...legs);
  g.scale.setScalar(0.9375);
  return person(g, head, legs, arms);
}

// Walks a person through keys [time, position, yaw]: between two keys at different places it walks (facing where it
// goes); two keys with the same time teleport. amount fades the leg swing in and out.
export function moveAlong(p, keys, t) {
  let k = 0;
  while (k + 1 < keys.length && keys[k + 1][0] <= t) k++;
  const [t0, p0, y0] = keys[k];
  const next = keys[k + 1];
  if (!next || next[1].distanceTo(p0) < 1e-3 || next[0] === t0) {
    p.g.position.copy(p0);
    p.g.rotation.y = y0;
    p.walk(0, 0);
    return;
  }
  const [t1, p1, y1] = next;
  const u = prog(t, t0, t1);
  const x = u * 0.85 + easeInOut(u) * 0.15;
  p.g.position.lerpVectors(p0, p1, x);
  const dir = Math.atan2(p1.x - p0.x, p1.z - p0.z);
  const turn = (a, b, w) => a + Math.atan2(Math.sin(b - a), Math.cos(b - a)) * w;
  p.g.rotation.y = u < 0.12 ? turn(y0, dir, u / 0.12) : u > 0.88 ? turn(dir, y1, (u - 0.88) / 0.12) : dir;
  p.walk(x * p0.distanceTo(p1) * 2.4, Math.min(1, u * 8, (1 - u) * 8));
}
