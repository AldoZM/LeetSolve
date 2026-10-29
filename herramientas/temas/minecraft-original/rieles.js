// Rails for the all-3D videos: tracks laid by code with the game's rail textures, the minecart entity (empty or with a
// chest), router stations and carts riding along a track. Served as /vendor/tema/rieles.js.
// Tracks are polylines of axis-aligned segments on whole blocks (x, z), like rails in the game.
import { THREE, V } from '/vendor/lib/stage.js';
import { tex, makeChest, makeSign, textWidth } from '/vendor/tema/mc.js';
import { entityPart, skinMat } from '/vendor/tema/gente.js';
import { put, makeLectern } from '/vendor/tema/aldea.js';

// ---------- tracks ----------
const flat = new THREE.PlaneGeometry(1, 1).rotateX(-Math.PI / 2);
const DIRS = { px: [1, 0], nx: [-1, 0], pz: [0, 1], nz: [0, -1] };
const dirName = (dx, dz) => (dx > 0 ? 'px' : dx < 0 ? 'nx' : dz > 0 ? 'pz' : 'nz');
const opposite = { px: 'nx', nx: 'px', pz: 'nz', nz: 'pz' };

// Lays rails along polylines (arrays of V with whole x, z). Each block gets a straight rail, a corner where a line
// turns, or two crossed rails where lines meet. y: height of the rails over the ground
export function makeTracks(imgs, lines, { y = 0.02 } = {}) {
  const cells = new Map();
  const link = (x, z, d) => {
    const k = `${x},${z}`;
    if (!cells.has(k)) cells.set(k, { x, z, dirs: new Set() });
    cells.get(k).dirs.add(d);
  };
  for (const pts of lines) {
    for (let i = 0; i + 1 < pts.length; i++) {
      const a = pts[i], b = pts[i + 1];
      const dx = Math.sign(b.x - a.x), dz = Math.sign(b.z - a.z);
      const n = Math.abs(b.x - a.x) + Math.abs(b.z - a.z);
      for (let s = 0; s < n; s++) {
        const x = a.x + dx * s, z = a.z + dz * s;
        link(x, z, dirName(dx, dz));
        link(x + dx, z + dz, opposite[dirName(dx, dz)]);
      }
    }
  }
  // Cut out with alphaTest, not transparent: the terrain is drawn in the transparent pass, and a transparent rail that
  // doesn't write depth gets painted over by any terrain chunk sorted after it (the rails vanished in the wide shots)
  const mat = (name) => new THREE.MeshBasicMaterial({ map: tex(imgs, name), alphaTest: 0.1, side: THREE.DoubleSide });
  const straight = mat('rail'), corner = mat('rail_corner');
  const g = new THREE.Group();
  const lay = (m, x, z, ry, dy = 0) => {
    const mesh = new THREE.Mesh(flat, m);
    mesh.position.set(x, y + dy, z);
    mesh.rotation.y = ry;
    g.add(mesh);
  };
  for (const { x, z, dirs } of cells.values()) {
    const alongX = dirs.has('px') || dirs.has('nx'), alongZ = dirs.has('pz') || dirs.has('nz');
    if (dirs.size === 2 && alongX && alongZ) {
      // rail_corner.png joins the +z and +x edges; turn it until it joins the two directions of this block
      const want = [...dirs].sort().join();
      for (let k = 0; k < 4; k++) {
        const r = k * Math.PI / 2, c = Math.round(Math.cos(r)), s = Math.round(Math.sin(r));
        const turned = [[1, 0], [0, 1]].map(([vx, vz]) => dirName(vx * c + vz * s, -vx * s + vz * c));
        if (turned.sort().join() === want) { lay(corner, x, z, r); break; }
      }
      continue;
    }
    if (alongZ) lay(straight, x, z, 0);
    if (alongX) lay(straight, x, z, Math.PI / 2, alongZ ? 0.004 : 0);
  }
  return g;
}

// ---------- riding along a polyline ----------
export function pathLength(pts) {
  let L = 0;
  for (let i = 0; i + 1 < pts.length; i++) L += pts[i].distanceTo(pts[i + 1]);
  return L;
}

// Position and heading after d blocks along the polyline (clamped to its ends). yaw turns the cart's long side (+x)
// toward the direction of travel
export function along(pts, d) {
  d = Math.max(0, d);
  for (let i = 0; i + 1 < pts.length; i++) {
    const a = pts[i], b = pts[i + 1], len = a.distanceTo(b);
    if (d <= len || i + 2 === pts.length) {
      const dir = b.clone().sub(a).normalize();
      return { pos: a.clone().lerp(b, Math.min(1, d / len)), yaw: Math.atan2(-dir.z, dir.x) };
    }
    d -= len;
  }
  return { pos: pts[0].clone(), yaw: 0 };
}

