const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { fileURLToPath } = require('node:url');
const { spawnSync } = require('node:child_process');

function main() {
  if (process.argv.length !== 4) process.exit(2);
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'parsarium-v8-'));
  try {
    const result = spawnSync(process.execPath,
      ['/work/afl_javascript_child.js', process.argv[2]], {
        env: { ...process.env, NODE_V8_COVERAGE: directory },
        encoding: 'utf8', timeout: 30000,
      });
    if (result.error || result.status !== 0) {
      throw new Error(`JavaScript fuzz entry failed: ${result.error || result.stderr}`);
    }
    const prefix = process.env.PARSARIUM_SUBJECT_PREFIX;
    const features = new Set();
    for (const entry of fs.readdirSync(directory)) {
      if (!entry.startsWith('coverage-') || !entry.endsWith('.json')) continue;
      const raw = JSON.parse(fs.readFileSync(path.join(directory, entry), 'utf8'));
      for (const script of raw.result) {
        if (!script.url.startsWith('file:')) continue;
        const filename = fileURLToPath(script.url);
        if (!filename.startsWith(prefix)) continue;
        for (const fn of script.functions) {
          for (const range of fn.ranges) {
            if (range.count > 0) {
              features.add(`${filename}:${range.startOffset}-${range.endOffset}`);
            }
          }
        }
      }
    }
    fs.writeFileSync(process.argv[3], [...features].sort().join('\n') + '\n');
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
}

main();
