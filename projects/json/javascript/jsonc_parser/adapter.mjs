import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { parseTree } = require('jsonc-parser');
const decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true });
const STRICT_JSON = { disallowComments: true, allowTrailingComma: false,
                      allowEmptyContent: false };

function tag(node) {
  if (node.type === 'array')
    return { type: 'array', items: node.children.map(tag) };
  if (node.type === 'object') {
    const entries = [];
    const seen = new Set();
    for (const property of node.children) {
      if (property.type !== 'property' || property.children?.length !== 2 ||
          property.children[0].type !== 'string')
        throw new Error('incomplete property in parsed AST');
      const name = property.children[0].value;
      if (seen.has(name)) {
        const rejected = new Error('duplicate key in JSON control');
        rejected.name = 'ParseRejectedError';
        throw rejected;
      }
      seen.add(name);
      entries.push([name, tag(property.children[1])]);
    }
    entries.sort(([a], [b]) => a.localeCompare(b));
    return { type: 'object', members: Object.fromEntries(entries) };
  }
  if (['string', 'number', 'boolean'].includes(node.type))
    return { type: node.type, value: node.value };
  if (node.type === 'null') return { type: 'null' };
  throw new Error(`unexpected JSONC AST node ${node.type}`);
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
  const errors = [];
  const root = parseTree(text, errors, STRICT_JSON);
  if (root === undefined || errors.length !== 0) {
    const rejected = new Error(`JSONC parser rejected input (${errors.length} errors)`);
    rejected.name = 'ParseRejectedError';
    throw rejected;
  }
  return tag(root);
}
