// Shared building blocks for the deterministic three.js clips rendered by render.mjs.
// A page imports this module, builds its scene, and sets window.renderAt(t).
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

export { THREE };

// Palette shared with the Manim prelude
export const C = { bg: 0x0B0E1A, panel: 0x141B2F, cyan: 0x22D3EE, magenta: 0xF472B6, yellow: 0xFACC15, green: 0x34D399,
                   red: 0xF87171, violet: 0xA78BFA, orange: 0xFB923C, muted: 0x64748B, ink: 0xE2E8F0, arrow: 0x8291AD };
export const css = (hex) => '#' + hex.toString(16).padStart(6, '0');

// ---------- math ----------
export const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
export const prog = (t, a, b) => clamp((t - a) / (b - a));
export const easeInOut = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
export const easeOut = (x) => 1 - Math.pow(1 - x, 3);
export const easeOutBack = (x) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
export const lerp = (a, b, x) => a + (b - a) * x;
export const lerpV = (a, b, x) => new THREE.Vector3().lerpVectors(a, b, x);
export const V = (x, y, z = 0) => new THREE.Vector3(x, y, z);
export const bezier = (p0, p1, p2, x) => {
  const u = 1 - x;
  return new THREE.Vector3().addScaledVector(p0, u * u).addScaledVector(p1, 2 * u * x).addScaledVector(p2, x * x);
};
export const mixColor = (a, b, x) => new THREE.Color(a).lerp(new THREE.Color(b), clamp(x));
// Smoothly blends a value through keyframes [[t, v], ...]
export function keyed(t, keys, ease = easeInOut, dur = 0.6) {
  let v = keys[0][1];
  for (const [k, val] of keys.slice(1)) v = lerp(v, val, ease(prog(t, k, k + dur)));
  return v;
}

// ---------- timing ----------
// Segment times relative to the first narration line covered by the clip
export async function loadTiming(first, last) {
  const subs = (await (await fetch('/timestamps.json')).json()).subtitles;
  const base = subs[first].start_s;
  return { seg: (i) => subs[i].start_s - base, total: subs[last].end_s - base, subs };
}

// ---------- text ----------
export function textCanvas(text, color, px = 180, font = 'Consolas', weight = 'bold') {
  const c = document.createElement('canvas');
  const ctx = c.getContext('2d');
  ctx.font = `${weight} ${px}px ${font}`;
  const w = Math.ceil(ctx.measureText(text).width + px * 0.4);
  c.width = w; c.height = Math.ceil(px * 1.35);
  ctx.font = `${weight} ${px}px ${font}`;
  ctx.fillStyle = css(color);
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(text, w / 2, c.height / 2 + px * 0.04);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  return { tex, aspect: w / c.height };
}

export function textSprite(text, color, height, font = 'Consolas') {
  const { tex, aspect } = textCanvas(String(text), color, 180, font);
  const mat = new THREE.SpriteMaterial({ map: tex, transparent: true, toneMapped: false, depthWrite: false });
  const s = new THREE.Sprite(mat);
  s.scale.set(height * aspect, height, 1);
  s.userData.base = s.scale.clone();
  s.setSize = (k) => s.scale.copy(s.userData.base).multiplyScalar(Math.max(k, 1e-4));
  return s;
}

// Flat text that lives in the scene (does not turn toward the camera)
export function textPlane(text, color, height, font = 'Consolas') {
  const { tex, aspect } = textCanvas(String(text), color, 200, font);
  const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, toneMapped: false, depthWrite: false });
  const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), mat);
  m.scale.set(height * aspect, height, 1);
  return m;
}

// ---------- shapes ----------
export function rrShape(w, h, r) {
  const s = new THREE.Shape();
  const x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
  s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
  s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
  return s;
}

const geoCache = new Map();
function cached(key, make) { if (!geoCache.has(key)) geoCache.set(key, make()); return geoCache.get(key); }

