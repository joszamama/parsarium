import { readFile } from 'node:fs/promises';
import { chromium } from 'playwright';

const path = process.argv[2];
if (!path) throw new Error('usage: node ascii_pnm_browser.mjs CONTROL');
const bytes = Array.from(await readFile(path));
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage();
  const output = await page.evaluate(async (input) => {
    const blob = new Blob([Uint8Array.from(input)], { type: 'image/x-portable-pixmap' });
    const url = URL.createObjectURL(blob);
    const image = new Image();
    image.src = url;
    let htmlImage;
    try {
      await image.decode();
      htmlImage = { decoded: true, width: image.naturalWidth, height: image.naturalHeight };
    } catch (error) {
      htmlImage = { decoded: false, error: error.name };
    } finally {
      URL.revokeObjectURL(url);
    }
    let imageBitmap;
    try {
      const bitmap = await createImageBitmap(blob);
      imageBitmap = { decoded: true, width: bitmap.width, height: bitmap.height };
      bitmap.close();
    } catch (error) {
      imageBitmap = { decoded: false, error: error.name };
    }
    return { htmlImage, imageBitmap };
  }, bytes);
  console.log(JSON.stringify({ chromium: browser.version(), ...output }));
} finally {
  await browser.close();
}
