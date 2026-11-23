// Each branch calls the package's documented local-input API. The verifier
// checks the returned fields; these functions do not invent expected values.
import { readFile } from 'node:fs/promises';
import { Readable } from 'node:stream';

export async function parse(name, path) {

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
  case 'canvas': {
    const { createCanvas, loadImage } = await import('canvas');
    const image = await loadImage(bytes);
    const canvas = createCanvas(image.width, image.height);
    const context = canvas.getContext('2d');
    context.drawImage(image, 0, 0);
    result = { width: image.width, height: image.height, rgba: rgba(context.getImageData(0, 0, image.width, image.height).data) };
    break;
  }
  case '@napi-rs/canvas': {
    const { createCanvas, loadImage } = await import('@napi-rs/canvas');
    const image = await loadImage(bytes);
    const canvas = createCanvas(image.width, image.height);
    const context = canvas.getContext('2d');
    context.drawImage(image, 0, 0);
    result = { width: image.width, height: image.height, rgba: rgba(context.getImageData(0, 0, image.width, image.height).data) };
    break;
  }
  case 'skia-canvas': {
    const { Canvas, loadImage } = await import('skia-canvas');
    const image = await loadImage(bytes);
    const canvas = new Canvas(image.width, image.height);
    const context = canvas.getContext('2d');
    context.drawImage(image, 0, 0);
    result = { width: image.width, height: image.height, rgba: rgba(context.getImageData(0, 0, image.width, image.height).data) };
    break;
  }
  case 'probe-image-size': {
    const probe = (await import('probe-image-size')).default;
    const info = probe.sync(bytes);
    result = { width: info.width, height: info.height, type: info.type };
    break;
  }
  case '@loaders.gl/images': {
    const { getBinaryImageMetadata } = await import('@loaders.gl/images');
    const arrayBuffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
    const metadata = getBinaryImageMetadata(arrayBuffer);
    result = { width: metadata.width, height: metadata.height, type: metadata.mimeType.split('/')[1] };
    break;
  }
  case '@react-pdf/image': {
    const resolveImage = (await import('@react-pdf/image')).default;
    const info = await resolveImage(bytes);
    result = { width: info.width, height: info.height, type: info.format };
    break;
  }
  case 'pureimage': {
    const image = await (await import('pureimage')).decodePNGFromStream(Readable.from([bytes]));
    result = { width: image.width, height: image.height, rgba: rgba(image.data) };
    break;
  }
  case 'pngjs-nozlib': {
    const { PNG } = await import('pngjs-nozlib');
    const image = PNG.sync.read(bytes);
    result = { width: image.width, height: image.height, rgba: rgba(image.data) };
    break;
  }
  case 'pngjs-image': {
    const PNGImage = (await import('pngjs-image')).default;
    const image = await new Promise((resolve, reject) => PNGImage.loadImage(bytes, (error, parsed) => error ? reject(error) : resolve(parsed)));
    result = { width: image.getWidth(), height: image.getHeight(), rgba: rgba(image.getImage().data) };
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
    // decode returns samples at the file's bit depth: 16-bit values, packed
    // sub-byte rows, palette indices and gray/gray+alpha/RGB channel counts.
    // Turn the first two pixels into 8-bit straight RGBA from what decode
    // returned: an indexed image (one channel with a palette; a truecolour
    // image may carry a suggested PLTE) through the library's
    // convertIndexedToRgb, which already carries tRNS alpha, and otherwise
    // depth, channels and the tRNS colour key, keeping the high byte of a
    // 16-bit sample. An 8-bit RGBA image is passed through unchanged.
    const { decode, convertIndexedToRgb } = await import('fast-png');
    const image = decode(bytes);
    const count = Math.min(2, image.width * image.height);
    const out = [];
    if (image.palette && image.channels === 1) {
      const colours = convertIndexedToRgb(image);
      const size = image.palette[0].length;
      for (let i = 0; i < count; i++) {
        const colour = Array.from(colours.slice(i * size, i * size + size));
        out.push(...(size === 4 ? colour : [...colour, 255]));
      }
    } else {
      const { width, depth, channels, data } = image;
      const rowSamples = width * channels;
      const rowLength = depth < 8 ? Math.ceil(rowSamples * depth / 8) : rowSamples;
      const sample = (pixel, channel) => {
        const row = Math.floor(pixel / width);
        const index = (pixel % width) * channels + channel;
        if (depth >= 8) return data[row * rowLength + index];
        const bit = index * depth;
        return (data[row * rowLength + (bit >> 3)] >> (8 - depth - (bit & 7))) & ((1 << depth) - 1);
      };
      const eight = (value) => depth === 16 ? value >> 8 : depth < 8 ? value * 255 / ((1 << depth) - 1) : value;
      const key = image.transparency && image.transparency.length === (channels >= 3 ? 3 : 1)
        ? Array.from(image.transparency) : null;
      for (let i = 0; i < count; i++) {
        const raw = Array.from({ length: channels }, (_, channel) => sample(i, channel));
        const colour = channels >= 3 ? raw.slice(0, 3) : [raw[0], raw[0], raw[0]];
        let alpha = channels === 2 || channels === 4 ? eight(raw[channels - 1]) : 255;
        if (key && key.every((value, channel) => value === raw[channel])) alpha = 0;
        out.push(...colour.map(eight), alpha);
      }
    }
    result = { width: image.width, height: image.height, rgba: out };
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

return result;
}
