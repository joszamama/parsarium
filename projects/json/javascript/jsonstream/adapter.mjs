// Local bytes reach the JSONStream.parse([]) through-stream API. JSONStream is a
// path filter over jsonparse: its own index.js decides what to emit, while the
// bytes are tokenized and values built by jsonparse's Parser.write.
import JSONStream from 'JSONStream';

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
  // With an empty path, JSONStream queues each completed root as one 'data'
  // event (the packaged test/test2.js; the README says empty paths emit
  // nothing). It has no end-of-input completeness check, so the adapter
  // requires exactly one root, no 'error', and 'end' after the whole Buffer.
  const stream = JSONStream.parse([]);
  const roots = [];
  let failure = null;
  let ended = false;
  stream.on('data', value => roots.push(value));
  stream.on('error', error => { failure = error; });
  stream.on('end', () => { ended = true; });
  stream.end(bytes);
  if (failure) throw failure;
  if (!ended || roots.length !== 1)
    throw new Error('expected one complete JSON value');
  return summarize(roots[0]);
}
