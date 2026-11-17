// Local bytes are decoded as strict UTF-8 text and passed once to JSON5.parse(text),
// the documented string API. JSON5 is a superset of JSON, so this path accepts
// JSON5-only syntax as well; it is not a strict RFC 8259 validator. The tree and
// summary are built from the value JSON5.parse returns, with no fallback parser.
import JSON5 from 'json5';

const decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true });
const float64 = new DataView(new ArrayBuffer(8));

// Numbers are tagged by their IEEE 754 double bits, so -0 and every rounding
// difference stay visible. Object members keep Object.keys order.
export function tree(value) {
  if (value === null) return { type: 'null' };
  if (Array.isArray(value)) return { type: 'array', items: value.map(tree) };
  switch (typeof value) {
    case 'boolean': return { type: 'boolean', value };
    case 'string': return { type: 'string', value };
    case 'number':
      float64.setFloat64(0, value);
      return { type: 'number', float64: float64.getBigUint64(0).toString(16).padStart(16, '0') };
    case 'object':
      if (Object.getPrototypeOf(value) !== Object.prototype) break;
      return { type: 'object', members: Object.keys(value).map(key => [key, tree(value[key])]) };
  }
  throw new Error(`unexpected JSON5 value ${Object.prototype.toString.call(value)}`);
}

export function summarize(root) {
  const result = { objects: 0, arrays: 0, booleans: 0, nulls: 0 };
  const strings = [];
  const numbers = [];
  let depth = 0;
  const walk = (node, level) => {
    switch (node.type) {
      case 'object':
        result.objects++;
        depth = Math.max(depth, level + 1);
        for (const [, member] of node.members) walk(member, level + 1);
        break;
      case 'array':
        result.arrays++;
        depth = Math.max(depth, level + 1);
        for (const item of node.items) walk(item, level + 1);
        break;
      case 'string': strings.push(node.value); break;
      case 'number':
        float64.setBigUint64(0, BigInt(`0x${node.float64}`));
        numbers.push(float64.getFloat64(0));
        break;
      case 'boolean': result.booleans++; break;
      case 'null': result.nulls++; break;
    }
  };
  walk(root, 0);
  result.strings = strings.sort();
  result.numbers = numbers.sort((a, b) => a - b);
  result.max_depth = depth;
  if (root.type === 'array') {
    result.root = 'array';
    result.top_level_items = root.items.length;
  } else if (root.type === 'object') {
    result.root = 'object';
    result.top_level_keys = root.members.map(([key]) => key).sort();
  } else {
    result.root = 'scalar';
  }
  return Object.fromEntries(Object.entries(result).sort(([a], [b]) => a < b ? -1 : 1));
}

export function decode(bytes) {
  // JSON5.parse lexes to end of input and rejects any token after the first value.
  const value = tree(JSON5.parse(decoder.decode(bytes)));
  return { summary: summarize(value), tree: value };
}

export function parse(bytes) {
  return decode(bytes).summary;
}
