import { readFile } from 'node:fs/promises';
import { chromium } from 'playwright';

const path = process.argv[2];
if (!path) throw new Error('usage: node adapters/javascript/wav_browser.mjs <WAV path>');
const bytes = await readFile(path);
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage();
  const result = await page.evaluate(async (input) => {
    const context = new OfflineAudioContext(1, 4, 8000);
    const audio = await context.decodeAudioData(new Uint8Array(input).buffer);
    return {
      sampleRate: audio.sampleRate,
      channels: audio.numberOfChannels,
      sampleCount: audio.length,
      sampleSigns: Array.from(audio.getChannelData(0), (value) => Math.sign(value))
    };
  }, Array.from(bytes));
  console.log(JSON.stringify({ browser: browser.version(), ...result }));
} finally {
  await browser.close();
}
