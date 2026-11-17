// Byte input reaches the documented stream-json parser() and Assembler path.
const { pathToFileURL } = require('node:url');

async function parseData(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > (1 << 20))
    throw new Error('input outside harness limit');
  const { parse } = await import(pathToFileURL('/work/adapter.mjs'));
  return await parse(data);
}
module.exports = { parseData };
