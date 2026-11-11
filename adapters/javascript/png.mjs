// Each branch calls the package's documented local-input API. The verifier
// checks the returned fields; these functions do not invent expected values.
import { readFile } from 'node:fs/promises';

const [name, path] = process.argv.slice(2);
if (!name || !path) {
  console.error('usage: node adapters/javascript/png.mjs <package> <PNG path>');
  process.exit(2);
}
const bytes = await readFile(path);
const rgba = (data) => Array.from(data.slice(0, 8));
let result;

switch (name) {
  case 'sharp': {
    const sharp = (await import('sharp')).default;
    const { data, info } = await sharp(bytes).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
    result = { width: info.width, height: info.height, rgba: rgba(data) };
    break;
  }
  case 'image-size': {
    const { imageSize } = await import('image-size');
    const info = imageSize(bytes);
    result = { width: info.width, height: info.height, type: info.type };
    break;
  }
  case 'jimp': {
    const { Jimp } = await import('jimp');
    const image = await Jimp.read(bytes);
    result = { width: image.width, height: image.height, rgba: rgba(image.bitmap.data) };
    break;
  }
  case 'pngjs': {
    const { PNG } = await import('pngjs');
    const image = PNG.sync.read(bytes);
    result = { width: image.width, height: image.height, rgba: rgba(image.data) };
    break;
  }
  case 'png-js': {
    const PNG = (await import('png-js')).default;
    const image = new PNG(bytes);
    const pixels = await new Promise((resolve) => image.decode(resolve));
    result = { width: image.width, height: image.height, rgba: rgba(pixels) };
    break;
  }
  case '@react-pdf/png-js': {
    const PNG = (await import('@react-pdf/png-js')).default;
    const image = new PNG(bytes);
    const pixels = await new Promise((resolve) => image.decode(resolve));
    result = { width: image.width, height: image.height, rgba: rgba(pixels) };
    break;
  }
  case 'fast-png': {
    const { decode } = await import('fast-png');
    const image = decode(bytes);
    result = { width: image.width, height: image.height, rgba: rgba(image.data) };
    break;
  }
  case 'upng-js': {
    const UPNG = (await import('upng-js')).default;
    const arrayBuffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
    const image = UPNG.decode(arrayBuffer);
    result = { width: image.width, height: image.height, rgba: rgba(new Uint8Array(UPNG.toRGBA8(image)[0])) };
    break;
  }
  case '@pdf-lib/upng': {
    // The published CommonJS build nests its documented default export.
    const UPNG = (await import('@pdf-lib/upng')).default.default;
    const arrayBuffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
    const image = UPNG.decode(arrayBuffer);
    result = { width: image.width, height: image.height, rgba: rgba(new Uint8Array(UPNG.toRGBA8(image)[0])) };
    break;
  }
  case 'parse-png': {
    const parsePng = (await import('parse-png')).default;
    const image = await parsePng(bytes);
    result = { width: image.width, height: image.height, rgba: rgba(image.data) };
    break;
  }
  case 'png-chunks-extract': {
    const extract = (await import('png-chunks-extract')).default;
    const chunks = extract(bytes);
    result = { chunks: chunks.map((chunk) => chunk.name) };
    break;
  }
  case '@jsquash/png': {
    const { decode, init } = await import('@jsquash/png/decode.js');
    const wasm = new URL('./codec/pkg/squoosh_png_bg.wasm', import.meta.resolve('@jsquash/png'));
    await init(await readFile(wasm));
    const arrayBuffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
    const image = await decode(arrayBuffer);
    result = { width: image.width, height: image.height, rgba: rgba(image.data) };
    break;
  }
  default:
    throw new Error(`unknown package: ${name}`);
}

console.log(JSON.stringify(result));
