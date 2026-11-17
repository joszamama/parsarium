import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const JSONbig = require('json-bigint');
const BigNumber = require('bignumber.js');
const decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true });

// This projection preserves the parser's value types, including BigNumber if
// a future input uses a large integer. The two pinned controls use safe Number.
function tag(value) {
  if (value === null) return { type: 'null' };
  if (BigNumber.isBigNumber(value)) return { type: 'BigNumber', decimal: value.toString() };
  if (Array.isArray(value)) return { type: 'array', items: value.map(tag) };
  switch (typeof value) {
    case 'object': return { type: 'object', members: Object.fromEntries(
      Object.keys(value).sort().map(key => [key, tag(value[key])])) };
    case 'string': return { type: 'string', value };
    case 'number': return { type: 'number', value };
    case 'boolean': return { type: 'boolean', value };
    default: throw new Error(`unexpected parsed value type ${typeof value}`);
  }
}

export function parse(bytes) {
  // No native JSON.parse participates in parsing the input text.
  let text;
  try { text = decoder.decode(bytes); }
  catch (error) {
    if (!(error instanceof TypeError)) throw error;
    const rejected = new Error('input is not valid UTF-8');
    rejected.name = 'InputDecodeError';
    throw rejected;
  }
  return tag(JSONbig.parse(text));
}
