const fs = require('node:fs');
const path = require('node:path');
const { fileURLToPath } = require('node:url');
const { spawnSync } = require('node:child_process');

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
const observed = JSON.parse(child.stdout.trim());
const expected = {"type":"object","members":{"enabled":{"type":"boolean","value":true},"missing":{"type":"null"},"name":{"type":"string","value":"parsarium"},"nested":{"type":"object","members":{"empty":{"type":"object","members":{}},"items":{"type":"array","items":[{"type":"object","members":{"id":{"type":"number","value":1},"ok":{"type":"boolean","value":false}}},{"type":"object","members":{"id":{"type":"number","value":2},"text":{"type":"string","value":"café \"quoted\""}}}]},"level":{"type":"number","value":2},"list":{"type":"array","items":[]}}},"ratio":{"type":"number","value":-2.5},"tags":{"type":"array","items":[{"type":"string","value":"json"},{"type":"string","value":"go"},{"type":"string","value":"rfc8259"}]},"version":{"type":"number","value":1}}};
if (JSON.stringify(observed) !== JSON.stringify(expected)) {
  throw new Error(`control mismatch: ${JSON.stringify(observed)}`);
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
    if (!new Set([
      'file:///work/node_modules/jsonc-parser/lib/umd/impl/parser.js',
      'file:///work/node_modules/jsonc-parser/lib/umd/impl/scanner.js',
    ]).has(script.url)) continue;
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
  output: observed,
  parser_source_files: files.length,
  parser_source_lines_covered: covered,
  coverage: '/coverage/coverage.json',
};
fs.writeFileSync(path.join(outputDir, 'observed.json'), JSON.stringify(observed, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'coverage.json'), JSON.stringify(coverage, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify(summary));
