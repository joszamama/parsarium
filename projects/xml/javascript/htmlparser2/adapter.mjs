// Local bytes are strictly UTF-8 decoded and written to htmlparser2's documented
// callback Parser with {xmlMode: true}: parser.write(text) then parser.end().
// htmlparser2 does not resolve namespaces. Tag and attribute names arrive as
// the raw qualified names (prefix:local), and xmlns/xmlns:* declarations are
// ordinary attributes, so the summary keeps those raw names and reports no
// namespace URIs. It does not check well-formedness either: only misuse of the
// parser reaches onerror. Text and CDATA are joined between markup.
import { Parser } from 'htmlparser2';

export function parse(bytes) {
  const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  const elements = [];
  const attributes = [];
  const segments = [];
  const comments = [];
  const instructions = [];
  let pending = '';
  let comment = '';
  let depth = 0;
  let maxDepth = 0;
  let cdata = 0;
  let failure = null;
  const flush = () => {
    const segment = pending.trim();
    if (segment) segments.push(segment);
    pending = '';
  };
  const parser = new Parser({
    onopentagname(name) {
      flush();
      elements.push(name);
      depth++;
      maxDepth = Math.max(maxDepth, depth);
    },
    // onattribute keeps source order; the onopentag object would merge repeats.
    onattribute(name, value) { attributes.push(`${name}=${value}`); },
    onclosetag() { flush(); depth--; },
    ontext(data) { pending += data; },
    oncdatastart() { cdata++; },
    oncomment(data) { flush(); comment += data; },
    oncommentend() { comments.push(comment); comment = ''; },
    // The data is the raw section after '<', with the trailing '?' removed;
    // the XML declaration arrives here as '?xml ...'.
    onprocessinginstruction(_name, data) { flush(); instructions.push(data.slice(1)); },
    onerror(error) { failure ??= error; },
  }, { xmlMode: true });
  parser.write(text);
  parser.end();
  if (failure) throw failure;
  if (elements.length === 0) throw new Error('no root element');
  return {
    attributes,
    cdata_sections: cdata,
    comments,
    elements,
    max_depth: maxDepth,
    processing_instructions: instructions,
    root: elements[0],
    text: segments,
  };
}
