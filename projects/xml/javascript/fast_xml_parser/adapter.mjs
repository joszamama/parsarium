// Local bytes go as a Buffer to fast-xml-parser's documented XMLParser.parse(data, true):
// its own validator scans the document, then OrderedObjParser builds the preserveOrder tree.
// fast-xml-parser keeps qualified names and does no namespace processing; the adapter
// resolves prefixes from in-scope xmlns attributes (Namespaces in XML 1.0) and rejects
// unbound prefixes and duplicate expanded attributes.
import { XMLParser } from 'fast-xml-parser';

const XML_NAMESPACE = 'http://www.w3.org/XML/1998/namespace';
const PREFIX = '@_';
const COMMENT = '#comment';
const TEXT = '#text';
const OPTIONS = {
  preserveOrder: true,
  ignoreAttributes: false,
  attributeNamePrefix: PREFIX,
  commentPropName: COMMENT,
  textNodeName: TEXT,
  trimValues: false,
  parseTagValue: false,
  parseAttributeValue: false,
  // Numeric character references are decoded only with htmlEntities (docs 5.Entities.md).
  htmlEntities: true,
};

const clark = (uri, local) => uri ? `{${uri}}${local}` : local;

function expand(qname, scope, isAttribute) {
  const colon = qname.indexOf(':');
  if (colon === -1) return isAttribute ? qname : clark(scope.get(''), qname);
  const prefix = qname.slice(0, colon);
  const local = qname.slice(colon + 1);
  if (!prefix || !local || local.includes(':')) throw new Error(`bad qualified name: ${qname}`);
  const uri = prefix === 'xml' ? XML_NAMESPACE : scope.get(prefix);
  if (!uri) throw new Error(`unbound prefix: ${prefix}`);
  return clark(uri, local);
}

export function parse(bytes) {
  const tree = new XMLParser(OPTIONS).parse(bytes, true);
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
  const walk = (nodes, parentScope, depth) => {
    for (const node of nodes) {
      const name = Object.keys(node).find(key => key !== ':@');
      if (name === TEXT) { pending += node[TEXT]; continue; }
      flush();
      if (name === COMMENT || name.startsWith('?')) continue;
      const scope = new Map(parentScope);
      const raw = Object.entries(node[':@'] ?? {})
        .map(([key, value]) => [key.slice(PREFIX.length), String(value)]);
      for (const [qname, value] of raw) {
        if (qname === 'xmlns') {
          scope.set('', value);  // empty value resets the default namespace
        } else if (qname.startsWith('xmlns:')) {
          if (!value) throw new Error(`empty prefix binding: ${qname}`);
          scope.set(qname.slice(6), value);
        } else {
          continue;
        }
        declarations++;
        if (value) namespaces.add(value);
      }
      elements.push(expand(name, scope, false));
      maxDepth = Math.max(maxDepth, depth);
      const seen = new Set();
      for (const [qname, value] of raw) {
        if (qname === 'xmlns' || qname.startsWith('xmlns:')) continue;
        const expanded = expand(qname, scope, true);
        if (seen.has(expanded)) throw new Error(`duplicate attribute: ${expanded}`);
        seen.add(expanded);
        attributes.push(`${expanded}=${value}`);
      }
      walk(node[name], scope, depth + 1);
      flush();
    }
  };
  walk(tree, new Map(), 1);
  // fast-xml-parser can return a tree without an element and no error; the result then lists no
  // elements and its root is null.
  return {
    attributes,
    elements,
    max_depth: maxDepth,
    namespace_declarations: declarations,
    namespaces: [...namespaces].sort(),
    root: elements.length ? elements[0] : null,
    text: segments,
  };
}
