import { readFile } from 'node:fs/promises';
import { chromium } from 'playwright';

const bytes = await readFile(process.argv[2]);
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage();
  const result = await page.evaluate(async (input) => {
    const data = new Uint8Array(input);
    const context = new OfflineAudioContext(1, 8000, 8000);
    const decoded = await context.decodeAudioData(data.buffer.slice(0));
    const pcm = { sampleRate: decoded.sampleRate, channels: decoded.numberOfChannels, samples: decoded.length };
    const blob = new Blob([data], { type: 'audio/mpeg' });
    const url = URL.createObjectURL(blob);
    const element = document.createElement('audio');
    element.preload = 'metadata';
    element.src = url;
    try {
      await new Promise((resolve, reject) => {
        element.addEventListener('loadedmetadata', resolve, { once: true });
        element.addEventListener('error', () => reject(new Error(String(element.error?.message))), { once: true });
      });
      return { pcm, media: { duration: element.duration } };
    } finally {
      element.removeAttribute('src');
      element.load();
      URL.revokeObjectURL(url);
    }
  }, [...bytes]);
  console.log(JSON.stringify({ browser: browser.version(), ...result }));
} finally { await browser.close(); }
