// Local bytes are strictly UTF-8 decoded and written to sax's documented
// strict, namespace-aware streaming parser.
import sax from 'sax';

const clark = (uri, local) => uri ? `{${uri}}${local}` : local;
const isDeclaration = name => name === 'xmlns' || name.startsWith('xmlns:');

export function parse(bytes) {
  const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  const parser = sax.parser(true, { xmlns: true, strictEntities: true });
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
  parser.onerror = error => { failure ??= error; };
  parser.ontext = chunk => { pending += chunk; };
  parser.oncdata = chunk => { pending += chunk; };
  parser.oncomment = flush;
  parser.onprocessinginstruction = flush;
  parser.onopennamespace = binding => {
    declarations++;
    if (binding.uri) namespaces.add(binding.uri);
  };
  parser.onopentag = node => {
    flush();
    elements.push(clark(node.uri, node.local));
    depth++;
    maxDepth = Math.max(maxDepth, depth);
    for (const attribute of Object.values(node.attributes)) {
      if (!isDeclaration(attribute.name)) {
        attributes.push(`${clark(attribute.uri, attribute.local)}=${attribute.value}`);
      }
    }
  };
  parser.onclosetag = () => { flush(); depth--; };
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
