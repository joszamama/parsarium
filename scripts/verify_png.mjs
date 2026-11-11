import { readFile, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const root = new URL('../', import.meta.url);
const parsers = JSON.parse(await readFile(new URL('data/javascript/png/parsers.json', root)));
const control = 'controls/png/red-green.png';
const png = await readFile(new URL(control, root));
const expectedRgba = [255, 0, 0, 255, 0, 255, 0, 255];
const expectedChunks = ['IHDR', 'IDAT', 'IEND'];
const results = [];
for (const parser of parsers) {
  const command = ['adapters/javascript/png.mjs', parser.name, control];
  const run = spawnSync(process.execPath, command, { cwd: root.pathname, encoding: 'utf8' });
  let output = null;
  let pass = false;
  let error = null;
  try {
    if (run.status !== 0) throw new Error(run.stderr.trim() || `exit ${run.status}`);
    output = JSON.parse(run.stdout.trim());
    pass = parser.scope === 'chunks'
      ? JSON.stringify(output.chunks) === JSON.stringify(expectedChunks)
      : output.width === 2 && output.height === 1 && (parser.scope === 'pixels'
        ? JSON.stringify(output.rgba) === JSON.stringify(expectedRgba)
        : output.type === 'png');
    if (!pass) error = 'output differs from expected control fields';
  } catch (cause) { error = String(cause); }
  results.push({ package: parser.name, version: parser.version, command: `node ${command.join(' ')}`, pass, output, error });
}
const report = {
  checked_at_utc: new Date().toISOString(),
  platform: process.platform,
  architecture: process.arch,
  node: process.version,
  control,
  control_sha256: createHash('sha256').update(png).digest('hex'),
  expected: { width: 2, height: 1, rgba: expectedRgba, chunks: expectedChunks },
  results
};
await writeFile(new URL('data/javascript/png/verification.json', root), `${JSON.stringify(report, null, 2)}\n`);
console.log(`${results.filter((r) => r.pass).length}/${results.length} parser adapters passed`);
const browserCommand = ['adapters/javascript/png_browser.mjs', control];
const browserRun = spawnSync(process.execPath, browserCommand, { cwd: root.pathname, encoding: 'utf8' });
let browserOutput = null;
let browserPass = false;
let browserError = null;
try {
  if (browserRun.status !== 0) throw new Error(browserRun.stderr.trim() || `exit ${browserRun.status}`);
  browserOutput = JSON.parse(browserRun.stdout.trim());
  browserPass = browserOutput.width === 2 && browserOutput.height === 1 &&
    JSON.stringify(browserOutput.rgba) === JSON.stringify(expectedRgba);
  if (!browserPass) browserError = 'output differs from expected control fields';
} catch (cause) { browserError = String(cause); }
await writeFile(new URL('data/javascript/png/browser-verification.json', root), `${JSON.stringify({
  checked_at_utc: new Date().toISOString(),
  command: `node ${browserCommand.join(' ')}`,
  playwright_version: '1.63.0',
  pass: browserPass,
  output: browserOutput,
  error: browserError
}, null, 2)}\n`);
console.log(`browser createImageBitmap ${browserPass ? 'passed' : 'failed'}`);
if (results.some((r) => !r.pass) || !browserPass) process.exitCode = 1;
