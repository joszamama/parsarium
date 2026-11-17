import { isLosslessNumber, parse as parseJSON } from 'lossless-json';

const decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true });

function tag(value) {
  if (value === null) return { type: 'null' };
  if (isLosslessNumber(value)) return { type: 'LosslessNumber', raw: value.value };
  if (Array.isArray(value)) return { type: 'array', items: value.map(tag) };
  switch (typeof value) {
    case 'object': return { type: 'object', members: Object.fromEntries(
      Object.keys(value).sort().map(key => [key, tag(value[key])])) };
    case 'string': return { type: 'string', value };
    case 'boolean': return { type: 'boolean', value };
    case 'number': return { type: 'number', value };
    default: throw new Error(`unexpected parsed value type ${typeof value}`);
  }
}

export function parse(bytes) {
  let text;
  try { text = decoder.decode(bytes); }
  catch (error) {
    if (!(error instanceof TypeError)) throw error;
    const rejected = new Error('input is not valid UTF-8');
    rejected.name = 'InputDecodeError';
    throw rejected;
  }
  return tag(parseJSON(text));
}
