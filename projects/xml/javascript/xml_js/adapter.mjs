import xmljs from 'xml-js';

// xml-js preserves qualified names and ordered SAX events, but does not expand
// namespace URIs. Resolve them from in-scope xmlns attributes here.
const clark = (uri, local) => uri ? `{${uri}}${local}` : local;
const split = name => {
  const colon = name.indexOf(':');
  return colon < 0 ? ['', name] : [name.slice(0, colon), name.slice(colon + 1)];
};

export function parse(bytes) {
  const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  const tree = xmljs.xml2js(text, {
    compact: false, trim: false, nativeType: false,
    nativeTypeAttributes: false, captureSpacesBetweenElements: true,
    alwaysChildren: true,
  });
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
  const walk = (node, depth, parentScope) => {
    flush();
    const scope = new Map(parentScope);
    for (const [name, value] of Object.entries(node.attributes ?? {})) {
      if (name === 'xmlns' || name.startsWith('xmlns:')) {
        declarations++;
        scope.set(name === 'xmlns' ? '' : name.slice(6), value);
        if (value) namespaces.add(value);
      }
    }
    const [prefix, local] = split(node.name);
    if (!scope.has(prefix)) throw new Error(`unbound namespace prefix: ${prefix}`);
    elements.push(clark(scope.get(prefix), local));
    maxDepth = Math.max(maxDepth, depth);
    for (const [name, value] of Object.entries(node.attributes ?? {})) {
      if (name === 'xmlns' || name.startsWith('xmlns:')) continue;
      const [attributePrefix, attributeLocal] = split(name);
      if (attributePrefix && !scope.has(attributePrefix))
        throw new Error(`unbound attribute namespace prefix: ${attributePrefix}`);
      attributes.push(`${clark(attributePrefix ? scope.get(attributePrefix) : '', attributeLocal)}=${value}`);
    }
    for (const child of node.elements ?? []) {
      if (child.type === 'element') walk(child, depth + 1, scope);
      else if (child.type === 'text') pending += child.text;
      else if (child.type === 'cdata') pending += child.cdata;
      else flush();
    }
    flush();
  };
  const roots = (tree.elements ?? []).filter(node => node.type === 'element');
  if (roots.length !== 1) throw new Error('expected one XML root element');
  walk(roots[0], 1, new Map([['', ''], ['xml', 'http://www.w3.org/XML/1998/namespace']]));
  return {
    attributes, elements, max_depth: maxDepth,
    namespace_declarations: declarations,
    namespaces: [...namespaces].sort(), root: elements[0], text: segments,
  };
}
