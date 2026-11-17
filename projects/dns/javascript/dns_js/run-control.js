const fs = require('node:fs');
const path = require('node:path');
const { fileURLToPath } = require('node:url');
const { spawnSync } = require('node:child_process');

const SUBJECT = '/work/node_modules/dns-js/lib/';
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
const expected = {"id":43981,"qr":1,"opcode":0,"aa":0,"tc":0,"rd":1,"ra":1,"z":0,"rcode":0,"qdcount":1,"ancount":4,"nscount":0,"arcount":0,"questions":[{"name":"www.example.test.","type":1,"class":1}],"answers":[{"name":"www.example.test.","type":5,"class":1,"ttl":3600,"rdata":"example.test."},{"name":"example.test.","type":1,"class":1,"ttl":300,"rdata":"192.0.2.10"},{"name":"example.test.","type":28,"class":1,"ttl":600,"rdata":"2001:db8::10"},{"name":"example.test.","type":15,"class":1,"ttl":7200,"rdata":"10 mail.example.test."}],"authority":[],"additional":[]};
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
    if (!script.url.startsWith(`file://${SUBJECT}`)) continue;
    scripts.set(fileURLToPath(script.url), script.functions);
  }
}
const files = [];
for (const [filename, functions] of [...scripts.entries()].sort()) {
  const lines = coveredLines(fs.readFileSync(filename, 'utf8'), functions);
  if (lines.length) files.push({ filename, summary: { lines: { covered: lines.length } }, executed_lines: lines });
}
const covered = files.reduce((sum, file) => sum + file.summary.lines.covered, 0);
if (!files.some(file => file.filename === `${SUBJECT}dnspacket.js`)) throw new Error('dns-js dnspacket.js not covered');
const summary = {
  control_pass: true,
  output: observed,
  parser_source_files: files.length,
  parser_source_lines_covered: covered,
  coverage: '/coverage/coverage.json',
};
fs.writeFileSync(path.join(outputDir, 'observed.json'), JSON.stringify(observed, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'coverage.json'), JSON.stringify({ data: [{ files }] }, null, 2) + '\n');
fs.writeFileSync(path.join(outputDir, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify(summary));
