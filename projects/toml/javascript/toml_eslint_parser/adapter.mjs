// Local bytes are decoded as strict UTF-8 text and passed once to
// parseTOML(text, { tomlVersion: '1.0.0' }), toml-eslint-parser's documented direct API.
// It returns an ESLint-style syntax tree whose TOMLValue nodes carry their TOML kind
// (integer with a BigInt, float, string, boolean, offset-date-time, local-date-time,
// local-date, local-time) and whose TOMLTable nodes carry the parser's resolvedKey
// (with array-of-tables indices). The typed tree is assembled by walking that syntax tree:
// table paths come from resolvedKey, key paths from getStaticTOMLValue(key), scalar values
// from the TOMLValue node. The TOML text is never re-parsed.
import { parseTOML, getStaticTOMLValue } from 'toml-eslint-parser';

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

// The parser represents every date-time kind as a JavaScript Date; local kinds are
// stored as if they were UTC, so their UTC fields are the written local fields.
function scalar(node) {
  switch (node.kind) {
    case 'string': return { type: 'string', value: node.value };
    case 'boolean': return { type: 'bool', value: String(node.value) };
    case 'integer': return { type: 'integer', value: node.bigint.toString() };
    case 'float': return { type: 'float', value: floatText(node.value) };
    case 'offset-date-time':
      return { type: 'datetime', value: trimFraction(node.value.toISOString()) };
    case 'local-date-time':
      return { type: 'datetime-local', value: trimFraction(node.value.toISOString().slice(0, -1)) };
    case 'local-date':
      return { type: 'date-local', value: node.value.toISOString().slice(0, 10) };
    case 'local-time':
      return { type: 'time-local', value: trimFraction(node.value.toISOString().slice(11, -1)) };
  }
  throw new Error(`unexpected toml-eslint-parser value kind ${node.kind}`);
}

function content(node) {
  switch (node.type) {
    case 'TOMLValue': return scalar(node);
    case 'TOMLArray': return node.elements.map(content);
    case 'TOMLInlineTable': {
      const table = {};
      for (const pair of node.body) assign(table, getStaticTOMLValue(pair.key), content(pair.value));
      return table;
    }
  }
  throw new Error(`unexpected toml-eslint-parser node ${node.type}`);
}

function isTable(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value) && !('type' in value && 'value' in value && typeof value.type === 'string');
}

// Follow a resolved path from the root, creating tables and array-of-tables entries.
function descend(root, path) {
  let table = root;
  for (let index = 0; index < path.length; index++) {
    const key = path[index];
    if (typeof key === 'number') {
      if (!Array.isArray(table)) throw new Error('array index outside an array of tables');
      table[key] ??= {};
      table = table[key];
    } else {
      const next = path[index + 1];
      if (!Object.hasOwn(table, key)) table[key] = typeof next === 'number' ? [] : {};
      table = table[key];
    }
    if (!Array.isArray(table) && !isTable(table)) throw new Error(`key path reaches a value: ${path}`);
  }
  return table;
}

function assign(table, keys, value) {
  const parent = descend(table, keys.slice(0, -1));
  const last = keys[keys.length - 1];
  if (Object.hasOwn(parent, last)) throw new Error(`key assigned twice: ${keys}`);
  parent[last] = value;
}

export function tree(program) {
  const root = {};
  const [top] = program.body;
  for (const node of top.body) {
    if (node.type === 'TOMLKeyValue') {
      assign(root, getStaticTOMLValue(node.key), content(node.value));
    } else if (node.type === 'TOMLTable') {
      const table = descend(root, node.resolvedKey);
      for (const pair of node.body) assign(table, getStaticTOMLValue(pair.key), content(pair.value));
    } else {
      throw new Error(`unexpected toml-eslint-parser node ${node.type}`);
    }
  }
  return root;
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
  return tree(parseTOML(decoder.decode(bytes), { tomlVersion: '1.0.0' }));
}
