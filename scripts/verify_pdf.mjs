import { readFile, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const root = new URL('../', import.meta.url);
const parsers = JSON.parse(await readFile(new URL('data/javascript/pdf/parsers.json', root)));
const control = 'controls/pdf/one-page.pdf';
const bytes = await readFile(new URL(control, root));
const expected = {
  text: { text: 'Parsarium' },
  page_metadata: { pages: 1, title: 'Parsarium PDF control' },
  page_count: { pages: 1 }
};
const results = [];
for (const { name, version, scope } of parsers) {
  const command = ['adapters/javascript/pdf.mjs', name, control];
  const run = spawnSync(process.execPath, command, { cwd: root.pathname, encoding: 'utf8' });
  let output = null;
  let pass = false;
  let error = null;
  try {
    if (run.status !== 0) throw new Error(run.stderr.trim().split('\n').at(-1) || `exit ${run.status}`);
    output = JSON.parse(run.stdout.trim().split('\n').at(-1));
    pass = JSON.stringify(output) === JSON.stringify(expected[scope]);
    if (!pass) error = 'output differs from expected PDF control result';
  } catch (cause) { error = String(cause); }
  results.push({ package: name, version, scope, command: `node ${command.join(' ')}`, pass, output, error });
}
const report = {
  checked_at_utc: new Date().toISOString(),
  platform: process.platform,
  architecture: process.arch,
  node: process.version,
  control,
  control_sha256: createHash('sha256').update(bytes).digest('hex'),
  expected,
  third_party: results
};
await writeFile(new URL('data/javascript/pdf/verification.json', root), `${JSON.stringify(report, null, 2)}\n`);
console.log(`${results.filter((result) => result.pass).length}/${results.length} PDF packages passed`);
if (results.some((result) => !result.pass)) process.exitCode = 1;
