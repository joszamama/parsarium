import { readFile, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';

const root = new URL('../', import.meta.url);
const directory = new URL('data/javascript/ascii_ply/', root);
const parsers = JSON.parse(await readFile(new URL('parsers.json', directory)));
const packageManifest = JSON.parse(await readFile(new URL('package.json', root)));
const seen = new Set();
const controls = {};
const third_party = [];
for (const parser of parsers) {
  if (seen.has(parser.name)) throw new Error(`duplicate package path: ${parser.name}`);
  seen.add(parser.name);
  if (packageManifest.dependencies[parser.name] !== parser.version) {
    throw new Error(`${parser.name} is not pinned to ${parser.version} in package.json`);
  }
  if (!(parser.control in controls)) {
    const bytes = await readFile(new URL(parser.control, root));
    controls[parser.control] = createHash('sha256').update(bytes).digest('hex');
  }
  const command = ['adapters/javascript/ascii_ply.mjs', parser.name, parser.control];
  const run = spawnSync(process.execPath, command, {
    cwd: root.pathname, encoding: 'utf8', timeout: 30000
  });
  let output = null, pass = false, error = null;
  try {
    if (run.error) throw run.error;
    if (run.status !== 0) throw new Error(run.stderr.trim().split('\n').at(-1) || `exit ${run.status}`);
    output = JSON.parse(run.stdout.trim().split('\n').at(-1));
    pass = isDeepStrictEqual(output, parser.expected_output);
    if (!pass) error = 'output differs from the valid ASCII PLY control';
  } catch (cause) { error = String(cause); }
  third_party.push({ package: parser.name, version: parser.version, scope: parser.scope,
    command: `node ${command.join(' ')}`, pass, output, error });
}

const report = {
  checked_at_utc: new Date().toISOString(), platform: process.platform,
  architecture: process.arch, node: process.version,
  controls, third_party, runtime: []
};
await writeFile(new URL('verification.json', directory), `${JSON.stringify(report, null, 2)}\n`);
console.log(`${third_party.filter((item) => item.pass).length}/${third_party.length} ASCII PLY packages passed`);
if (third_party.some((item) => !item.pass)) process.exitCode = 1;
