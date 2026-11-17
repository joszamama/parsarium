// Byte input is decoded locally and reaches lossless-json's parse(text) path.
const { pathToFileURL } = require('node:url');

async function parseData(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > (1 << 20)) {
    const rejected = new Error('input outside harness limit');
    rejected.name = 'InputLimitError';
    throw rejected;
  }
  const { parse } = await import(pathToFileURL('/work/adapter.mjs'));
  return parse(data);
}
module.exports = { parseData };
