"use strict";
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { spawnSync } = require("node:child_process");

const rawDirectory = fs.mkdtempSync(path.join(os.tmpdir(), "parsarium-v8-"));
const child = spawnSync(process.execPath, ["/work/replay.js", "/input/control"], {
  encoding: "utf8", env: { ...process.env, NODE_V8_COVERAGE: rawDirectory },
});
if (child.status !== 0) throw new Error(`request replay failed: ${child.stderr}`);
const observed = JSON.parse(child.stdout.trim());
const expected = { method: "GET", target: "/parsarium?x=1" };
if (JSON.stringify(observed) !== JSON.stringify(expected))
  throw new Error(`control mismatch: ${JSON.stringify(observed)}`);

function coveredLines(source, functions) {
  const lines = [];
  let offset = 0;
  let number = 1;
  for (const line of source.split("\n")) {
    const position = line.search(/\S/);
    if (position >= 0) {
      const index = offset + position;
      let smallest = Infinity;
      let count = 0;
      for (const fn of functions) for (const range of fn.ranges) {
        const width = range.endOffset - range.startOffset;
        if (range.startOffset <= index && index < range.endOffset && width < smallest) {
          smallest = width;
          count = range.count;
        }
      }
      if (count > 0) lines.push(number);
    }
    offset += line.length + 1;
    number++;
  }
  return lines;
}

const natives = process.binding("natives");
const scripts = new Map();
for (const file of fs.readdirSync(rawDirectory)) {
  if (!file.startsWith("coverage-") || !file.endsWith(".json")) continue;
  const raw = JSON.parse(fs.readFileSync(path.join(rawDirectory, file), "utf8"));
  for (const script of raw.result)
    if (script.url.startsWith("node:_http_")) scripts.set(script.url, script.functions);
}
const files = [];
for (const [filename, functions] of [...scripts].sort()) {
  const source = natives[filename.slice(5)];
  if (typeof source !== "string") throw new Error(`missing bundled source ${filename}`);
  const lines = coveredLines(source, functions);
  if (lines.length) files.push({ filename, summary: { lines: { covered: lines.length } }, executed_lines: lines });
}
if (!files.some(file => file.filename === "node:_http_common" && file.summary.lines.covered > 0))
  throw new Error("Node's HTTP/1.1 source was not covered");
const summary = { control_pass: true, output: observed,
  parser_source_files: files.length,
  parser_source_lines_covered: files.reduce((sum, file) => sum + file.summary.lines.covered, 0),
  coverage: "/coverage/coverage.json" };
fs.writeFileSync("/coverage/observed.json", JSON.stringify(observed, null, 2) + "\n");
fs.writeFileSync("/coverage/coverage.json", JSON.stringify({ data: [{ files }] }, null, 2) + "\n");
fs.writeFileSync("/coverage/summary.json", JSON.stringify(summary) + "\n");
console.log(JSON.stringify(summary));
