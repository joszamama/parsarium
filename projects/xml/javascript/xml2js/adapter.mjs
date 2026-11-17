// Local bytes are strictly UTF-8 decoded and given to xml2js's documented
// Parser.parseStringPromise(text). xml2js drives a strict sax 1.6.1 parser
// (xmlns: true) and builds the object tree read here: $ns holds each element's
// namespace URI and local name, $ holds sax's {name, prefix, local, uri, value}
// attribute objects, and $$ keeps element and text children in document order.
// xml2js drops comments and processing instructions, so adjacent text children
// are joined; a text run split only by a comment or PI becomes one segment.
import xml2js from 'xml2js';

const TEXT = '#text';  // charkey outside XML Name syntax, so no element name collides
const OPTIONS = {
  xmlns: true,
  explicitChildren: true,
  preserveChildrenOrder: true,
  charsAsChildren: true,
  includeWhiteChars: true,
  charkey: TEXT,
};

const clark = (uri, local) => uri ? `{${uri}}${local}` : local;
const isDeclaration = name => name === 'xmlns' || name.startsWith('xmlns:');

export async function parse(bytes) {
  const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  const result = await new xml2js.Parser(OPTIONS).parseStringPromise(text);
  if (!result) throw new Error('no root element');
  const elements = [];
  const attributes = [];
  const namespaces = new Set();
  const segments = [];
  let pending = '';
  let maxDepth = 0;
  let declarations = 0;
  const flush = () => {
    const segment = pending.trim();
    if (segment) segments.push(segment);
    pending = '';
  };
  // Element entries carry $ns; text children ({'#name': '__text__'}) do not.
  const walk = (node, depth) => {
    flush();
    elements.push(clark(node.$ns.uri, node.$ns.local));
    maxDepth = Math.max(maxDepth, depth);
    for (const attribute of Object.values(node.$ ?? {})) {
      if (isDeclaration(attribute.name)) {
        declarations++;
        if (attribute.value) namespaces.add(attribute.value);
      } else {
        attributes.push(`${clark(attribute.uri, attribute.local)}=${attribute.value}`);
      }
    }
    for (const child of node.$$ ?? []) {
      if (child.$ns) walk(child, depth + 1);
      else pending += child[TEXT];
    }
    flush();
  };
  const roots = Object.values(result);
  if (roots.length !== 1 || !roots[0].$ns) throw new Error('no root element');
  walk(roots[0], 1);
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
