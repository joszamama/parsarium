// Local bytes reach bfj.parse() through a documented Readable stream.
import { Readable } from 'node:stream';
import bfj from 'bfj';

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

export async function parse(bytes) {
  // bfj.parse consumes the complete stream when ndjson is false (the default).
  // walk.js checks for trailing non-whitespace before emitting the end event.
  const value = await bfj.parse(Readable.from([bytes]), { ndjson: false });
  return summarize(value);
}