// Distances along the polyline where it passes point p (a corner, a station or any point on a segment)
export function distancesTo(pts, p) {
  const out = [];
  let acc = 0;
  for (let i = 0; i + 1 < pts.length; i++) {
    const a = pts[i], b = pts[i + 1], len = a.distanceTo(b);
    const da = a.distanceTo(p), db = b.distanceTo(p);
    if (Math.abs(da + db - len) < 1e-6 && !(out.length && Math.abs(out[out.length - 1] - (acc + da)) < 1e-6)) out.push(acc + da);
    acc += len;
  }
  return out;
}

// Distance along the route at time t from keys [[time, distance], ...]: constant speed between keys, so two keys with
// the same distance are a stop (waiting in line). Before the first key and after the last one it holds still
export function distanceAt(keys, t) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i + 1 < keys.length; i++) {
    const [t0, d0] = keys[i], [t1, d1] = keys[i + 1];
    if (t <= t1) return d0 + (d1 - d0) * (t - t0) / Math.max(t1 - t0, 1e-6);
  }
  return keys[keys.length - 1][1];
}

// Time when the cart of `keys` reaches distance d (first time), for sound cues and bubbles
export function timeAt(keys, d) {
  for (let i = 0; i + 1 < keys.length; i++) {
    const [t0, d0] = keys[i], [t1, d1] = keys[i + 1];
    if (d1 > d0 && d >= d0 && d <= d1) return t0 + (t1 - t0) * (d - d0) / (d1 - d0);
  }
  return keys[keys.length - 1][0];
}

// ---------- the minecart ----------
// MinecartModel: floor and four walls, 64 x 32 texture. The game draws it at the entity's position + 0.375 with
// y flipped, sitting 1/16 over the rail; entityPart puts y = 0 at 1.5 blocks, hence the shift. Long side along +x.
export function makeMinecart(imgs, { chest = true } = {}) {
  const mat = skinMat([imgs.minecart]);
  const S = [64, 32];
  const wall = [[0, 0, -8, -9, -1, 16, 8, 2]];
  const body = new THREE.Group();
  body.add(entityPart(mat, [0, 4, 0], [[0, 10, -10, -8, -1, 20, 16, 2]], [Math.PI / 2, 0, 0], S),
           entityPart(mat, [-9, 4, 0], wall, [0, Math.PI * 1.5, 0], S),
           entityPart(mat, [9, 4, 0], wall, [0, Math.PI / 2, 0], S),
           entityPart(mat, [0, 4, -7], wall, [0, Math.PI, 0], S),
           entityPart(mat, [0, 4, 7], wall, [0, 0, 0], S));
  body.position.y = -1.5 + 0.375 + 1 / 16;
  const g = new THREE.Group();
  g.add(body);
  const cart = { g };
  if (chest) {
    // The chest minecart shows a chest block at 3/4 size, sitting on the floor
    cart.chest = makeChest(imgs, 0.66);
    cart.chest.g.position.y = 0.2;
    cart.chest.g.rotation.y = -Math.PI / 2;
    g.add(cart.chest.g);
  }
  // place(pts, d): on the track, d blocks along it
  cart.place = (pts, d) => {
    const { pos, yaw } = along(pts, d);
    g.position.copy(pos);
    g.rotation.y = yaw;
  };
  g.visible = false;
  return cart;
}

// ---------- router station ----------
// An open stall: four log posts, a plank roof with a sign, a lectern with the routing book and the keeper behind it.
// Origin on the ground at the middle of the open front, facing +z (like aldea.js)
export function makeStation(imgs, { label = 'ROUTER' } = {}) {
  const g = new THREE.Group();
  for (const x of [-2, 2]) for (const z of [-4, -1]) for (let y = 0; y <= 2; y++) put(imgs, g, 'log', x, y, z);
  for (let x = -2; x <= 2; x++) for (let z = -4; z <= -1; z++) put(imgs, g, 'oak_planks', x, 3, z);
  const lectern = makeLectern(imgs);
  lectern.g.position.set(0, 0, -1.8);
  g.add(lectern.g);
  const sign = makeSign(imgs, [label], { w: Math.max(1.8, textWidth(label) * 0.075 + 0.5), h: 0.75, post: false });
  sign.position.set(0, 3.5, -0.47);
  g.add(sign);
  return { g, lectern, keeper: V(0, 0, -3.0), visitor: V(0, 0, -0.4) };
}
