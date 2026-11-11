import { readFile, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const root = new URL('../', import.meta.url);
const parsers = JSON.parse(await readFile(new URL('data/javascript/svg/parsers.json', root)));
const control = 'controls/svg/red-green.svg';
const bytes = await readFile(new URL(control, root));
const fills = ['#ff0000', '#00ff00'];
const expected = {
  dimensions: { width: 2, height: 1, format: 'svg' },
  pixels: { width: 2, height: 1, rgba: [255, 0, 0, 255, 0, 255, 0, 255] },
  structure: { width: 2, height: 1, rects: 2, fills },
  paths: { width: 2, height: 1, paths: 2, fills },
  optimized_paths: { paths: 2, fills },
  colors: { fills }
};
const third_party = parsers.map(({ name, version, scope }) => {
  const command = ['adapters/javascript/svg.mjs', name, control];
  const run = spawnSync(process.execPath, command, { cwd: root.pathname, encoding: 'utf8', timeout: 10000 });
  let output = null, pass = false, error = null;
  try {
    if (run.error) throw run.error;
    if (run.status !== 0) throw new Error(run.stderr.trim().split('\n').at(-1) || `exit ${run.status}`);
    output = JSON.parse(run.stdout.trim().split('\n').at(-1));
    pass = JSON.stringify(output) === JSON.stringify(expected[scope]);
    if (!pass) error = 'output differs from expected SVG control result';
  } catch (cause) { error = String(cause); }
  return { package: name, version, scope, command: `node ${command.join(' ')}`, pass, output, error };
});
const browserCommand = ['adapters/javascript/svg_browser.mjs', control];
const browserRun = spawnSync(process.execPath, browserCommand, { cwd: root.pathname, encoding: 'utf8', timeout: 10000 });
const runtime = { command: `node ${browserCommand.join(' ')}`, pass: false, output: null, error: null };
try {
  if (browserRun.error) throw browserRun.error;
  if (browserRun.status !== 0) throw new Error(browserRun.stderr.trim().split('\n').at(-1) || `exit ${browserRun.status}`);
  runtime.output = JSON.parse(browserRun.stdout.trim().split('\n').at(-1));
  const dom = { ...expected.structure, typed_root: true, typed_rects: true };
  runtime.pass = JSON.stringify(runtime.output.dom) === JSON.stringify(dom) &&
    JSON.stringify(runtime.output.image) === JSON.stringify(expected.pixels);
  if (!runtime.pass) runtime.error = 'browser output differs from expected SVG DOM/image results';
} catch (cause) { runtime.error = String(cause); }
const report = {
  checked_at_utc: new Date().toISOString(), platform: process.platform, architecture: process.arch, node: process.version,
  control, control_sha256: createHash('sha256').update(bytes).digest('hex'), expected, third_party, runtime
};
await writeFile(new URL('data/javascript/svg/verification.json', root), `${JSON.stringify(report, null, 2)}\n`);
console.log(`${third_party.filter((item) => item.pass).length}/${third_party.length} SVG packages passed; browser runtime ${runtime.pass ? 'passed' : 'failed'}`);
if (third_party.some((item) => !item.pass) || !runtime.pass) process.exitCode = 1;
