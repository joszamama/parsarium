// Byte input is decoded locally and reaches the toml.min parse(text, { bigint: true }) path.
const { pathToFileURL } = require('node:url');

async function parseData(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > (1 << 20))
    throw new Error('input outside harness limit');
  const { decode } = await import(pathToFileURL('/work/adapter.mjs'));
  return decode(data);
}
module.exports = { parseData };
