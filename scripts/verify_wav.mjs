import { readFile, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const root = new URL('../', import.meta.url);
const parsers = JSON.parse(await readFile(new URL('data/javascript/wav/parsers.json', root)));
const control = 'controls/wav/four-samples.wav';
const bytes = await readFile(new URL(control, root));
const expected = {
  samples: { sampleRate: 8000, channels: 1, sampleCount: 4, sampleSigns: [0, 1, -1, 0] },
  header: { sampleRate: 8000, channels: 1, bitsPerSample: 16 },
  duration: { durationSeconds: 0.0005 }
};
function run(command, kind) {
  const processResult = spawnSync(process.execPath, command, { cwd: root.pathname, encoding: 'utf8' });
  let output = null;
  let pass = false;
  let error = null;
  try {
    if (processResult.status !== 0) throw new Error(processResult.stderr.trim() || `exit ${processResult.status}`);
    output = JSON.parse(processResult.stdout.trim());
    if (kind === 'browser') {
      const { browser, ...parsed } = output;
      pass = Boolean(browser) && JSON.stringify(parsed) === JSON.stringify(expected.samples);
    } else {
      pass = JSON.stringify(output) === JSON.stringify(expected[kind]);
    }
    if (!pass) error = 'output differs from the expected WAV control fields';
  } catch (cause) { error = String(cause); }
  return { command: `node ${command.join(' ')}`, pass, output, error };
}
const results = parsers.map(({ name, version, scope }) => ({
  package: name, version, scope,
  ...run(['adapters/javascript/wav.mjs', name, control], scope)
}));
const browser = run(['adapters/javascript/wav_browser.mjs', control], 'browser');
const report = {
  checked_at_utc: new Date().toISOString(),
  platform: process.platform,
  architecture: process.arch,
  node: process.version,
  playwright_version: '1.63.0',
  control,
  control_sha256: createHash('sha256').update(bytes).digest('hex'),
  expected,
  third_party: results,
  runtime: browser
};
await writeFile(new URL('data/javascript/wav/verification.json', root), `${JSON.stringify(report, null, 2)}\n`);
console.log(`${results.filter((result) => result.pass).length}/${results.length} packages, browser ${browser.pass ? 'passed' : 'failed'}`);
if (results.some((result) => !result.pass) || !browser.pass) process.exitCode = 1;
