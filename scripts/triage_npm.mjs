// Prioritize discovery leads by one metric. This file is NOT a parser ranking.
import { readFile, writeFile } from 'node:fs/promises';

const cell = process.argv[2];
if (!['png', 'zip'].includes(cell)) throw new Error('usage: node scripts/triage_npm.mjs png|zip');
const path = new URL(`../data/javascript/${cell}/registry-snapshot.json`, import.meta.url);
const snapshot = JSON.parse(await readFile(path));
const parsers = JSON.parse(await readFile(new URL(`../data/javascript/${cell}/parsers.json`, import.meta.url)));
const verifiedNames = new Set(parsers.map((parser) => parser.name));
const seen = new Map();
const relevant = cell === 'png'
  ? /\bpng\b|png[-.]|image (decoder|reader|parser|size)|image dimensions/i
  : /\bzip\b|zip[-.]|unzip|archive (reader|extractor|parser)/i;
const parseLikely = /decod|pars|read|load|extract|unzip|dimension|size|image|archive/i;
for (const search of snapshot.search) {
  for (const hit of search.hits) {
    if (!relevant.test(`${hit.name} ${hit.description}`) || !parseLikely.test(hit.description)) continue;
    if (!seen.has(hit.name)) seen.set(hit.name, { name: hit.name, description: hit.description, first_query: search.query, first_rank: hit.rank });
  }
}
const extra = cell === 'png'
  ? ['canvas', '@napi-rs/canvas', 'skia-canvas', 'probe-image-size', '@loaders.gl/images', 'image-js']
  : ['decompress', 'decompress-unzip', 'pizzip', 'yauzl-promise', 'node-zip', 'unzip-stream', 'unzip', '@endo/zip', '@electron-internal/extract-zip', 'zip-lib', 'zipread', '7zip-min'];
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