// A tile: dark rounded box, glowing outline on the front face, text facing +z
export function makeTile(value, color, { size = 1.4, depth = 0.5, textColor = C.ink, textScale = 0.6 } = {}) {
  const boxGeo = cached(`box${size}_${depth}`, () => new RoundedBoxGeometry(size, size, depth, 4, size * 0.115));
  const ringGeo = cached(`ring${size}`, () => {
    const outer = rrShape(size * 1.07, size * 1.07, size * 0.17);
    outer.holes.push(rrShape(size * 0.97, size * 0.97, size * 0.13));
    return new THREE.ShapeGeometry(outer, 10);
  });
  const g = new THREE.Group();
  const boxMat = new THREE.MeshStandardMaterial({ color: C.panel, roughness: 0.35, metalness: 0.25, transparent: true });
  const box = new THREE.Mesh(boxGeo, boxMat);
  const ringMat = new THREE.MeshBasicMaterial({ color, toneMapped: false, transparent: true });
  const ring = new THREE.Mesh(ringGeo, ringMat);
  ring.position.z = depth / 2 + 0.01;
  const { tex, aspect } = textCanvas(String(value), textColor, 200);
  const digitMat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, toneMapped: false, depthWrite: false });
  const digit = new THREE.Mesh(cached('plane', () => new THREE.PlaneGeometry(1, 1)), digitMat);
  digit.scale.set(size * textScale * aspect, size * textScale, 1);
  digit.position.z = depth / 2 + 0.02;
  g.add(box, ring, digit);
  const tile = { g, boxMat, ringMat, digitMat, color };
  tile.set = ({ scale = 1, opacity = 1, ring: ringColor = color, digitOpacity = opacity, fill = C.panel } = {}) => {
    g.scale.setScalar(Math.max(scale, 1e-4));
    g.visible = scale > 0.001 && opacity > 0.001;
    boxMat.opacity = opacity;
    boxMat.color.set(fill);
    ringMat.opacity = opacity;
    ringMat.color.set(ringColor);
    digitMat.opacity = digitOpacity;
  };
  return tile;
}

// A round node for trees: dark sphere, glowing torus facing +z, value on the front
export function makeOrb(value, color, { r = 0.62, textColor = C.ink } = {}) {
  const sphGeo = cached(`sph${r}`, () => new THREE.SphereGeometry(r, 40, 24));
  const torGeo = cached(`tor${r}`, () => new THREE.TorusGeometry(r * 1.02, r * 0.07, 12, 64));
  const g = new THREE.Group();
  const boxMat = new THREE.MeshStandardMaterial({ color: C.panel, roughness: 0.75, metalness: 0.1, transparent: true });
  g.add(new THREE.Mesh(sphGeo, boxMat));
  const ringMat = new THREE.MeshBasicMaterial({ color, toneMapped: false, transparent: true });
  const ring = new THREE.Mesh(torGeo, ringMat);
  g.add(ring);
  const { tex, aspect } = textCanvas(String(value), textColor, 200);
  const digitMat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, toneMapped: false, depthWrite: false });
  const digit = new THREE.Mesh(cached('plane', () => new THREE.PlaneGeometry(1, 1)), digitMat);
  const h = String(value).length > 2 ? r * 0.8 : r * 1.0;
  digit.scale.set(h * aspect, h, 1);
  digit.position.z = r + 0.02;
  g.add(digit);
  const node = { g, boxMat, ringMat, digitMat, color, ring };
  node.set = ({ scale = 1, opacity = 1, ring: ringColor = color, digitOpacity = opacity, fill = C.panel } = {}) => {
    g.scale.setScalar(Math.max(scale, 1e-4));
    g.visible = scale > 0.001 && opacity > 0.001;
    boxMat.opacity = opacity;
    boxMat.color.set(fill);
    ringMat.opacity = opacity;
    ringMat.color.set(ringColor);
    digitMat.opacity = digitOpacity;
  };
  return node;
}

export function makeArrow(length, color = C.arrow, radius = 0.035) {
  const g = new THREE.Group();
  const mat = new THREE.MeshBasicMaterial({ color, toneMapped: false, transparent: true });
  const shaft = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, length - 0.22, 12), mat);
  shaft.rotation.z = -Math.PI / 2;
  shaft.position.x = (length - 0.22) / 2;
  const head = new THREE.Mesh(new THREE.ConeGeometry(radius * 3.2, 0.22, 16), mat);
  head.rotation.z = -Math.PI / 2;
  head.position.x = length - 0.11;
  g.add(shaft, head);
  g.userData.mat = mat;
  g.grow = (p) => { g.scale.set(Math.max(p, 1e-4), 1, 1); g.visible = p > 0.001; };
  return g;
}

