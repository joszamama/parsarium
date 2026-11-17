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
const expected = {"attributes": ["xmlns:c=urn:parsarium:catalog", "xmlns=urn:parsarium:item", "version=1", "id=a1", "c:lang=es", "id=b2"], "cdata_sections": 1, "comments": [], "elements": ["c:catalog", "item", "item", "name", "note"], "max_depth": 3, "processing_instructions": ["xml version=\"1.0\" encoding=\"UTF-8\""], "root": "c:catalog", "text": ["Café & té", "Zürich <HQ>", "x < y"]};
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

// htmlparser2's own Parser and Tokenizer are the parser package; the
// entities decode trees it calls for character references are counted
// separately. index.js also loads domhandler/domutils, which this callback
// path never calls, so they are outside both prefixes.
const PARSER = '/work/node_modules/htmlparser2/';
const UNDERLYING = '/work/node_modules/entities/';
const PREFIXES = [PARSER, UNDERLYING];
const scripts = new Map();
for (const file of fs.readdirSync(rawDir)) {
  if (!file.startsWith('coverage-') || !file.endsWith('.json')) continue;
  const raw = JSON.parse(fs.readFileSync(path.join(rawDir, file), 'utf8'));
  for (const script of raw.result) {
    if (!PREFIXES.some(prefix => script.url.startsWith(`file://${prefix}`))) continue;
    scripts.set(fileURLToPath(script.url), script.functions);
  }
}
const files = [];
for (const [filename, functions] of [...scripts.entries()].sort()) {
  const lines = coveredLines(fs.readFileSync(filename, 'utf8'), functions);
  files.push({ filename, summary: { lines: { covered: lines.length } }, executed_lines: lines });
}
const within = prefix => files.filter(file => file.filename.startsWith(prefix));
const linesUnder = prefix => within(prefix).reduce((sum, file) => sum + file.summary.lines.covered, 0);
const covered = linesUnder(PARSER);
const underlying = linesUnder(UNDERLYING);
if (covered === 0) throw new Error('no htmlparser2 source lines covered');
if (underlying === 0) throw new Error('no underlying entities source lines covered');
const perFile = Object.fromEntries(files.map(file => [file.filename, file.summary.lines.covered]));
for (const name of ['Parser.js', 'Tokenizer.js']) {
  if (!perFile[`${PARSER}dist/${name}`]) throw new Error(`no htmlparser2 ${name} lines covered`);
}
const coverage = { data: [{ files }] };
const summary = {
  control_pass: true,
  output: observed,
  parser_source_files: within(PARSER).length,
  parser_source_lines_covered: covered,
  underlying_source_files: within(UNDERLYING).length,
  underlying_source_lines_covered: underlying,
  lines_covered_by_file: perFile,
  coverage: '/coverage/coverage.json',
};
fs.writeFileSync(path.join(outputDir, 'observed.json'), JSON.stringify(observed, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'coverage.json'), JSON.stringify(coverage, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify(summary));
