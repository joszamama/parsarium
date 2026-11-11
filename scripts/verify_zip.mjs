import { readFile, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const root = new URL('../', import.meta.url);
const parsers = JSON.parse(await readFile(new URL('data/javascript/zip/parsers.json', root)));
const control = 'controls/zip/hello.zip';
const bytes = await readFile(new URL(control, root));
const expected = { entries: ['hello.txt'], content: 'parsarium\n' };

function run(command) {
  const processResult = spawnSync(process.execPath, command, { cwd: root.pathname, encoding: 'utf8' });
  let output = null;
  let pass = false;
  let error = null;
  try {
    if (processResult.status !== 0) throw new Error(processResult.stderr.trim() || `exit ${processResult.status}`);
    output = JSON.parse(processResult.stdout.trim());
    pass = JSON.stringify(output) === JSON.stringify(expected);
    if (!pass) error = 'output differs from expected ZIP entry and content';
  } catch (cause) { error = String(cause); }
  return { command: `node ${command.join(' ')}`, pass, output, error };
}

const results = parsers.map(({ name, version }) => ({ package: name, version, ...run(['adapters/javascript/zip.mjs', name, control]) }));
const runtime = { runtime: `Node.js ${process.version}`, ...run(['adapters/javascript/zip_node.mjs', control]) };
const report = {
  checked_at_utc: new Date().toISOString(),
  platform: process.platform,
  architecture: process.arch,
  node: process.version,
  control,
  control_sha256: createHash('sha256').update(bytes).digest('hex'),
  expected,
  third_party: results,
  runtime
};
await writeFile(new URL('data/javascript/zip/verification.json', root), `${JSON.stringify(report, null, 2)}\n`);
console.log(`${results.filter((r) => r.pass).length}/${results.length} packages, Node built-in ${runtime.pass ? 'passed' : 'failed'}`);
if (results.some((r) => !r.pass) || !runtime.pass) process.exitCode = 1;
