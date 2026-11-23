import { createReadStream } from 'node:fs';
import { readFile } from 'node:fs/promises';

export async function parse(name, path) {

if (!name || !path) throw new Error('usage: node ascii_pnm.mjs PACKAGE CONTROL');
const bytes = await readFile(path);
let output;

if (name === 'image-size') {
  const { imageSize } = await import('image-size');
  const { type, width, height } = imageSize(bytes);
  output = { type, width, height };
} else if (['image-size-next', 'image-size-safe', '@nous-research/image-size', '@localnerve/image-size'].includes(name)) {
  const { imageSize } = await import(name);
  const { type, width, height } = imageSize(bytes);
  output = { type, width, height };
} else if (name === 'tiny-image-size') {
  const { tinyImageSize } = await import('tiny-image-size');
  const { type, width, height } = tinyImageSize(bytes);
  output = { type, width, height };
} else if (name === '@portable/image-size') {
  const { parse } = await import('@portable/image-size');
  const { type, width, height } = parse(bytes);
  output = { type, width, height };
} else if (name === 'view-image-size') {
  const { default: module } = await import('view-image-size');
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const toAscii = (input, start, end) =>
    Buffer.from(input.buffer, input.byteOffset, input.byteLength).toString('ascii', start, end);
  const { type, width, height } = module.imageSize(view, toAscii);
  output = { type, width, height };
} else if (name === 'fastimage') {
  const { info } = await import('fastimage');
  const { type, width, height } = await info(bytes);
  output = { type, width, height };
} else if (name === 'image-meta') {
  const { imageMeta } = await import('image-meta');
  const { type, width, height } = imageMeta(bytes);
  output = { type, width, height };
} else if (name === 'netpbm-parser') {
  const { parse } = await import('netpbm-parser');
  const originalLog = console.log;
  let image;
  try {
    console.log = () => {};
    image = parse(bytes.toString('ascii'), 1);
  } finally {
    console.log = originalLog;
  }
  output = { type: image.type, width: image.dimension.width,
    height: image.dimension.height, rgba: Array.from(image.rgba) };
} else if (name === 'pgmjs') {
  const { readPgm } = await import('pgmjs');
  const image = await readPgm(path);
  output = { type: image.signature, width: Number(image.width),
    height: Number(image.height), maxval: Number(image.maxval), pixels: image.pixels };
} else if (name === '@lp-labs/ppm-image-codec') {
  const { decodePpm } = await import('@lp-labs/ppm-image-codec');
  const image = decodePpm(bytes);
  output = { width: image.width, height: image.height,
    maxval: image.maxval, rgb: Array.from(image.data) };
} else if (name === '@jdmichaud/netpbm') {
  const { ImageData } = await import('@napi-rs/canvas');
  const { decode } = await import('@jdmichaud/netpbm');
  globalThis.ImageData = ImageData;
  const image = decode(bytes);
  output = { width: image.width, height: image.height, rgba: Array.from(image.data) };
} else if (name === 'ppm') {
  const ppm = await import('ppm');
  const image = await new Promise((resolve, reject) =>
    ppm.parse(createReadStream(path), (error, parsed) => error ? reject(error) : resolve(parsed)));
  output = { width: image[0].length, height: image.length, rgb: image.flat(2) };
} else if (name === '@napi-rs/image') {
  const { Transformer } = await import('@napi-rs/image');
  const metadata = await new Transformer(bytes).metadata();
  output = { format: metadata.format, width: metadata.width, height: metadata.height };
} else if (name === '@imgdrop/pnm') {
  const { PNMDecoder } = await import('@imgdrop/pnm');
  let position = 0;
  const image = new PNMDecoder((size) => {
    const part = bytes.subarray(position, position + size);
    position += part.length;
    return part.buffer.slice(part.byteOffset, part.byteOffset + part.byteLength);
  });
  image.decode();
  output = { width: image.width, height: image.height,
    tuple: image.tupltype, rgb: Array.from(image.data) };
} else if (name === 'pgmts') {
  const { parsePgm } = await import('pgmts');
  const image = parsePgm(bytes);
  output = { type: image.signature, width: image.width, height: image.height,
    maxval: image.maxval, pixels: image.pixels };
} else if (name === 'purejsimage') {
  const { createImageLibrary } = await import('purejsimage');
  const { netpbmCodec } = await import('purejsimage/codecs/netpbm');
  const library = createImageLibrary({ codecs: [netpbmCodec] });
  const image = await library.open(path);
  const metadata = await image.metadata();
  output = { format: metadata.format, variant: metadata.variant,
    width: metadata.width, height: metadata.height, channels: metadata.channels };
} else if (name === 'image-in-browser') {
  const { decodePnm } = await import('image-in-browser');
  const image = decodePnm({ data: bytes });
  // decodePnm documents undefined as its result when decoding fails.
  if (image === undefined) throw new Error('image-in-browser decodePnm could not decode the image');
  const rgb = [];
  for (let y = 0; y < image.height; y++) {
    for (let x = 0; x < image.width; x++) {
      const pixel = image.getPixel(x, y);
      rgb.push(pixel.r, pixel.g, pixel.b);
    }
  }
  output = { width: image.width, height: image.height, rgb };
} else if (name === '@designliquido/delegua-imagens') {
  const { abrirPPM } = await import('@designliquido/delegua-imagens');
  const image = await abrirPPM({}, path);
  output = { width: image.largura, height: image.altura,
    rgb: image.pixelsRGB.flatMap((row) => row.flatMap((pixel) => [pixel.r, pixel.g, pixel.b])) };
} else if (name === '@catlabtech/webcvt-image-legacy') {
  const { parsePpm } = await import('@catlabtech/webcvt-image-legacy');
  const image = parsePpm(bytes);
  output = { variant: image.variant, width: image.width,
    height: image.height, rgb: Array.from(image.pixelData) };
} else {
  throw new Error(`unknown ASCII PNM parser: ${name}`);
}

return output;
}
