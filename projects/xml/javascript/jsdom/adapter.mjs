// Local bytes are strictly UTF-8 decoded and given to jsdom's documented
// new JSDOM(text, {contentType: 'application/xml'}). jsdom's XML document
// parser (lib/jsdom/browser/parser/xml.js) drives saxes 6.0.0 with
// {xmlns: true, forceXMLVersion: true} and builds the DOM from its events; a
// saxes error becomes a thrown SyntaxError and any reported jsdomError is
// fatal here. construct() only builds the document; parse() then reads the
// DOM's own namespaceURI/localName resolution, attribute order and text nodes.
import { JSDOM, VirtualConsole } from 'jsdom';

const XMLNS = 'http://www.w3.org/2000/xmlns/';
const ELEMENT = 1, TEXT = 3, CDATA = 4, PI = 7, COMMENT = 8;
const clark = (uri, local) => uri ? `{${uri}}${local}` : local;

export function construct(bytes) {
  const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  const reported = [];
  const virtualConsole = new VirtualConsole();
  virtualConsole.on('jsdomError', error => reported.push(error));
  let dom;
  try {
    dom = new JSDOM(text, { contentType: 'application/xml', virtualConsole });
  } catch (error) {
    // jsdom's DOMException comes from the window realm, so rewrap it as a local Error.
    throw new Error(`jsdom: ${error?.name}: ${error?.message}`);
  }
  if (reported.length) {
    dom.window.close();
    throw new Error(`jsdom: ${reported[0].message}`);
  }
  return dom;
}

export function parse(bytes) {
  const dom = construct(bytes);
  const document = dom.window.document;
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
        for (const attribute of child.attributes) {
          if (attribute.namespaceURI === XMLNS) {
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
  const hasRoot = document.documentElement !== null;
  dom.window.close();
  if (!hasRoot) throw new Error('no root element');
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
