const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { fileURLToPath } = require('node:url');
const { spawnSync } = require('node:child_process');

const PACKAGE_URL = 'file:///work/node_modules/toml-eslint-parser/';
const outputDir = '/coverage';
const rawDir = path.join(outputDir, 'v8');
fs.mkdirSync(rawDir, { recursive: true });
const child = spawnSync(process.execPath, ['/work/replay.js', '/input/control'], {
  encoding: 'utf8',
  env: { ...process.env, NODE_V8_COVERAGE: rawDir },
});
if (child.status !== 0) {
  throw new Error(`control replay failed: ${child.stderr}`);
}
// expected-trees.json holds the typed trees of both TOML controls, keyed by control
// SHA-256; they are copies of controls/toml/*.expected.json (hand-written from the
// TOML 1.0.0 specification and checked against Python tomllib).
const observedText = child.stdout.trim();
const observed = JSON.parse(observedText);
const digest = crypto.createHash('sha256').update(fs.readFileSync('/input/control')).digest('hex');
const expected = JSON.parse(fs.readFileSync('/work/expected-trees.json', 'utf8'))[digest];
const canonical = node => JSON.stringify(sortKeys(node));
function sortKeys(node) {
  if (Array.isArray(node)) return node.map(sortKeys);
  if (node !== null && typeof node === 'object') {
    return Object.fromEntries(Object.keys(node).sort().map(key => [key, sortKeys(node[key])]));
  }
  return node;
}
// Any other valid input reports the typed tree the parser produced in the mismatch message.
if (!expected || canonical(observed) !== canonical(expected.tree)) {
  throw new Error(`control typed tree mismatch: ${observedText}`);
}

function coveredLines(source, functions) {
  const executed = [];
  let start = 0;
  let lineNumber = 1;
  for (const line of source.split('\n')) {
    const end = start + line.length;
    let covered = false;
    for (let offset = start; offset < end && !covered; offset++) {
      if (/\s/.test(source[offset])) continue;
      let smallest = Infinity;
      let count = 0;
      for (const fn of functions) {
        for (const range of fn.ranges) {
          if (range.startOffset <= offset && offset < range.endOffset &&
              range.endOffset - range.startOffset < smallest) {
            smallest = range.endOffset - range.startOffset;
            count = range.count;
          }
        }
      }
      covered = count > 0;
    }
    if (covered) executed.push(lineNumber);
    start = end + 1;
    lineNumber++;
  }
  return executed;
}

const scripts = new Map();
for (const file of fs.readdirSync(rawDir)) {
  if (!file.startsWith('coverage-') || !file.endsWith('.json')) continue;
  const raw = JSON.parse(fs.readFileSync(path.join(rawDir, file), 'utf8'));
  for (const script of raw.result) {
    if (!script.url.startsWith(PACKAGE_URL)) continue;
    scripts.set(fileURLToPath(script.url), script.functions);
  }
}
const files = [];
for (const [filename, functions] of [...scripts.entries()].sort()) {
  const lines = coveredLines(fs.readFileSync(filename, 'utf8'), functions);
  files.push({ filename, summary: { lines: { covered: lines.length } }, executed_lines: lines });
}
const covered = files.reduce((sum, file) => sum + file.summary.lines.covered, 0);
if (covered === 0) throw new Error('no parser package source lines covered');
const coverage = { data: [{ files }] };
const summary = {
  control_pass: true,
  control_sha256: digest,
  output: observed,
  tree_matches_expected: true,
  parser_source_files: files.length,
  parser_source_lines_covered: covered,
  coverage: '/coverage/coverage.json',
};
fs.writeFileSync(path.join(outputDir, 'observed.json'), JSON.stringify(observed, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'coverage.json'), JSON.stringify(coverage, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify(summary));
