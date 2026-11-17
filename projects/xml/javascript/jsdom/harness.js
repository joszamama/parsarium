// Byte input reaches jsdom's documented new JSDOM(text, {contentType: 'application/xml'}) path over saxes.
const { pathToFileURL } = require('node:url');

async function adapter(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > (1 << 20))
    throw new Error('input outside harness limit');
  return import(pathToFileURL('/work/adapter.mjs'));
}

// Full summary (DOM read back) for replay and the control check.
async function parseData(data) {
  return (await adapter(data)).parse(data);
}

// Document construction only, without walking the tree: the fuzz and AFL++
// feedback entry, so harness traversal does not add jsdom getter coverage.
async function constructData(data) {
  (await adapter(data)).construct(data).window.close();
}
module.exports = { parseData, constructData };
