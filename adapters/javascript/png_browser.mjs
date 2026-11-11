// Verify the browser-bundled createImageBitmap API against the same PNG control.
import { readFile } from 'node:fs/promises';
import { chromium } from 'playwright';

const path = process.argv[2];
if (!path) {
  console.error('usage: node adapters/javascript/png_browser.mjs <PNG path>');
  process.exit(2);
}
const bytes = await readFile(path);
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage();
  const parsed = await page.evaluate(async (input) => {
    const blob = new Blob([new Uint8Array(input)], { type: 'image/png' });
    const bitmap = await createImageBitmap(blob);
    const canvas = document.createElement('canvas');
    canvas.width = bitmap.width;
    canvas.height = bitmap.height;
    const context = canvas.getContext('2d');
    context.drawImage(bitmap, 0, 0);
    const rgba = Array.from(context.getImageData(0, 0, bitmap.width, bitmap.height).data);
    return { width: bitmap.width, height: bitmap.height, rgba };
  }, Array.from(bytes));
  console.log(JSON.stringify({ browser: browser.version(), ...parsed }));
} finally {
  await browser.close();
}
