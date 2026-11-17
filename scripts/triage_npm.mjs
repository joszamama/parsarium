// Prioritize discovery leads by one metric. This file is NOT a parser ranking.
import { readFile, writeFile } from 'node:fs/promises';

const cell = process.argv[2];
if (!['png', 'zip', 'mp4', 'mp3', 'wav', 'pdf', 'svg', 'http11', 'ascii_pnm', 'ascii_ply'].includes(cell)) throw new Error('usage: node scripts/triage_npm.mjs png|zip|mp4|mp3|wav|pdf|svg|http11|ascii_pnm|ascii_ply');
const path = new URL(`../data/javascript/${cell}/registry-snapshot.json`, import.meta.url);
const snapshot = JSON.parse(await readFile(path));
const parsers = JSON.parse(await readFile(new URL(`../data/javascript/${cell}/parsers.json`, import.meta.url)));
const verifiedNames = new Set(parsers.map((parser) => parser.name));
const seen = new Map();
const relevant = cell === 'png'
  ? /\bpng\b|png[-.]|image (decoder|reader|parser|size)|image dimensions/i
  : cell === 'zip'
    ? /\bzip\b|zip[-.]|unzip|archive (reader|extractor|parser)/i
    : cell === 'mp4'
      ? /\bmp4\b|mp4[-.]|isobmff|iso.?bmff|mpeg[- ]?4|quicktime|video metadata/i
    : cell === 'mp3'
      ? /\bmp3\b|mp3[-.]|id3v2|id3[-.]|audio metadata|audio tag/i
    : cell === 'wav'
      ? /\bwav\b|wavefile|wave audio|audio (decoder|reader|parser|metadata)/i
      : cell === 'pdf'
        ? /\bpdf\b|pdf[-.]|portable document/i
        : cell === 'svg'
          ? /\bsvg\b|svg[-.]|scalable vector/i
          : cell === 'ascii_ply'
            ? /\bply\b|PLYLoader|polygon file format|stanford triangle/i
          : cell === 'ascii_pnm'
            ? /\bpnm\b|\bnetpbm\b|\bppm\b|\bpgm\b|\bpbm\b|portable (pixmap|graymap|bitmap)/i
            : /\bhttp\b|http[-.]|HTTP\/1\.1|request (parser|reader)|response (parser|reader)/i;
const parseLikely = /decod|pars|read|load|extract|unzip|dimension|size|image|archive|audio|riff|wav|text|page|render|document/i;
for (const search of snapshot.search) {
  for (const hit of search.hits) {
    if (!relevant.test(`${hit.name} ${hit.description}`) || !parseLikely.test(hit.description)) continue;
    if (!seen.has(hit.name)) seen.set(hit.name, { name: hit.name, description: hit.description, first_query: search.query, first_rank: hit.rank });
  }
}
const extra = cell === 'png'
  ? ['canvas', '@napi-rs/canvas', 'skia-canvas', 'probe-image-size', '@loaders.gl/images', 'image-js']
  : cell === 'zip'
    ? ['decompress', 'decompress-unzip', 'pizzip', 'yauzl-promise', 'node-zip', 'unzip-stream', 'unzip', '@endo/zip', '@electron-internal/extract-zip', 'zip-lib', 'zipread', '7zip-min']
    : cell === 'mp4'
      ? ['mp4box', 'codem-isoboxer', 'isobmff-inspector', 'fmp4.js', 'mp4', 'mp4.js', 'mp4-parser', 'mp4-parser-js', 'mp4-info', 'mp4-stream', 'mp4frag', 'mediainfo.js', 'music-metadata', 'mediabunny', '@remotion/media-parser', 'get-video-duration', 'get-video-dimensions', 'mux.js', '@videojs/mp4', 'mp4box.js', 'metaprobe']
    : cell === 'mp3'
      ? ['music-metadata', 'mediainfo.js', 'jsmediatags', '@dantheman827/taglib-ts', 'node-id3', 'id3-parser', 'id3js', 'mp3tag.js', 'mp3-parser', 'mp3-duration', 'get-mp3-duration', 'get-audio-duration', '@audio/decode-mp3', 'mp3-decoder', 'lamejs', 'id3v2', 'id3v2-parser', 'audio-decode']
    : cell === 'wav'
      ? ['wavefile', 'wav-decoder', 'node-wav', 'wav', 'music-metadata', 'music-metadata-browser', 'audio-decode', '@audio/decode', '@audio/decode-wav', 'get-audio-duration', 'mediainfo.js', '@uttori/audio-wave', 'riff-reader']
      : cell === 'pdf'
        ? ['pdfjs-dist', 'pdf-parse', 'pdf-lib', 'pdf2json', 'pdfreader', 'pdf-extraction', 'pdf-to-text', 'pdf-text-extract', 'pdf-extract', 'pdf-parser', 'mupdf', 'pdfjs', 'pdf-parse-new', 'pdfnative']
        : cell === 'svg'
          ? ['svg-parser', 'canvg', 'sharp', '@resvg/resvg-js', '@resvg/resvg-wasm', '@cf-wasm/resvg', '@stacksjs/ts-svg', 'svgson', 'svgps', 'postsvg', 'streaming-svg-parser', 'svg2img', 'svg-to-img', '@svgdotjs/svg.js', 'svgdom', 'svgo', 'svg-size', 'get-svg-colors', 'probe-image-size', 'image-size', 'canvas', '@napi-rs/canvas', 'skia-canvas', 'svg-eslint-parser', 'vsvg-parser', '@yworks/canvg', 'svg-to-pdfkit', 'svgicons2svgfont', '@react-pdf/svg', 'react-inlinesvg']
          : cell === 'ascii_ply'
            ? ['three', 'three-stdlib', '@loaders.gl/core', '@loaders.gl/ply', '@loaders.gl/pointclouds', 'parse-ply', 'plyparser', 'ply-js', '@draco-rust/ply', 'three-ply-loader', 'threejs-ply-loader', 'three-ply-loader-ts', '@kibeo/loaders.gl-ply', '@isopodlabs/binary_meshes', '@meshioplusplus/wasm', '@dp-software/point-cloud-wasm', 'online-3d-viewer', '@playcanvas/engine', '@playcanvas/splat-transform', 'spz-js', '3dgs-ply-3dtiles-converter', '3dgs-loader', '@wangyoumo/gs3d-loader', '@sruim/mesh-flow', '@voxelkloud/format-single', '@voxelkloud/wasm-build', 'point-cloud-convert', 'sunzi-plyloader', 'modeltree', '@file-viewer/renderer-3d', 'threepipe', '@combos-fun/plugin-renderer-3d-model', 'meshlab-ts']
          : cell === 'ascii_pnm'
            ? ['image-size', 'image-size-next', 'image-size-safe', '@nous-research/image-size', '@localnerve/image-size', 'tiny-image-size', '@portable/image-size', 'view-image-size', 'fastimage', 'image-meta', '@napi-rs/image', 'netpbm-parser', '@jdmichaud/netpbm', 'ppm', 'ppm-parser', 'pgmjs', 'pgmts', 'dumb-pgm', '@lp-labs/ppm-image-codec', '@fitbit/portable-pixmap', '@catlabtech/webcvt-image-legacy', 'pnm', '@imgdrop/pnm', 'pnm-convertor', '@thi.ng/pixel-io-netpbm', '@designliquido/delegua-imagens', 'image-in-browser', 'imagescript', 'purejsimage']
            : ['http-parser-js', 'http-string-parser', 'raw-http-parser', 'parse-http', 'http-parse', 'http-parser', 'llhttp', 'http-message-parser', 'parse-raw-http', '@caido-utils/parser', 'http-parser-wasm', 'http-z', '@ibiwan/http-message-parser', 'http-message-parser-ts', 'raw-request-parser', 'http-headers', 'http-request-parser', '@alikia/http-parser', '@browsercore/http1'];
