const { unzipSync } = require('fflate');

function parseZip(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > (1 << 20)) {
    throw new Error('input size outside harness limit');
  }
  const files = unzipSync(data, { filter: info => info.originalSize <= (1 << 20) });
  // unzipSync fills the object in central-directory order; keep that order.
  const entries = Object.keys(files);
  if (entries.length === 0) return { entries, content: '' };
  return {
    entries,
    content: Buffer.from(files[entries[0]]).toString('utf8'),
  };
}

module.exports = { parseZip };
