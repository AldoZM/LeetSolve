// The world background of a video page, shared by the pages made after the template: sky, terrain, clouds, mobs and
// the camera that roams for the whole clip and blends into the walk's camera in [W0, W1].
// Served as /vendor/tema/escena.js. Same camera and terrain setup as the template (pruebas/0001-two-sum-minecraft-original),
// which keeps that code inline and has no mobs.
//   const sc = await makeScene({ map: 'claude_aldea', turn: 0, total: TOTAL, W0, W1, mobs: { extra: [...] } });
//   sc.stage.add(...);  ...  sc.frame(t, walkPose);
import { THREE, prog, easeInOut, lerp, V, pose, mixPose } from '/vendor/lib/stage.js';
import { makeWorld, makeTerrain, makeClouds, loadTheme } from '/vendor/tema/mc.js';
import { makeMobs } from '/vendor/tema/mobs.js';

export async function makeScene({ map, turn = 0, plot = [-5, 5, -2, 7], clear = [-9, 9, -2, 22], regrow = true,
                                  sky, fog = [55, 120], total, W0, W1, mobs = {}, roam = {}, textures = [] }) {
  const world = makeWorld({ fov: 40, offset: 0.34, fog, ...(sky ? { sky } : {}) });
  const { scene } = world;
  const terrain = await makeTerrain(`/vendor/tema/mundos/${map}.json`, { turn, plot, clear, regrow });
  scene.add(terrain);
  const imgs = await loadTheme(['grass_side', 'grass_top', 'dirt', 'planks', 'leaves', 'log_side', 'log_top', ...textures]);
  const clouds = makeClouds(imgs);
  scene.add(clouds);
  // Mobs stay out of the plot and of the cameras' corridor; extra ones (scene coordinates) sit on the ground
  const herd = await makeMobs(terrain, { total, avoid: [clear, [-6, 6, -3, 8]], max: 36, ...mobs });
  scene.add(herd.g);
  const stage = new THREE.Group();
  scene.add(stage);
  // Roam: one slow loop over the place for the whole video, so the last frame matches the first
  const { x = 6, y = 3.4, z = 13, dz = 2.5, lookY = 4.2 } = roam;
  const roamPose = (t) => {
    const a = 2 * Math.PI * t / total;
    return pose(V(x * Math.sin(a), y + 0.8 * Math.sin(2 * a), z + dz * Math.cos(a)), V(0.5 * x * Math.sin(a), lookY, -30));
  };
  const frame = (t, walkPose) => {
    const k = easeInOut(prog(t, W0 - 1.6, W0 - 0.1)) * (1 - easeInOut(prog(t, W1 + 0.1, W1 + 1.6)));
    const cam = k > 0 ? mixPose(roamPose(t), walkPose, k) : roamPose(t);
    world.look(cam.pos, cam.look);
    // The walk keeps its content high in the frame (the overlay uses the bottom); the roam shows more sky
    world.camera.setViewOffset(world.W, world.H, 0, world.H * lerp(0.12, 0.34, k), world.W, world.H);
    clouds.position.x = 4 * Math.sin(2 * Math.PI * t / total);
    herd.update(t);
    stage.visible = t < W1;
    world.draw(t, total, 0, 0);
  };
  // The terrain's blocks are drawn in the transparent pass too; sprites (which write no depth) go after them, on top
  const onTop = (sp) => { sp.renderOrder = 10; sp.material.depthTest = false; return sp; };
  return { world, scene, terrain, imgs, clouds, mobs: herd, stage, frame, onTop };
}
