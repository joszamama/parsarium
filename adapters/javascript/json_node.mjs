// Standard Node.js path: local bytes -> strict UTF-8 TextDecoder -> JSON.parse(string).
// JSON.parse accepts only a string, so byte decoding is this adapter's step, not the parser's.
import { readFile } from 'node:fs/promises';

function summarize(root) {
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

const [path] = process.argv.slice(2);
if (!path) throw new Error('usage: node json_node.mjs CONTROL');
const bytes = await readFile(path);
const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
console.log(JSON.stringify(summarize(JSON.parse(text))));
