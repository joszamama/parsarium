// Local bytes are strictly UTF-8 decoded and passed to xmldom's documented
// DOMParser.parseFromString(text, 'application/xml'); every reported warning,
// error or fatal error stops parsing. The summary reads the package DOM's own
// namespaceURI/localName resolution.
import xmldom from '@xmldom/xmldom';

const { DOMParser, NAMESPACE } = xmldom;
const ELEMENT = 1, TEXT = 3, CDATA = 4, PI = 7, COMMENT = 8;
const clark = (uri, local) => uri ? `{${uri}}${local}` : local;

export function parse(bytes) {
  const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  const parser = new DOMParser({
    onError(level, message) { throw new Error(`xmldom ${level}: ${message}`); },
  });
  const document = parser.parseFromString(text, 'application/xml');
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
  const visit = (node, depth) => {
    for (let child = node.firstChild; child; child = child.nextSibling) {
      if (child.nodeType === TEXT || child.nodeType === CDATA) {
        pending += child.data;
      } else if (child.nodeType === COMMENT || child.nodeType === PI) {
        flush();
      } else if (child.nodeType === ELEMENT) {
        flush();
        elements.push(clark(child.namespaceURI, child.localName));
        maxDepth = Math.max(maxDepth, depth + 1);
        for (let i = 0; i < child.attributes.length; i++) {
          const attribute = child.attributes.item(i);
          if (attribute.namespaceURI === NAMESPACE.XMLNS) {
            declarations++;
            if (attribute.value) namespaces.add(attribute.value);
          } else {
            attributes.push(`${clark(attribute.namespaceURI, attribute.localName)}=${attribute.value}`);
          }
        }
        visit(child, depth + 1);
        flush();
      }
    }
  };
  visit(document, 0);
  if (!document.documentElement) throw new Error('no root element');
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
