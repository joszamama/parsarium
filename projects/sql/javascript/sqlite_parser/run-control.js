'use strict';
// Replay the valid control and map V8 block coverage of the package's own files to source
// lines: per-offset counts painted from the largest to the smallest range (innermost wins),
// and a line is covered when one of its non-blank characters has a positive count.
const fs = require('node:fs');
const path = require('node:path');
const { fileURLToPath } = require('node:url');
const { spawnSync } = require('node:child_process');

const PREFIX = '/work/node_modules/sqlite-parser/lib/';
const REQUIRED = '/work/node_modules/sqlite-parser/lib/parser.js';
const outputDir = '/coverage';
const rawDir = path.join(outputDir, 'v8');
fs.mkdirSync(rawDir, { recursive: true });
const child = spawnSync(process.execPath, ['/work/replay.js', '/input/control'], {
  encoding: 'utf8', env: { ...process.env, NODE_V8_COVERAGE: rawDir },
});
if (child.status !== 0) throw new Error(`control replay failed: ${child.stderr}`);
const observed = JSON.parse(child.stdout.trim());
const expected = {"statement_count":1,"statements":[{"kind":"select","tables":["customers","orders"],"select_items":3,"joins":1,"where":true,"group_by":1,"order_by":1,"functions":["count","sum"],"literals":[["number","10"],["string","paid"]]}]};
if (JSON.stringify(observed) !== JSON.stringify(expected)) {
  throw new Error(`control mismatch: ${JSON.stringify(observed)}`);
}

const scripts = new Map();
for (const file of fs.readdirSync(rawDir)) {
  if (!file.startsWith('coverage-') || !file.endsWith('.json')) continue;
  for (const script of JSON.parse(fs.readFileSync(path.join(rawDir, file), 'utf8')).result) {
    if (!script.url.startsWith('file:')) continue;
    const filename = fileURLToPath(script.url);
    if (!filename.startsWith(PREFIX)) continue;
    if (!scripts.has(filename)) scripts.set(filename, []);
    for (const fn of script.functions) scripts.get(filename).push(...fn.ranges);
  }
}

function coveredLines(source, ranges) {
  const counts = new Int32Array(source.length).fill(-1);
  ranges.sort((a, b) => (b.endOffset - b.startOffset) - (a.endOffset - a.startOffset));
  for (const range of ranges) counts.fill(range.count, range.startOffset, Math.min(range.endOffset, source.length));
  const executed = [];
  let start = 0, lineNumber = 1;
  for (const line of source.split('\n')) {
    for (let index = 0; index < line.length; index++) {
      if (!/\s/.test(line[index]) && counts[start + index] > 0) { executed.push(lineNumber); break; }
    }
    start += line.length + 1;
    lineNumber++;
  }
  return executed;
}

const files = [];
for (const [filename, ranges] of [...scripts.entries()].sort()) {
  const lines = coveredLines(fs.readFileSync(filename, 'utf8'), ranges);
  if (lines.length) files.push({ filename, summary: { lines: { covered: lines.length } }, executed_lines: lines });
}
if (!files.some(file => file.filename === REQUIRED)) throw new Error('no generated grammar parser lines covered');
const covered = files.reduce((sum, file) => sum + file.summary.lines.covered, 0);
const summary = { control_pass: true, output: observed, parser_source_files: files.length,
                  parser_source_lines_covered: covered, coverage: '/coverage/coverage.json' };
fs.writeFileSync(path.join(outputDir, 'observed.json'), JSON.stringify(observed, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'coverage.json'), JSON.stringify({ data: [{ files }] }, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify(summary));
