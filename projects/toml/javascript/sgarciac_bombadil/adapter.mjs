// Local bytes are decoded as strict UTF-8 text and passed once to
// new TomlReader().readToml(text, true), bombadil's documented reader with its documented
// "full typing information" flag. The reader lexes and parses the document with its own
// chevrotain grammar and loads the tables; on failure result is undefined and errors holds
// the lexer, parser or table-loading errors. With the flag, every table is
// { type: 'table', content } and every primitive is { type, image, value } with type
// atomicString, atomicInteger, atomicFloat, atomicBoolean, offsetDateTime, localDateTime,
// localDate or localTime; arrays are JavaScript arrays. The typed tree is built from those
// types and values only (never from image); the TOML text is never re-parsed.
import { createRequire } from 'node:module';

const { TomlReader } = createRequire(import.meta.url)('@sgarciac/bombadil');
const decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true });

// Drop trailing zeros of a fractional-seconds part, and the dot when nothing is left.
function trimFraction(text) {
  return text.replace(/\.(\d*?)0+(?=Z?$)/, (_, digits) => digits ? `.${digits}` : '');
}

// Shortest round-trip digits (Number.prototype.toString) written positionally with at
// least one fractional digit: 1e3 -> 1000.0, 1.5625e-2 -> 0.015625.
export function floatText(value) {
  if (Number.isNaN(value)) return 'nan';
  if (!Number.isFinite(value)) return value > 0 ? 'inf' : '-inf';
  const negative = value < 0 || Object.is(value, -0);
  const [mantissa, exponent = '0'] = Math.abs(value).toString().split('e');
  const dot = mantissa.indexOf('.');
  let digits = mantissa.replace('.', '');
  let point = (dot < 0 ? mantissa.length : dot) + Number(exponent);
  while (digits.length > 1 && digits[0] === '0') {
    digits = digits.slice(1);
    point--;
  }
  let text;
  if (point <= 0) text = `0.${'0'.repeat(-point)}${digits}`;
  else if (point >= digits.length) text = `${digits}${'0'.repeat(point - digits.length)}.0`;
  else text = `${digits.slice(0, point)}.${digits.slice(point)}`;
  return (negative ? '-' : '') + text;
}

// bombadil returns every date-time kind as a JavaScript Date (README "Type mapping"):
// the offset date-time Date is the instant; local kinds are stored with UTC±00:00, so their
// UTC fields are the written local fields (millisecond precision).
function integerText(value) {
  if (!Number.isSafeInteger(value)) throw new Error(`integer outside the exact Number range: ${value}`);
  return String(value);
}

function scalar(node) {
  switch (node.type) {
    case 'atomicString': return { type: 'string', value: node.value };
    case 'atomicBoolean': return { type: 'bool', value: String(node.value) };
    case 'atomicInteger': return { type: 'integer', value: integerText(node.value) };
    case 'atomicFloat': return { type: 'float', value: floatText(node.value) };
    case 'offsetDateTime': return { type: 'datetime', value: trimFraction(node.value.toISOString()) };
    case 'localDateTime': return { type: 'datetime-local', value: trimFraction(node.value.toISOString().slice(0, -1)) };
    case 'localDate': return { type: 'date-local', value: node.value.toISOString().slice(0, 10) };
    case 'localTime': return { type: 'time-local', value: trimFraction(node.value.toISOString().slice(11, -1)) };
  }
  throw new Error(`unexpected bombadil value type ${node.type}`);
}

export function tree(node) {
  if (Array.isArray(node)) return node.map(tree);
  if (node.type === 'table') {
    return Object.fromEntries(Object.keys(node.content).map(key => [key, tree(node.content[key])]));
  }
  return scalar(node);
}

// Canonical JSON with sorted object keys, so key order is not significant.
export function canonical(node) {
  if (Array.isArray(node)) return `[${node.map(canonical).join(',')}]`;
  if (node !== null && typeof node === 'object') {
    return `{${Object.keys(node).sort().map(key => `${JSON.stringify(key)}:${canonical(node[key])}`).join(',')}}`;
  }
  return JSON.stringify(node);
}

export function decode(bytes) {
  const reader = new TomlReader();
  reader.readToml(decoder.decode(bytes), true);
  if (reader.result === undefined || reader.errors.length) {
    throw new Error(`bombadil rejected the document (${reader.errors.length} errors)`);
  }
  return tree(reader.result);
}
