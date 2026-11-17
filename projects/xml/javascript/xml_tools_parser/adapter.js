const { parse } = require('@xml-tools/parser');

// The package returns a concrete syntax tree. Names and attribute values here
// are the original token images; no namespace or entity interpretation is added.
function project(data) {
  const { cst, tokenVector, lexErrors, parseErrors } = parse(data);
  const roots = cst.children.element || [];
  if (roots.length !== 1) throw new Error(`expected one CST root, got ${roots.length}`);

  let maxDepth = 0;
  function element(node, depth) {
    maxDepth = Math.max(maxDepth, depth);
    return {
      qname: node.children.Name?.[0]?.image ?? null,
      attributes: (node.children.attribute || []).map(attribute => ({
        qname: attribute.children.Name?.[0]?.image ?? null,
        raw_value: attribute.children.STRING?.[0]?.image ?? null,
      })),
      children: (node.children.content || []).flatMap(content =>
        (content.children.element || []).map(child => element(child, depth + 1))),
    };
  }
  return {
    tree: element(roots[0], 1),
    max_depth: maxDepth,
    token_count: tokenVector.length,
    lex_errors: lexErrors.length,
    parse_errors: parseErrors.length,
  };
}

module.exports = { project };
