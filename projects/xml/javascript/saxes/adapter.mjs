// Local bytes are strictly UTF-8 decoded and written to saxes' documented
// namespace-aware SaxesParser({xmlns: true}) event stream.
import { SaxesParser } from 'saxes';

const XMLNS = 'http://www.w3.org/2000/xmlns/';
const clark = (uri, local) => uri ? `{${uri}}${local}` : local;

export function parse(bytes) {
  const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  const parser = new SaxesParser({ xmlns: true });
  const elements = [];
  const attributes = [];
  const namespaces = new Set();
  const segments = [];
  let pending = '';
  let depth = 0;
  let maxDepth = 0;
  let declarations = 0;
  let failure = null;
  const flush = () => {
    const segment = pending.trim();
    if (segment) segments.push(segment);
    pending = '';
  };
  parser.on('error', error => { failure ??= error; });
  parser.on('text', chunk => { pending += chunk; });
  parser.on('cdata', chunk => { pending += chunk; });
  parser.on('comment', flush);
  parser.on('processinginstruction', flush);
  parser.on('opentag', node => {
    flush();
    elements.push(clark(node.uri, node.local));
    depth++;
    maxDepth = Math.max(maxDepth, depth);
    for (const attribute of Object.values(node.attributes)) {
      if (attribute.uri === XMLNS) {
        declarations++;
        if (attribute.value) namespaces.add(attribute.value);
      } else {
        attributes.push(`${clark(attribute.uri, attribute.local)}=${attribute.value}`);
      }
    }
  });
  parser.on('closetag', () => { flush(); depth--; });
  parser.write(text).close();
  if (failure) throw failure;
  if (elements.length === 0) throw new Error('no root element');
  return {
    attributes,
    elements,
    max_depth: maxDepth,
    namespace_declarations: declarations,
    namespaces: [...namespaces].sort(),
    root: elements[0],
    text: segments,
  };
}
