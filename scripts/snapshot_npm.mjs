// Capture registry discovery hits and comparable download counts for the pilot.
import { readFile, writeFile } from 'node:fs/promises';

const cell = process.argv[2] ?? 'png';
const querySets = {
  png: ['png', 'png decoder', 'png reader', 'png image'],
  zip: ['zip', 'zip archive', 'zip parser', 'zip reader']
};
if (!(cell in querySets)) throw new Error(`unsupported cell: ${cell}`);
const out = new URL(`../data/javascript/${cell}/registry-snapshot.json`, import.meta.url);
const parsers = JSON.parse(await readFile(new URL(`../data/javascript/${cell}/parsers.json`, import.meta.url)));
const queries = querySets[cell];
const metricWindow = '2026-10-11:2026-11-09';

async function json(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${response.status} ${url}`);
  return response.json();
}

const search = [];
for (const query of queries) {
  const url = `https://registry.npmjs.org/-/v1/search?text=${encodeURIComponent(query)}&size=100&from=0`;
  const response = await json(url);
  search.push({ query, url, total: response.total, hits: response.objects.map(({ package: p }, i) => ({ rank: i + 1, name: p.name, version: p.version, description: p.description ?? '', url: p.links?.npm ?? `https://www.npmjs.com/package/${p.name}` })) });
}

const releases = {};
const downloads = {};
for (const { name, version } of parsers) {
  const encoded = encodeURIComponent(name);
  const releaseUrl = `https://registry.npmjs.org/${encoded}/${version}`;
  const meta = await json(releaseUrl);
  releases[name] = { version, url: releaseUrl, license: meta.license ?? null, integrity: meta.dist?.integrity ?? null, repository: meta.repository?.url ?? null };
  const metricUrl = `https://api.npmjs.org/downloads/point/${metricWindow}/${encoded}`;
  const metric = await json(metricUrl);
  downloads[name] = { downloads: metric.downloads ?? null, start: metric.start ?? null, end: metric.end ?? null, url: metricUrl };
}

const snapshot = {
  captured_at_utc: new Date().toISOString(),
  search_api_docs: 'https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md',
  downloads_api_docs: 'https://github.com/npm/registry/blob/main/docs/download-counts.md',
  search_limit_per_query: 100,
  search,
  releases,
  download_metric: { name: 'npm registry tarball downloads', window: metricWindow, packages: downloads }
};
await writeFile(out, `${JSON.stringify(snapshot, null, 2)}\n`);
console.log(`Wrote ${out.pathname}`);
