// Local bytes are strictly UTF-8 decoded and given to xmldoc's documented
// new XmlDocument(xml: string). xmldoc trims the string and writes it to a
// strict sax 1.6.1 parser created as sax.parser(true), without the xmlns
// option, and never calls close(). Element and attribute names are therefore
// the raw qualified names (prefix:local), xmlns/xmlns:* are ordinary entries in
// attr, and no namespace URI exists in the tree; the summary keeps those raw
// names and reports no URIs. The tree holds element, text, CDATA and comment
// children. Processing instructions (the XML declaration included) and text or
// comments before or after the root element are not kept, so a text run split
// only by a processing instruction becomes one segment here.
import { XmlDocument } from 'xmldoc';

export function parse(bytes) {
  const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  const document = new XmlDocument(text);
  const elements = [];
  const attributes = [];
  const segments = [];
  const comments = [];
  let pending = '';
  let cdata = 0;
  let maxDepth = 0;
  const flush = () => {
    const segment = pending.trim();
    if (segment) segments.push(segment);
    pending = '';
  };
  const walk = (element, depth) => {
    flush();
    elements.push(element.name);
    maxDepth = Math.max(maxDepth, depth);
    // attr is sax's {name: value} object; insertion order is source order.
    for (const [name, value] of Object.entries(element.attr))
      attributes.push(`${name}=${value}`);
    for (const child of element.children) {
      if (child.type === 'element') walk(child, depth + 1);
      else if (child.type === 'text') pending += child.text;
      else if (child.type === 'cdata') { cdata++; pending += child.cdata; }
      else if (child.type === 'comment') { flush(); comments.push(child.comment); }
      else throw new Error(`unexpected xmldoc node type: ${child.type}`);
    }
    flush();
  };
  walk(document, 1);
  return {
    attributes,
    cdata_sections: cdata,
    comments,
    doctype: document.doctype,
    elements,
    max_depth: maxDepth,
    root: document.name,
    text: segments,
  };
}