// A glowing rod between two points that can grow from a to b
export function makeRod(a, b, color = C.arrow, radius = 0.05) {
  const mat = new THREE.MeshBasicMaterial({ color, toneMapped: false, transparent: true });
  const len = a.distanceTo(b);
  const geo = new THREE.CylinderGeometry(radius, radius, 1, 12);
  geo.translate(0, 0.5, 0);
  const m = new THREE.Mesh(geo, mat);
  m.position.copy(a);
  m.quaternion.setFromUnitVectors(V(0, 1, 0), b.clone().sub(a).normalize());
  m.grow = (p) => { m.scale.set(1, Math.max(p * len, 1e-4), 1); m.visible = p > 0.001; };
  m.grow(1);
  return m;
}

export function makeOrbLight(color, r = 0.3) {
  const mat = new THREE.MeshBasicMaterial({ color, toneMapped: false, transparent: true });
  const m = new THREE.Mesh(cached(`orb${r}`, () => new THREE.SphereGeometry(r, 32, 16)), mat);
  return m;
}

// ---------- stage ----------
// Renderer, scene, camera, lights, floor grid, bloom and a fade plane.
// offset pushes the content up the frame (fraction of the height) so the overlay can use the bottom.
export function makeStage({ fov = 42, offset = 0.24, bloom = 0.75, gridY = -3, gridX = 0, fog = [20, 48] } = {}) {
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
  scene.background = new THREE.Color(C.bg);
  scene.fog = new THREE.Fog(C.bg, fog[0], fog[1]);
  const camera = new THREE.PerspectiveCamera(fov, W / H, 0.1, 200);
  if (offset) camera.setViewOffset(W, H, 0, H * offset, W, H);
  scene.add(new THREE.AmbientLight(0xffffff, 0.55));
  const key = new THREE.DirectionalLight(0xffffff, 1.4);
  key.position.set(6, 10, 12);
  scene.add(key);
  const grid = new THREE.GridHelper(120, 120, C.cyan, C.cyan);
  grid.material.transparent = true;
  grid.material.opacity = 0.13;
  grid.position.set(gridX, gridY, 0);
  scene.add(grid);
  const fadeMat = new THREE.MeshBasicMaterial({ color: C.bg, transparent: true, depthTest: false, depthWrite: false });
  const fade = new THREE.Mesh(new THREE.PlaneGeometry(10, 10), fadeMat);
  fade.position.z = -0.5;
  fade.renderOrder = 999;
  camera.add(fade);
  scene.add(camera);
  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  composer.addPass(new UnrealBloomPass(new THREE.Vector2(W, H), bloom, 0.45, 0.2));
  composer.addPass(new OutputPass());
  const look = (pos, target) => { camera.position.copy(pos); camera.lookAt(target); };
  // Fades in at the start and out at the end of the clip
  const draw = (t, total, fin = 0.5, fout = 0.55) => {
    fadeMat.opacity = 1 - prog(t, 0, fin) + prog(t, total - fout, total - 0.05);
    fade.visible = fadeMat.opacity > 0.001;
    composer.render();
  };
  return { W, H, renderer, scene, camera, grid, composer, look, draw };
}

// Camera pose blending: poses are {pos, look}
export const pose = (pos, look) => ({ pos, look });
export const mixPose = (p, q, x) => ({ pos: lerpV(p.pos, q.pos, x), look: lerpV(p.look, q.look, x) });
export function poseTrack(t, keys, dur = 0.9) {
  // keys: [[time, pose], ...]; each key blends from the previous pose over `dur` seconds (or [time, pose, dur])
  let p = keys[0][1];
  for (const k of keys.slice(1)) p = mixPose(p, k[1], easeInOut(prog(t, k[0], k[0] + (k[2] ?? dur))));
  return { pos: p.pos.clone(), look: p.look.clone() };
}
export function drift(p, t, ax = 0.35, ay = 0.2) {
  p.pos.x += ax * Math.sin(t * 0.45);
  p.pos.y += ay * Math.sin(t * 0.31 + 1.0);
  return p;
}
