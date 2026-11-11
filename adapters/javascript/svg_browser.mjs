import { readFile } from 'node:fs/promises';
import { chromium } from 'playwright';

const bytes = await readFile(process.argv[2]);
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage();
  const result = await page.evaluate(async (input) => {
    const source = new TextDecoder().decode(new Uint8Array(input));
    const document = new DOMParser().parseFromString(source, 'image/svg+xml');
    const root = document.documentElement;
    const rects = [...root.querySelectorAll('rect')];
    const dom = {
      width: root.width.baseVal.value,
      height: root.height.baseVal.value,
      rects: rects.length,
      fills: rects.map((rect) => rect.getAttribute('fill')),
      typed_root: root instanceof SVGSVGElement,
      typed_rects: rects.every((rect) => rect instanceof SVGRectElement)
    };
    const blob = new Blob([new Uint8Array(input)], { type: 'image/svg+xml' });
    let imageBitmapCandidate;
    try {
      const bitmap = await createImageBitmap(blob);
      imageBitmapCandidate = { pass: true, width: bitmap.width, height: bitmap.height };
      bitmap.close();
    } catch (error) {
      imageBitmapCandidate = { pass: false, error: error.name };
    }
    const url = URL.createObjectURL(blob);
    const image = new Image();
    image.src = url;
    await image.decode();
    URL.revokeObjectURL(url);
    const canvas = window.document.createElement('canvas');
    canvas.width = image.naturalWidth;
    canvas.height = image.naturalHeight;
    const context = canvas.getContext('2d');
    context.drawImage(image, 0, 0);
    return {
      dom,
      image: { width: image.naturalWidth, height: image.naturalHeight, rgba: [...context.getImageData(0, 0, image.naturalWidth, image.naturalHeight).data] },
      imageBitmapCandidate
    };
  }, [...bytes]);
  console.log(JSON.stringify({ browser: browser.version(), ...result }));
} finally {
  await browser.close();
}
