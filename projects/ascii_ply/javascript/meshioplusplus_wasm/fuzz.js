// Emscripten's Node runtime conflicts with Jazzer.js shutdown in one process.
// Replay in a child; the separate AFL++ bridge maps this package's source ranges.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

module.exports.fuzz = function fuzz(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > (1 << 20)) return;
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'parsarium-wasm-'));
  const input = path.join(directory, 'input.ply');
  try {
    fs.writeFileSync(input, data);
    spawnSync(process.execPath, ['/work/replay.js', input], {
      timeout: 30000, stdio: 'ignore'
    });
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
};
