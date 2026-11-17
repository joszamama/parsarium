'use strict';
// Local bytes reach rawsql-ts through adapter.js.
const { parse } = require('./adapter');

async function parseData(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > (1 << 20)) {
    const rejected = new Error('input outside harness limit');
    rejected.name = 'InputLimitError';
    throw rejected;
  }
  return parse(data);
}
module.exports = { parseData };
