// Strict UTF-8 local bytes reach the documented parse(text) CST API.
const { TextDecoder } = require('node:util');
const { project } = require('./adapter');
const utf8 = new TextDecoder('utf-8', { fatal: true });

async function parseData(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > (1 << 20))
    throw new Error('input outside harness limit');
  return project(utf8.decode(data));
}
module.exports = { parseData };
