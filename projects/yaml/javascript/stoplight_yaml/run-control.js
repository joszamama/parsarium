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
const expected = {"tree": ["map", [["kind", ["str", "catalog"]], ["version", ["int", "2"]], ["ratio", ["float", "0.25"]], ["offset", ["int", "-17"]], ["enabled", ["bool", true]], ["retired", ["bool", false]], ["missing", ["null"]], ["title", ["str", "Café \"quoted\"\tend"]], ["single", ["str", "it's here"]], ["tags", ["seq", [["str", "alpha"], ["str", "beta"], ["str", "gamma delta"]]]], ["point", ["map", [["lat", ["int", "1"]], ["lon", ["float", "-2.5"]]]]], ["items", ["seq", [["map", [["id", ["int", "7"]], ["name", ["str", "first item"]], ["note", ["str", "line one\nline two\n"]]]], ["map", [["id", ["int", "8"]], ["name", ["str", "Zürich"]], ["note", ["str", "folded text\n"]]]]]]], ["defaults", ["map", [["retries", ["int", "3"]], ["label", ["str", "base"]]]]], ["service", ["map", [["settings", ["map", [["retries", ["int", "3"]], ["label", ["str", "base"]]]]], ["label", ["str", "edge"]]]]]]]};
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

// Coverage groups: the package's own files, the underlying parser it delegates to and dependency source.
const OWN = "/work/node_modules/@stoplight/yaml/";
const UNDERLYING = "/work/node_modules/@stoplight/yaml-ast-parser/";
const DEPENDENCIES = ["/work/node_modules/@stoplight/ordered-object-literal/", "/work/node_modules/@stoplight/types/", "/work/node_modules/tslib/"];
const PREFIXES = [OWN, ...(UNDERLYING ? [UNDERLYING] : []), ...DEPENDENCIES];
const scripts = new Map();
for (const file of fs.readdirSync(rawDir)) {
  if (!file.startsWith('coverage-') || !file.endsWith('.json')) continue;
  const raw = JSON.parse(fs.readFileSync(path.join(rawDir, file), 'utf8'));
  for (const script of raw.result) {
    if (!script.url.startsWith('file://')) continue;
    const filename = fileURLToPath(script.url);
    if (!PREFIXES.some(prefix => filename.startsWith(prefix))) continue;
    scripts.set(filename, script.functions);
  }
}
const files = [];
for (const [filename, functions] of [...scripts.entries()].sort()) {
  const lines = coveredLines(fs.readFileSync(filename, 'utf8'), functions);
  files.push({ filename, summary: { lines: { covered: lines.length } }, executed_lines: lines });
}
const lines = list => list.reduce((sum, file) => sum + file.summary.lines.covered, 0);
const own = files.filter(file => file.filename.startsWith(OWN));
const underlying = UNDERLYING ? files.filter(file => file.filename.startsWith(UNDERLYING)) : [];
const dependency = files.filter(file => DEPENDENCIES.some(prefix => file.filename.startsWith(prefix)));
if (lines(own) === 0) throw new Error('no parser package source lines covered');
if (UNDERLYING && lines(underlying) === 0) throw new Error('no underlying parser source lines covered');
const coverage = { data: [{ files }] };
const summary = {
  control_pass: true,
  output: observed,
  parser_source_files: own.length,
  parser_source_lines_covered: lines(own),
  ...(UNDERLYING ? { underlying_source_files: underlying.length,
                     underlying_source_lines_covered: lines(underlying) } : {}),
  ...(DEPENDENCIES.length ? { dependency_source_files: dependency.length,
                              dependency_source_lines_covered: lines(dependency) } : {}),
  coverage: '/coverage/coverage.json',
};
fs.writeFileSync(path.join(outputDir, 'observed.json'), JSON.stringify(observed, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'coverage.json'), JSON.stringify(coverage, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify(summary));
