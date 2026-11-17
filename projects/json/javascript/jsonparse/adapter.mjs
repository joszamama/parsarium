// Local bytes reach jsonparse Parser.write(Buffer), the byte-level streaming API
// shown in the package example and tests (its README documents no API).
import Parser from 'jsonparse';

export function summarize(root) {
  const result = { objects: 0, arrays: 0, booleans: 0, nulls: 0 };
  const strings = [];
  const numbers = [];
  let depth = 0;
  const walk = (value, level) => {
    if (Array.isArray(value)) {
      result.arrays++;
      depth = Math.max(depth, level + 1);
      for (const child of value) walk(child, level + 1);
    } else if (value === null) {
      result.nulls++;
    } else if (typeof value === 'object') {
      result.objects++;
      depth = Math.max(depth, level + 1);
      for (const child of Object.values(value)) walk(child, level + 1);
    } else if (typeof value === 'string') {
      strings.push(value);
    } else if (typeof value === 'number') {
      numbers.push(value);
    } else if (typeof value === 'boolean') {
      result.booleans++;
    }
  };
  walk(root, 0);
  result.strings = strings.sort();
  result.numbers = numbers.sort((a, b) => a - b);
  result.max_depth = depth;
  if (Array.isArray(root)) {
    result.root = 'array';
    result.top_level_items = root.length;
  } else if (root !== null && typeof root === 'object') {
    result.root = 'object';
    result.top_level_keys = Object.keys(root).sort();
  } else {
    result.root = 'scalar';
  }
  return Object.fromEntries(Object.entries(result).sort(([a], [b]) => a < b ? -1 : 1));
}

export function parse(bytes) {
  // jsonparse accepts a stream of concatenated values and has no end() call.
  // A root is an onValue with an empty stack; exactly one must arrive, and the
  // tokenizer must be back in START with no open container after the Buffer.
  const parser = new Parser();
  let root;
  let roots = 0;
  parser.onValue = function (value) {
    if (this.stack.length === 0) { root = value; roots++; }
  };
  parser.write(bytes);
  if (roots !== 1 || parser.stack.length !== 0 || parser.tState !== Parser.C.START)
    throw new Error('expected one complete JSON value');
  return summarize(root);
}
