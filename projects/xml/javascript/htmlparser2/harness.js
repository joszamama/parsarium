// Byte input reaches htmlparser2's documented callback Parser({xmlMode: true}) write/end path.
const { pathToFileURL } = require('node:url');

async function parseData(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > (1 << 20))
    throw new Error('input outside harness limit');
  const { parse } = await import(pathToFileURL('/work/adapter.mjs'));
  return parse(data);
}
module.exports = { parseData };
