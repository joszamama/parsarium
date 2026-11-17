import { readFile, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const root = new URL('../', import.meta.url);
const parsers = JSON.parse(await readFile(new URL('data/javascript/mp3_id3v2/parsers.json', root)));
const control = 'controls/mp3_id3v2/tone-tags.mp3';
const bytes = await readFile(new URL(control, root));
const tagResult = { title: 'Parsarium', artist: 'Control', album: 'Pilot' };
const expected = Object.fromEntries(parsers.map(({ name }) => [name, tagResult]));
Object.assign(expected, {
  'music-metadata': { ...tagResult, sampleRate: 8000 },
  'jsmediatags': { ...tagResult, version: '2.3.0' },
  '@audio/decode': { sampleRate: 8000, channels: 1, samples: 8000 },
  '@audio/decode-mp3': { sampleRate: 8000, channels: 2, samples: 8000 },
  'get-audio-duration': { duration_ms: 1152 },
  'id3js': { ...tagResult, version: [3, 0] },
  'mp3-duration': { duration_ms: 1224 },
  'get-mp3-duration': { duration_ms: 1224 },
  'audio-tag': { ...tagResult, format: 'mpeg' },
  'mp3-parser': { ...tagResult, version: 3 }
});
const third_party = parsers.map(({ name, version, scope }) => {
  const command = ['adapters/javascript/mp3_id3v2.mjs', name, control];
  const run = spawnSync(process.execPath, command, { cwd: root.pathname, encoding: 'utf8', timeout: 15000 });
  let output = null, pass = false, error = null;
  try {
    if (run.error) throw run.error;
    if (run.status !== 0) throw new Error(run.stderr.trim().split('\n').at(-1) || `exit ${run.status}`);
    output = JSON.parse(run.stdout.trim().split('\n').at(-1));
    pass = JSON.stringify(output) === JSON.stringify(expected[name]);
    if (!pass) error = 'output differs from expected MP3/ID3v2 control result';
  } catch (cause) { error = String(cause); }
  return { package: name, version, scope, command: `node ${command.join(' ')}`, pass, output, error };
});
const browserCommand = ['adapters/javascript/mp3_id3v2_browser.mjs', control];
const browserRun = spawnSync(process.execPath, browserCommand, { cwd: root.pathname, encoding: 'utf8', timeout: 15000 });
const runtime = { command: `node ${browserCommand.join(' ')}`, pass: false, output: null, error: null };
try {
  if (browserRun.error) throw browserRun.error;
  if (browserRun.status !== 0) throw new Error(browserRun.stderr.trim().split('\n').at(-1) || `exit ${browserRun.status}`);
  runtime.output = JSON.parse(browserRun.stdout.trim().split('\n').at(-1));
  runtime.pass = JSON.stringify(runtime.output.pcm) === JSON.stringify({ sampleRate: 8000, channels: 1, samples: 8000 }) && runtime.output.media.duration === 1;
  if (!runtime.pass) runtime.error = 'browser output differs from expected decoded audio and media duration';
} catch (cause) { runtime.error = String(cause); }
const report = {
  checked_at_utc: new Date().toISOString(), platform: process.platform, architecture: process.arch, node: process.version,
  control, control_sha256: createHash('sha256').update(bytes).digest('hex'), expected, third_party, runtime
};
await writeFile(new URL('data/javascript/mp3_id3v2/verification.json', root), `${JSON.stringify(report, null, 2)}\n`);
console.log(`${third_party.filter((item) => item.pass).length}/${third_party.length} MP3/ID3v2 packages passed; browser runtime ${runtime.pass ? 'passed' : 'failed'}`);
if (third_party.some((item) => !item.pass) || !runtime.pass) process.exitCode = 1;
