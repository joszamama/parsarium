// Local UTF-8 bytes reach the documented streaming JSONParser.write API.
import { JSONParser } from '@streamparser/json';

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
  // The default undefined separator ends parsing after one complete document.
  // The root callback is identified by its empty stack.
  const parser = new JSONParser({ keepStack: true });
  let root;
  let roots = 0;
  parser.onValue = ({ value, stack }) => {
    if (stack.length === 0) { root = value; roots++; }
  };
  parser.write(bytes);
  if (!parser.isEnded) parser.end();
  if (!parser.isEnded || roots !== 1) throw new Error('expected one complete JSON value');
  return summarize(root);
}
