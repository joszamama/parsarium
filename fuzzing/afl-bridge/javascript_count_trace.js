// Opt-in JavaScript AFL++ feedback for parser functions whose input-dependent
// frame walks execute the same source ranges a different number of times.
// Module-load ranges and all functions outside the explicit allowlist are out.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { fileURLToPath } = require('node:url');
const { spawnSync } = require('node:child_process');

function collect(raw, prefix, names) {
  const features = new Set();
  for (const script of raw.result) {
    if (!script.url.startsWith('file:')) continue;
    const filename = fileURLToPath(script.url);
    if (!filename.startsWith(prefix)) continue;
    for (const fn of script.functions) {
      if (!names.has(fn.functionName)) continue;
      for (const range of fn.ranges) {
        if (range.count > 0) {
          // Exact small counts distinguish 11 and 12 parsed frames. Saturation
          // bounds the feedback alphabet on longer inputs. These are execution
          // counts, not newly covered branches or source lines.
          const count = Math.min(range.count, 255);
          features.add(`${filename}:${fn.functionName}:${range.startOffset}-${range.endOffset}:hits=${count}`);
        }
      }
    }
  }
  return features;
}

function main() {
  if (process.argv.length !== 4) process.exit(2);
  const prefix = process.env.PARSARIUM_SUBJECT_PREFIX;
  const names = new Set((process.env.PARSARIUM_JS_COUNT_FUNCTIONS || '').split(',').filter(Boolean));
  if (!prefix || names.size === 0) throw new Error('count trace requires a source prefix and function allowlist');
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'parsarium-v8-'));
  try {
    const result = spawnSync(process.execPath,
      ['/work/afl_javascript_child.js', process.argv[2]], {
        env: { ...process.env, NODE_V8_COVERAGE: directory },
        encoding: 'utf8', timeout: 30000,
      });
    if (result.error || result.status !== 0)
      throw new Error(`JavaScript fuzz entry failed: ${result.error || result.stderr}`);
    const features = new Set();
    for (const entry of fs.readdirSync(directory)) {
      if (!entry.startsWith('coverage-') || !entry.endsWith('.json')) continue;
      const raw = JSON.parse(fs.readFileSync(path.join(directory, entry), 'utf8'));
      for (const feature of collect(raw, prefix, names)) features.add(feature);
    }
    fs.writeFileSync(process.argv[3], [...features].sort().join('\n') + '\n');
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
}

if (require.main === module) main();
module.exports = { collect };
