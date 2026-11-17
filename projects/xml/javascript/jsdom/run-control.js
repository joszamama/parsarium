const fs = require('node:fs');
const path = require('node:path');
const { fileURLToPath } = require('node:url');
const { spawnSync } = require('node:child_process');

const outputDir = '/coverage';
const rawDir = path.join(outputDir, 'v8');
fs.mkdirSync(rawDir, { recursive: true });
// The summary replay reads the DOM back; coverage comes from a separate
// construction-only run so jsdom getters used by that read are not counted.
const child = spawnSync(process.execPath, ['/work/replay.js', '/input/control'], { encoding: 'utf8' });
if (child.status !== 0) {
  throw new Error(`control replay failed: ${child.stderr}`);
}
const built = spawnSync(process.execPath, ['/work/construct.js', '/input/control'], {
  encoding: 'utf8',
  env: { ...process.env, NODE_V8_COVERAGE: rawDir },
});
if (built.status !== 0) {
  throw new Error(`control construction failed: ${built.stderr}`);
}
const observed = JSON.parse(child.stdout.trim());
const expected = {"attributes": ["version=1", "id=a1", "{urn:parsarium:catalog}lang=es", "id=b2"], "elements": ["{urn:parsarium:catalog}catalog", "{urn:parsarium:item}item", "{urn:parsarium:item}item", "{urn:parsarium:item}name", "{urn:parsarium:item}note"], "max_depth": 3, "namespace_declarations": 2, "namespaces": ["urn:parsarium:catalog", "urn:parsarium:item"], "root": "{urn:parsarium:catalog}catalog", "text": ["Café & té", "Zürich <HQ>", "x < y"]};
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

// jsdom builds the DOM; saxes underneath is the XML tokenizer, counted separately.
// XML_PATH is jsdom's own XML document parser over saxes events.
const PARSER = '/work/node_modules/jsdom/';
const UNDERLYING = '/work/node_modules/saxes/';
const XML_PATH = '/work/node_modules/jsdom/lib/jsdom/browser/parser/xml.js';
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
if (covered === 0) throw new Error('no jsdom package source lines covered');
if (underlying === 0) throw new Error('no underlying saxes source lines covered');
const xmlPath = linesUnder(XML_PATH);
if (xmlPath === 0) throw new Error('no jsdom XML parser lines covered');
const coverage = { data: [{ files }] };
const summary = {
  control_pass: true,
  output: observed,
  parser_source_files: within(PARSER).length,
  parser_source_lines_covered: covered,
  xml_parser_lines_covered: xmlPath,
  underlying_source_files: within(UNDERLYING).length,
  underlying_source_lines_covered: underlying,
  coverage: '/coverage/coverage.json',
};
fs.writeFileSync(path.join(outputDir, 'observed.json'), JSON.stringify(observed, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'coverage.json'), JSON.stringify(coverage, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify(summary));
