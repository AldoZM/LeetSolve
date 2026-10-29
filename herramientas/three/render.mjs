// Renders a deterministic three.js page frame by frame into an mp4 (or PNG stills).
// The page must define window.renderAt(seconds), which draws the frame for that time synchronously.
// Usage:
//   node render.mjs --page <scene.html> --out clip.mp4 --frames 1054 [--fps 30] [--width 1080] [--height 1440]
//   node render.mjs --page <scene.html> --stills 0,5.2,12 --outdir stills/
//   --lib <dir> sets the folder served as /vendor/lib/ (default: this file's folder, with stage.js)
//   --tema <dir> serves a theme folder as /vendor/tema/
//   --cues <file> writes the page's window.sfxCues ([[seconds, sound, gain], ...]) as JSON, for build.py's mix
import { chromium } from 'playwright';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const args = Object.fromEntries(process.argv.slice(2).reduce((acc, a, i, all) => {
  if (a.startsWith('--')) acc.push([a.slice(2), all[i + 1]?.startsWith('--') ? 'true' : all[i + 1]]);
  return acc;
}, []));

const fps = Number(args.fps ?? 30);
const width = Number(args.width ?? 1080);
const height = Number(args.height ?? 1440);
const pagePath = path.resolve(args.page);
const root = path.dirname(pagePath);
const threeDir = path.join(path.dirname(fileURLToPath(import.meta.url)), 'node_modules', 'three');
// Shared helpers for every scene (palette, text sprites, nodes, stage setup), served under /vendor/lib/
const libDir = args.lib ? path.resolve(args.lib) : path.dirname(fileURLToPath(import.meta.url));
// Optional visual theme (textures, fonts, helpers), served under /vendor/tema/
const temaDir = args.tema ? path.resolve(args.tema) : null;

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json',
               '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.ttf': 'font/ttf' };

// Serves the scene folder, plus three.js under /vendor/three/ (module imports need http, not file://)
const server = http.createServer((req, res) => {
  const url = decodeURIComponent(req.url.split('?')[0]);
  const file = url.startsWith('/vendor/three/')
    ? path.join(threeDir, url.slice('/vendor/three/'.length))
    : url.startsWith('/vendor/lib/')
      ? path.join(libDir, url.slice('/vendor/lib/'.length))
      : url.startsWith('/vendor/tema/') && temaDir
        ? path.join(temaDir, url.slice('/vendor/tema/'.length))
        : path.join(root, url === '/' ? path.basename(pagePath) : url);
  // Also allow files one level up (session folder: timestamps.json)
  const candidates = [file, path.join(path.dirname(root), url)];
  const found = candidates.find((f) => fs.existsSync(f) && fs.statSync(f).isFile());
  if (!found) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(found)] ?? 'application/octet-stream' });
  fs.createReadStream(found).pipe(res);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;

const browser = await chromium.launch({
  args: [`--use-angle=${process.platform === 'darwin' ? 'metal' : 'd3d11'}`, '--enable-gpu', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'],
});
const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
page.on('console', (m) => console.log('[page]', m.text()));
page.on('pageerror', (e) => { console.error('[page error]', e.message); process.exitCode = 1; });
await page.goto(`http://127.0.0.1:${port}/${path.basename(pagePath)}?w=${width}&h=${height}`);
await page.waitForFunction(() => typeof window.renderAt === 'function', null, { timeout: 60000 });
console.log('GPU:', await page.evaluate(() => window.gpuInfo ?? 'unknown'));
if (args.cues) {
  const cues = await page.evaluate(() => window.sfxCues ?? []);
  fs.writeFileSync(path.resolve(args.cues), JSON.stringify(cues));
  console.log(`${cues.length} sound cues ->`, args.cues);
}

const grab = async (t) => {
  const dataUrl = await page.evaluate((s) => { window.renderAt(s); return document.querySelector('canvas').toDataURL('image/png'); }, t);
  return Buffer.from(dataUrl.split(',')[1], 'base64');
};

if (args.stills) {
  const outdir = path.resolve(args.outdir ?? 'stills');
  fs.mkdirSync(outdir, { recursive: true });
  for (const t of args.stills.split(',').map(Number)) {
    fs.writeFileSync(path.join(outdir, `t_${t.toFixed(2)}.png`), await grab(t));
  }
  console.log('stills ->', outdir);
} else {
  const frames = Number(args.frames);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', path.resolve(args.out)],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const started = Date.now();
  for (let i = 0; i < frames; i++) {
    const png = await grab(i / fps);
    if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`frame ${i}/${frames} (${((Date.now() - started) / 1000).toFixed(0)}s)`);
  }
  ff.stdin.end();
  await new Promise((r) => ff.on('close', r));
  console.log(`done ${frames} frames in ${((Date.now() - started) / 1000).toFixed(0)}s ->`, args.out);
}
await browser.close();
server.close();