for (const name of extra) if (!seen.has(name)) seen.set(name, { name, description: 'Documentation lead; description not captured in registry search window.', first_query: 'project documentation', first_rank: null });

const names = [...seen.keys()];
const downloads = new Map();
const period = '2026-10-11:2026-11-09';
async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${response.status} ${url}`);
  return response.json();
}
const unscoped = names.filter((name) => !name.startsWith('@'));
for (let i = 0; i < unscoped.length; i += 100) {
  const batch = unscoped.slice(i, i + 100);
  const url = `https://api.npmjs.org/downloads/point/${period}/${batch.map(encodeURIComponent).join(',')}`;
  const response = await fetchJson(url);
  for (const name of batch) downloads.set(name, response[name]?.downloads ?? null);
}
const scoped = names.filter((name) => name.startsWith('@'));
for (let i = 0; i < scoped.length; i += 8) {
  await Promise.all(scoped.slice(i, i + 8).map(async (name) => {
    const url = `https://api.npmjs.org/downloads/point/${period}/${encodeURIComponent(name)}`;
    try { downloads.set(name, (await fetchJson(url)).downloads ?? null); }
    catch { downloads.set(name, null); }
  }));
}
for (const name of scoped.filter((name) => downloads.get(name) == null)) {
  const url = `https://api.npmjs.org/downloads/point/${period}/${encodeURIComponent(name)}`;
  try { downloads.set(name, (await fetchJson(url)).downloads ?? null); }
  catch { /* Preserve missing data as null. */ }
}
for (const [name, record] of Object.entries(snapshot.download_metric.packages)) {
  downloads.set(name, record.downloads);
}
const leads = [...seen.values()].map((hit) => ({ ...hit, downloads: downloads.get(hit.name) ?? null, status: verifiedNames.has(hit.name) ? 'verified_in_parsers_json' : 'search_hit_unverified' }));
leads.sort((a, b) => (b.downloads ?? -1) - (a.downloads ?? -1));
const out = new URL(`../data/javascript/${cell}/triage.json`, import.meta.url);
await writeFile(out, `${JSON.stringify({ captured_at_utc: new Date().toISOString(), metric_window: period, notice: 'Download counts prioritize leads only; none of these rows is evidence that a package parses the format.', leads }, null, 2)}\n`);
console.log(`${leads.length} registry and documentation hits saved to ${out.pathname}`);
