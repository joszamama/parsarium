import { readFile } from 'node:fs/promises';
import { chromium } from 'playwright';

const bytes = await readFile(process.argv[2]);
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage();
  const result = await page.evaluate(async (input) => {
    const blob = new Blob([new Uint8Array(input)], { type: 'video/mp4' });
    const url = URL.createObjectURL(blob);
    const video = document.createElement('video');
    video.preload = 'metadata';
    video.src = url;
    try {
      await new Promise((resolve, reject) => {
        video.addEventListener('loadedmetadata', resolve, { once: true });
        video.addEventListener('error', () => reject(new Error(String(video.error?.message))), { once: true });
      });
      return { width: video.videoWidth, height: video.videoHeight, duration: video.duration };
    } finally {
      video.removeAttribute('src');
      video.load();
      URL.revokeObjectURL(url);
    }
  }, [...bytes]);
  console.log(JSON.stringify({ browser: browser.version(), ...result }));
} finally { await browser.close(); }
