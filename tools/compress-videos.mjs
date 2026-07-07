// Recomprime os vídeos do site (H.264 CRF 23, lado maior <=1920, +faststart).
// Uso:  cd tools && npm install && node compress-videos.mjs
// Substitui o original apenas se o resultado ficar >=15% menor.
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const ffmpeg = require('ffmpeg-static');
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR = path.join(ROOT, 'assets', 'videos');

const files = fs.readdirSync(DIR).filter(f => f.endsWith('.mp4') && !f.startsWith('tmp-'));
let before = 0, after = 0;
for (const f of files) {
  const src = path.join(DIR, f);
  const tmp = path.join(DIR, `tmp-${f}`);
  const inMB = fs.statSync(src).size / 1048576;
  before += inMB;
  execFileSync(ffmpeg, [
    '-y', '-i', src,
    '-c:v', 'libx264', '-crf', '23', '-preset', 'slow',
    '-vf', "scale=-2:'min(1920,ih)'",
    '-c:a', 'aac', '-b:a', '128k',
    '-movflags', '+faststart',
    tmp,
  ], { stdio: ['ignore', 'ignore', 'inherit'] });
  const outMB = fs.statSync(tmp).size / 1048576;
  if (outMB < inMB * 0.85) {
    fs.renameSync(tmp, src);
    after += outMB;
    console.log(`${f}: ${inMB.toFixed(1)}MB -> ${outMB.toFixed(1)}MB`);
  } else {
    fs.rmSync(tmp);
    after += inMB;
    console.log(`${f}: mantido (${inMB.toFixed(1)}MB; recompressao nao compensou)`);
  }
}
console.log(`\nTOTAL: ${before.toFixed(1)}MB -> ${after.toFixed(1)}MB`);
