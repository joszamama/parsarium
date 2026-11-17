'use strict';
// Replay the valid control and map V8 block coverage of the minified PostgreSQL parser
// bundle back to its own sources (the PEG.js-generated parser and src/*.js) through the
// source map shipped in the pinned package.
const fs = require('node:fs');
const path = require('node:path');
const { fileURLToPath } = require('node:url');
const { spawnSync } = require('node:child_process');

const BUNDLE = '/work/node_modules/node-sql-parser/build/postgresql.js';
const SOURCE_ROOT = '/home/runner/work/node-sql-parser/node-sql-parser/';
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

// Per-offset block counts: paint ranges from largest to smallest so the innermost wins.
const bundle = fs.readFileSync(BUNDLE, 'utf8');
const counts = new Int32Array(bundle.length).fill(-1);
const ranges = [];
for (const file of fs.readdirSync(rawDir)) {
  if (!file.startsWith('coverage-') || !file.endsWith('.json')) continue;
  for (const script of JSON.parse(fs.readFileSync(path.join(rawDir, file), 'utf8')).result) {
    if (!script.url.startsWith('file:') || fileURLToPath(script.url) !== BUNDLE) continue;
    for (const fn of script.functions) ranges.push(...fn.ranges);
  }
}
if (!ranges.length) throw new Error('no V8 coverage for the parser bundle');
ranges.sort((a, b) => (b.endOffset - b.startOffset) - (a.endOffset - a.startOffset));
for (const range of ranges) counts.fill(range.count, range.startOffset, Math.min(range.endOffset, bundle.length));

// Minimal Base64 VLQ decoder for the source map's mappings.
const BASE64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
function decodeSegment(text) {
  const values = [];
  let value = 0, shift = 0;
  for (const char of text) {
    const digit = BASE64.indexOf(char);
    if (digit < 0) throw new Error('bad VLQ digit');
    value += (digit & 31) << shift;
    if (digit & 32) { shift += 5; continue; }
    values.push(value & 1 ? -(value >>> 1) : value >>> 1);
    value = 0; shift = 0;
  }
  return values;
}
const map = JSON.parse(fs.readFileSync(`${BUNDLE}.map`, 'utf8'));
const generatedLines = bundle.split('\n');
const lineStarts = [];
let offset = 0;
for (const line of generatedLines) { lineStarts.push(offset); offset += line.length + 1; }
const covered = new Map();
let source = 0, originalLine = 0, originalColumn = 0;
map.mappings.split(';').forEach((group, generatedLine) => {
  let generatedColumn = 0;
  for (const segment of group.split(',')) {
    if (!segment) continue;
    const fields = decodeSegment(segment);
    generatedColumn += fields[0];
    if (fields.length < 4) continue;
    source += fields[1]; originalLine += fields[2]; originalColumn += fields[3];
    const name = map.sources[source];
    if (!name.startsWith(SOURCE_ROOT)) continue;
    const relative = name.slice(SOURCE_ROOT.length);
    if (!(relative.startsWith('pegjs/') || relative.startsWith('src/'))) continue;
    const at = lineStarts[generatedLine] + generatedColumn;
    if (counts[at] > 0) {
      if (!covered.has(relative)) covered.set(relative, new Set());
      covered.get(relative).add(originalLine + 1);
    }
  }
});
const files = [...covered.entries()].sort().map(([relative, lines]) => {
  const executed = [...lines].sort((a, b) => a - b);
  return { filename: `${BUNDLE}!${relative}`, summary: { lines: { covered: executed.length } },
           executed_lines: executed };
});
const total = files.reduce((sum, file) => sum + file.summary.lines.covered, 0);
if (!files.some(file => file.filename.endsWith('!pegjs/postgresql.pegjs'))) {
  throw new Error('no generated PostgreSQL grammar parser lines covered');
}
const summary = { control_pass: true, output: observed, parser_source_files: files.length,
                  parser_source_lines_covered: total, coverage: '/coverage/coverage.json' };
fs.writeFileSync(path.join(outputDir, 'observed.json'), JSON.stringify(observed, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'coverage.json'), JSON.stringify({ data: [{ files }] }, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify(summary));
