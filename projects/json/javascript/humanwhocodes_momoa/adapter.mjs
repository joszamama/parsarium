// Local bytes are decoded as strict UTF-8 text and passed to momoa parse(text),
// the documented string API, in its default "json" mode. The summary is built
// from momoa's own AST nodes, not from evaluate() or JSON.parse.
import { parse as parseJson } from '@humanwhocodes/momoa';

const decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true });

export function summarize(document) {
  const result = { objects: 0, arrays: 0, booleans: 0, nulls: 0 };
  const strings = [];
  const numbers = [];
  let depth = 0;
  const walk = (node, level) => {
    switch (node.type) {
      case 'Object':
        result.objects++;
        depth = Math.max(depth, level + 1);
        for (const member of node.members) walk(member.value, level + 1);
        break;
      case 'Array':
        result.arrays++;
        depth = Math.max(depth, level + 1);
        for (const element of node.elements) walk(element.value, level + 1);
        break;
      case 'String': strings.push(node.value); break;
      case 'Number': numbers.push(node.value); break;
      case 'Boolean': result.booleans++; break;
      case 'Null': result.nulls++; break;
      default: throw new Error(`unexpected JSON node ${node.type}`);
    }
  };
  if (document.type !== 'Document') throw new Error('expected a Document node');
  const root = document.body;
  walk(root, 0);
  result.strings = strings.sort();
  result.numbers = numbers.sort((a, b) => a - b);
  result.max_depth = depth;
  if (root.type === 'Array') {
    result.root = 'array';
    result.top_level_items = root.elements.length;
  } else if (root.type === 'Object') {
    result.root = 'object';
    result.top_level_keys = root.members.map(member => member.name.value).sort();
  } else {
    result.root = 'scalar';
  }
  return Object.fromEntries(Object.entries(result).sort(([a], [b]) => a < b ? -1 : 1));
}

export function parse(bytes) {
  // parse() rejects any token after the first value, so one call covers the
  // whole text.
  return summarize(parseJson(decoder.decode(bytes), { mode: 'json' }));
}
