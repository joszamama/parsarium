// Replays both valid controls through the standard adapter: bytes -> strict UTF-8 TextDecoder -> JSON.parse.
// JSON.parse is native V8 C++, so the V8 coverage dump has no parser script; this records that, not lines.
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const outputDir = '/coverage';
const rawDir = path.join(outputDir, 'v8');
fs.mkdirSync(rawDir, { recursive: true });

function replay(control) {
  const child = spawnSync(process.execPath, ['/work/adapter.mjs', control], {
    encoding: 'utf8',
    env: { ...process.env, NODE_V8_COVERAGE: rawDir },
  });
  if (child.status !== 0) throw new Error(`control replay failed: ${child.stderr}`);
  return JSON.parse(child.stdout.trim());
}

const expected = {"arrays": 3, "booleans": 2, "max_depth": 4, "nulls": 1, "numbers": [-2.5, 1, 1, 2, 2], "objects": 5, "root": "object", "strings": ["café \"quoted\"", "go", "json", "parsarium", "rfc8259"], "top_level_keys": ["enabled", "missing", "name", "nested", "ratio", "tags", "version"]};
const secondExpected = {"arrays": 4, "booleans": 2, "max_depth": 3, "nulls": 1, "numbers": [0.25, 1], "objects": 2, "root": "array", "strings": ["A", "two"], "top_level_items": 5};
const observed = replay('/input/control');
if (JSON.stringify(observed) !== JSON.stringify(expected)) {
  throw new Error(`control mismatch: ${JSON.stringify(observed)}`);
}
const second = replay('/work/second-control.json');
if (JSON.stringify(second) !== JSON.stringify(secondExpected)) {
  throw new Error(`second control mismatch: ${JSON.stringify(second)}`);
}

const scriptUrls = new Set();
for (const file of fs.readdirSync(rawDir)) {
  if (!file.startsWith('coverage-') || !file.endsWith('.json')) continue;
  const raw = JSON.parse(fs.readFileSync(path.join(rawDir, file), 'utf8'));
  for (const script of raw.result) scriptUrls.add(script.url);
}
const urls = [...scriptUrls].sort();
if (!urls.includes('file:///work/adapter.mjs')) throw new Error('V8 coverage did not record the adapter');
const parserScripts = urls.filter(url => /json/i.test(url) && url !== 'file:///work/adapter.mjs');
if (parserScripts.length) throw new Error(`unexpected JSON script in V8 coverage: ${parserScripts}`);

const summary = {
  control_pass: true,
  output: observed,
  second_control_output: second,
  v8_coverage_scripts: urls.length,
  json_parser_scripts: 0,
  parser_source_files: null,
  parser_source_lines_covered: null,
  coverage: '/coverage/coverage.json',
};
fs.writeFileSync(path.join(outputDir, 'observed.json'), JSON.stringify(observed, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'coverage.json'), JSON.stringify({ data: [{ files: [] }], v8_script_urls: urls }, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify(summary));
