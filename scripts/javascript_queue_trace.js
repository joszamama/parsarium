// Replay one saved local input through the project's verified Node harness.
// NODE_V8_COVERAGE belongs only to the child process that calls the parser.
const fs = require('node:fs');
const path = require('node:path');
const { fileURLToPath } = require('node:url');
const { spawnSync } = require('node:child_process');

const [casePath, outputPath, prefixesText] = process.argv.slice(2);
const prefixes = JSON.parse(prefixesText);
if (!Array.isArray(prefixes) || prefixes.length === 0 ||
    prefixes.some(prefix => typeof prefix !== 'string' || !prefix.startsWith('/')))
  throw new Error('expected absolute parser source prefixes');

const rawDir = path.join(path.dirname(outputPath), `v8-${path.basename(outputPath, '.json')}`);
fs.mkdirSync(rawDir, { recursive: true });
const child = spawnSync(process.execPath, ['/work/replay.js', casePath], {
  stdio: 'ignore',
  env: { ...process.env, NODE_V8_COVERAGE: rawDir },
});
const outcome = child.error ? `exception:${child.error.name}` :
  child.status === 0 ? 'ok' : `exception:ReplayExit${child.status ?? 'Signal'}`;

// Match the project's valid-control V8 line mapping: a line is observed when
// any non-whitespace character belongs to the smallest executed range.
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
    if (!script.url.startsWith('file://')) continue;
    const filename = fileURLToPath(script.url);
    if (!prefixes.some(prefix => filename.startsWith(prefix))) continue;
    scripts.set(filename, [...(scripts.get(filename) || []), ...script.functions]);
  }
}
const files = [];
for (const [filename, functions] of [...scripts.entries()].sort()) {
  const lines = coveredLines(fs.readFileSync(filename, 'utf8'), functions);
  if (lines.length > 0) files.push({ filename, executed_lines: lines });
}
fs.writeFileSync(outputPath, JSON.stringify({ outcome, files }) + '\n');
fs.rmSync(rawDir, { recursive: true, force: true });
