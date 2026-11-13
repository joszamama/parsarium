import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createRequire } from 'node:module';
import { build } from 'esbuild';

const root = new URL('../../', import.meta.url);
const lock = JSON.parse(await readFile(new URL('data/javascript/matrix_market/graphbox-source-lock.json', root)));
const [controlPath] = process.argv.slice(2);
if (!controlPath) throw new Error('expected one local Matrix Market path');
const require = createRequire(import.meta.url);
if (require('esbuild/package.json').version !== '0.25.12') throw new Error('esbuild release differs from lock');

const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const control = await readFile(controlPath);
if (hash(control) !== lock.control_sha256) throw new Error('control hash differs from lock');
const response = await fetch(lock.source_url);
if (!response.ok) throw new Error(`GraphBox source download failed: ${response.status}`);
const archive = Buffer.from(await response.arrayBuffer());
if (hash(archive) !== lock.source_sha256) throw new Error('GraphBox source hash differs from lock');

const directory = await mkdtemp(join(tmpdir(), 'parsarium-graphbox-mtx-'));
try {
  const archivePath = join(directory, 'source.tar.gz');
  await writeFile(archivePath, archive);
  const listing = spawnSync('tar', ['-tzf', archivePath], { encoding: 'utf8', timeout: 30000 });
  if (listing.status !== 0) throw new Error(listing.stderr);
  for (const member of listing.stdout.trim().split('\n')) {
    if (!member.startsWith('GraphBox-1.4.6/') || member.split('/').includes('..')) {
      throw new Error(`unexpected archive member: ${member}`);
    }
  }
  const extracted = spawnSync('tar', ['-xzf', archivePath, '-C', directory],
    { encoding: 'utf8', timeout: 30000 });
  if (extracted.status !== 0) throw new Error(extracted.stderr);
  const source = join(directory, 'GraphBox-1.4.6');
  for (const [member, expected] of Object.entries(lock.source_members)) {
    if (hash(await readFile(join(source, member))) !== expected) {
      throw new Error(`GraphBox source member hash differs: ${member}`);
    }
  }
  const metadata = JSON.parse(await readFile(join(source, 'package.json')));
  if (metadata.version !== lock.release || metadata.license !== lock.license) {
    throw new Error('GraphBox release metadata differs from lock');
  }
  const publicApi = await readFile(join(source, 'src/formats/mtx/index.ts'), 'utf8');
  if (!publicApi.includes('export { mtxToJson, parseMtx } from "./parse"')) {
    throw new Error('tagged source no longer exports parseMtx');
  }
  const built = await build({
    entryPoints: [join(source, 'src/formats/mtx/parse.ts')],
    bundle: true, platform: 'node', format: 'esm', write: false, logLevel: 'silent',
  });
  const url = `data:text/javascript;base64,${Buffer.from(built.outputFiles[0].contents).toString('base64')}`;
  const { parseMtx } = await import(url);
  const parsed = parseMtx(control.toString('utf8'));
  const target = parsed.entries.find((entry) => entry.row === 1 && entry.col === 3);
  console.log(JSON.stringify({
    rows: parsed.rows, cols: parsed.cols, entries: parsed.entries.length,
    value_1_3: target?.value ?? null, valueType: parsed.valueType, symmetry: parsed.symmetry,
  }));
} finally {
  await rm(directory, { recursive: true, force: true });
}
