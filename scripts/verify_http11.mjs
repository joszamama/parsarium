import { readFile, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const root = new URL('../', import.meta.url);
const parsers = JSON.parse(await readFile(new URL('data/javascript/http11/parsers.json', root)));
const controls = { request: 'controls/http11/request.http', response: 'controls/http11/response.http' };
const expected = { request: { method: 'GET', target: '/parsarium?x=1' }, response: { status: 200, body: 'parsarium' } };
const hashes = {};
for (const [kind, path] of Object.entries(controls)) hashes[kind] = createHash('sha256').update(await readFile(new URL(path, root))).digest('hex');

function check(command, expect) {
  const run = spawnSync(process.execPath, command, { cwd: root.pathname, encoding: 'utf8', timeout: 10000 });
  let output = null;
  let pass = false;
  let error = null;
  try {
    if (run.error) throw run.error;
    if (run.status !== 0) throw new Error(run.stderr.trim().split('\n').at(-1) || `exit ${run.status}`);
    output = JSON.parse(run.stdout.trim().split('\n').at(-1));
    pass = JSON.stringify(output) === JSON.stringify(expect);
    if (!pass) error = 'output differs from expected HTTP/1.1 control result';
  } catch (cause) { error = String(cause); }
  return { command: `node ${command.join(' ')}`, pass, output, error };
}

const third_party = parsers.map(({ name, version, scope }) => ({
  package: name, version, scope,
  ...check(['adapters/javascript/http11.mjs', name, controls[scope]], expected[scope])
}));
const runtime = { api: 'node:http.createServer', ...check(['adapters/javascript/http11_node.mjs', controls.request], expected.request) };
const report = {
  checked_at_utc: new Date().toISOString(), platform: process.platform, architecture: process.arch, node: process.version,
  controls, control_sha256: hashes, expected, third_party, runtime
};
await writeFile(new URL('data/javascript/http11/verification.json', root), `${JSON.stringify(report, null, 2)}\n`);
console.log(`${third_party.filter((item) => item.pass).length}/${third_party.length} HTTP/1.1 packages passed; Node runtime ${runtime.pass ? 'passed' : 'failed'}`);
if (third_party.some((item) => !item.pass) || !runtime.pass) process.exitCode = 1;
