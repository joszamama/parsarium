import { readFile, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';

const root = new URL('../', import.meta.url);
const directory = new URL('data/javascript/ascii_pnm/', root);
const parsers = JSON.parse(await readFile(new URL('parsers.json', directory)));
const controls = {};
const third_party = [];
for (const parser of parsers) {
  const control = parser.control;
  if (!(control in controls)) {
    const bytes = await readFile(new URL(control, root));
    controls[control] = createHash('sha256').update(bytes).digest('hex');
  }
  const command = ['adapters/javascript/ascii_pnm.mjs', parser.name, control];
  const run = spawnSync(process.execPath, command, { cwd: root.pathname, encoding: 'utf8', timeout: 10000 });
  let output = null, pass = false, error = null;
  try {
    if (run.error) throw run.error;
    if (run.status !== 0) throw new Error(run.stderr.trim().split('\n').at(-1) || `exit ${run.status}`);
    output = JSON.parse(run.stdout.trim().split('\n').at(-1));
    pass = isDeepStrictEqual(output, parser.expected_output);
    if (!pass) error = 'output differs from the valid ASCII PNM control';
  } catch (cause) { error = String(cause); }
  third_party.push({ package: parser.name, version: parser.version, scope: parser.scope,
    command: `node ${command.join(' ')}`, pass, output, error });
}

const browserCommand = ['adapters/javascript/ascii_pnm_browser.mjs', 'controls/ascii_pnm/red-green.ppm'];
const browserRun = spawnSync(process.execPath, browserCommand, {
  cwd: root.pathname, encoding: 'utf8', timeout: 10000
});
const browser_probe = { command: `node ${browserCommand.join(' ')}`, ran: false, output: null, error: null };
try {
  if (browserRun.error) throw browserRun.error;
  if (browserRun.status !== 0) throw new Error(browserRun.stderr.trim().split('\n').at(-1) || `exit ${browserRun.status}`);
  browser_probe.output = JSON.parse(browserRun.stdout.trim().split('\n').at(-1));
  browser_probe.ran = true;
} catch (cause) { browser_probe.error = String(cause); }

const report = {
  checked_at_utc: new Date().toISOString(), platform: process.platform,
  architecture: process.arch, node: process.version,
  controls, third_party, runtime: [], browser_probe
};
await writeFile(new URL('verification.json', directory), `${JSON.stringify(report, null, 2)}\n`);
console.log(`${third_party.filter((item) => item.pass).length}/${third_party.length} ASCII PNM packages passed; browser probe ${browser_probe.ran ? 'ran' : 'failed to run'}`);
if (third_party.some((item) => !item.pass) || !browser_probe.ran) process.exitCode = 1;
