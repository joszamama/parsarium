import { readFile, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const root = new URL('../', import.meta.url);
const parsers = JSON.parse(await readFile(new URL('data/javascript/mp4/parsers.json', root)));
const control = 'controls/mp4/red-av.mp4';
const bytes = await readFile(new URL(control, root));
const boxResult = { boxes: ['ftyp', 'moov', 'free', 'mdat'] };
const expected = {
  'music-metadata': { title: 'Parsarium', width: 2, height: 2, sampleRate: 8000 },
  'mediainfo.js': { title: 'Parsarium', width: 2, height: 2, sampleRate: 8000 },
  'codem-isoboxer': { ...boxResult, brand: 'isom' },
  'mp4box': { brand: 'isom', width: 2, height: 2, tracks: 2 },
  'isobmff-inspector': { ...boxResult, brand: 'isom' },
  'mediabunny': { format: 'MP4', duration: 1, width: 2, height: 2, audioCodec: 'aac' },
  '@audio/decode-mp4': { sampleRate: 8000, channels: 1, samples: 8000 },
  'jsmediatags': { type: 'MP4', brand: 'isom', title: 'Parsarium' },
  'mp4-box-encoding': { type: 'ftyp', brand: 'isom', compatible: ['isom', 'iso2', 'avc1', 'mp41'] },
  'node-video-lib': { duration: 1, tracks: 2 },
  'mp4reader': { brand: 'isom', handlers: ['vide', 'soun'] },
  'mediafile-metadata': { creationDate: '2020-01-02T03:04:05.000Z' },
  'mp4-parser': { title: 'Parsarium', duration: 1 },
  'mp4-stream': boxResult,
  'fmp4.js': boxResult,
  '@isomp4/parser': boxResult,
  'mp4tree': { valid: true, ...boxResult },
  'metaprobe': { kind: 'video', format: 'mp4', width: 2, height: 2, title: 'Parsarium', duration: 1 },
  '@dantheman827/taglib-ts': { title: 'Parsarium', sampleRate: 8000, channels: 1 },
  'mp4-metadata': { creationTime: '2020-01-02T03:04:05.000Z' }
};
const third_party = parsers.map(({ name, version, scope }) => {
  const command = ['adapters/javascript/mp4.mjs', name, control];
  const run = spawnSync(process.execPath, command, { cwd: root.pathname, encoding: 'utf8', timeout: 15000 });
  let output = null, pass = false, error = null;
  try {
    if (!expected[name]) throw new Error('missing expected result');
    if (run.error) throw run.error;
    if (run.status !== 0) throw new Error(run.stderr.trim().split('\n').at(-1) || `exit ${run.status}`);
    output = JSON.parse(run.stdout.trim().split('\n').at(-1));
    pass = JSON.stringify(output) === JSON.stringify(expected[name]);
    if (!pass) error = 'output differs from expected MP4 control result';
  } catch (cause) { error = String(cause); }
  return { package: name, version, scope, command: `node ${command.join(' ')}`, pass, output, error };
});
const browserCommand = ['adapters/javascript/mp4_browser.mjs', control];
const browserRun = spawnSync(process.execPath, browserCommand, { cwd: root.pathname, encoding: 'utf8', timeout: 15000 });
const runtime = { command: `node ${browserCommand.join(' ')}`, pass: false, output: null, error: null };
try {
  if (browserRun.error) throw browserRun.error;
  if (browserRun.status !== 0) throw new Error(browserRun.stderr.trim().split('\n').at(-1) || `exit ${browserRun.status}`);
  runtime.output = JSON.parse(browserRun.stdout.trim().split('\n').at(-1));
  runtime.pass = runtime.output.width === 2 && runtime.output.height === 2 && runtime.output.duration === 1;
  if (!runtime.pass) runtime.error = 'browser output differs from expected MP4 metadata';
} catch (cause) { runtime.error = String(cause); }
const report = {
  checked_at_utc: new Date().toISOString(), platform: process.platform, architecture: process.arch, node: process.version,
  control, control_sha256: createHash('sha256').update(bytes).digest('hex'), expected, third_party, runtime
};
await writeFile(new URL('data/javascript/mp4/verification.json', root), `${JSON.stringify(report, null, 2)}\n`);
console.log(`${third_party.filter((item) => item.pass).length}/${third_party.length} MP4 packages passed; browser runtime ${runtime.pass ? 'passed' : 'failed'}`);
if (third_party.some((item) => !item.pass) || !runtime.pass) process.exitCode = 1;
