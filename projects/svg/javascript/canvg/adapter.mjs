import { readFile } from 'node:fs/promises';

export async function parse(name, control) {

if (!name || !control) throw new Error('usage: node adapters/javascript/svg.mjs PACKAGE CONTROL_PATH');
const bytes = await readFile(control);
const source = bytes.toString('utf8');
const dimensions = (width, height, format = 'svg') => ({ width, height, format });
const structure = (width, height, fills) => ({ width: Number(width), height: Number(height), rects: fills.length, fills });
const pixels = (width, height, rgba) => ({ width: Number(width), height: Number(height), rgba: [...rgba] });
let result;

if (name === 'sharp') {
  const { default: sharp } = await import(name);
  const meta = await sharp(bytes).metadata();
  result = dimensions(meta.width, meta.height, meta.format);
} else if (name === 'image-size') {
  const { imageSize } = await import(name);
  const meta = imageSize(bytes);
  result = dimensions(meta.width, meta.height, meta.type);
} else if (name === 'probe-image-size') {
  const { sync } = await import(name);
  const meta = sync(bytes);
  result = dimensions(meta.width, meta.height, meta.type);
} else if (['skia-canvas', '@napi-rs/canvas', 'canvas'].includes(name)) {
  const api = await import(name);
  const image = await api.loadImage(bytes);
  const canvas = name === 'skia-canvas' ? new api.Canvas(image.width, image.height) : api.createCanvas(image.width, image.height);
  const ctx = canvas.getContext('2d');
  ctx.drawImage(image, 0, 0);
  result = pixels(image.width, image.height, ctx.getImageData(0, 0, image.width, image.height).data);
} else if (['canvg', '@yworks/canvg'].includes(name)) {
  const api = await import(name);
  const { createCanvas } = await import('canvas');
  const { DOMParser } = await import('@xmldom/xmldom');
  const canvas = createCanvas(2, 1);
  const ctx = canvas.getContext('2d');
  const renderer = api.Canvg.fromString(ctx, source, api.presets.node({ DOMParser, canvas: createCanvas, fetch }));
  await renderer.render();
  result = pixels(canvas.width, canvas.height, ctx.getImageData(0, 0, canvas.width, canvas.height).data);
} else if (name === 'svg-parser') {
  const { parse } = await import(name);
  const svg = parse(source).children.find((item) => item.tagName === 'svg');
  result = structure(svg.properties.width, svg.properties.height, svg.children.filter((item) => item.tagName === 'rect').map((item) => item.properties.fill));
} else if (name === 'svgson') {
  const { parse } = await import(name);
  const svg = await parse(source);
  result = structure(svg.attributes.width, svg.attributes.height, svg.children.filter((item) => item.name === 'rect').map((item) => item.attributes.fill));
} else if (name === 'postsvg') {
  const { parse } = await import(name);
  const tree = parse(source);
  result = structure(tree.root.attrs.width, tree.root.attrs.height, tree.select('rect').map((item) => item.attrs.fill));
} else if (name === 'streaming-svg-parser') {
  const { createStreamingSVGParser } = await import(name);
  const elements = [];
  const parseText = createStreamingSVGParser((element) => elements.push({ tag: element.tagName, attrs: Object.fromEntries(element.attributes) }));
  parseText(source);
  const svg = elements.find((item) => item.tag === 'svg');
  result = structure(svg.attrs.width, svg.attrs.height, elements.filter((item) => item.tag === 'rect').map((item) => item.attrs.fill));
} else if (name === 'svg-eslint-parser') {
  const { parse } = await import(name);
  const svg = parse(source).children.find((item) => item.name === 'svg');
  const attrs = (item) => Object.fromEntries(item.attributes.map((attribute) => [attribute.key.value, attribute.value?.value]));
  result = structure(attrs(svg).width, attrs(svg).height, svg.children.filter((item) => item.name === 'rect').map((item) => attrs(item).fill));
} else if (name === 'vsvg-parser') {
  const { parse } = await import(name);
  const svg = parse(source).find((item) => item.tagName === 'svg');
  result = structure(svg.attributes.width, svg.attributes.height, svg.children.filter((item) => item.tagName === 'rect').map((item) => item.attributes.fill));
} else if (name === 'svgps') {
  const { parse } = await import(name);
  const svg = parse(source);
  result = { width: svg.width, height: svg.height, paths: svg.paths.length, fills: svg.attrs.map((item) => item.fill) };
} else if (name === 'svgo') {
  const { optimize } = await import(name);
  const { data } = optimize(source, { plugins: ['convertShapeToPath'] });
  result = { paths: (data.match(/<path\b/g) ?? []).length, fills: [...data.matchAll(/\bfill="([^"]+)"/g)].map((match) => match[1]) };
} else if (name === 'get-svg-colors') {
  const { default: getColors } = await import(name);
  result = { fills: getColors(source, { flat: true }).map((color) => color.hex()) };
} else if (['@resvg/resvg-js', '@resvg/resvg-wasm', '@cf-wasm/resvg', '@stacksjs/ts-svg'].includes(name)) {
  const api = await import(name);
  if (name === '@resvg/resvg-wasm') {
    const wasm = await readFile(new URL(import.meta.resolve('@resvg/resvg-wasm/index_bg.wasm')));
    await api.initWasm(wasm);
  }
  const renderer = name === '@cf-wasm/resvg' ? await api.Resvg.async(source) : new api.Resvg(source);
  const image = renderer.render();
  const width = typeof image.width === 'function' ? image.width() : image.width;
  const height = typeof image.height === 'function' ? image.height() : image.height;
  const rgba = typeof image.pixels === 'function' ? image.pixels() : image.pixels;
  result = pixels(width, height, rgba);
  image.free?.();
  renderer.free?.();
} else if (name === 'svg2img') {
  const { default: convert } = await import(name);
  const pngBytes = await new Promise((resolve, reject) => convert(source, (error, output) => error ? reject(error) : resolve(output)));
  const { PNG } = await import('pngjs');
  const image = PNG.sync.read(pngBytes);
  result = pixels(image.width, image.height, image.data);
} else {
  throw new Error(`unsupported package: ${name}`);
}
if (Object.values(result).some((value) => value === undefined || value === null)) throw new Error(`${name} returned missing parsed fields`);
return result;
}
