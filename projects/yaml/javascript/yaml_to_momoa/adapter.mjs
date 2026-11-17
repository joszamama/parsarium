import yamlToMomoa from 'yaml-to-momoa';

const decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: false });

function rejected(name, message) {
  const error = new Error(message);
  error.name = name;
  return error;
}

function decode(bytes) {
  try { return decoder.decode(bytes); }
  catch (error) {
    if (!(error instanceof TypeError)) throw error;
    throw rejected('InputDecodeError', 'input is not valid UTF-8');
  }
}

// Parsarium typed YAML tree (controls/yaml/check_controls.py) read from the returned
// Momoa JSON AST. Momoa Number nodes do not keep YAML's int/float distinction: a finite
// integral number is tagged int. Member names are Momoa String nodes in source order.
function tag(node) {
  switch (node?.type) {
    case 'Null': return ['null'];
    case 'Boolean': return ['bool', node.value];
    case 'String': return ['str', node.value];
    case 'Number':
      if (typeof node.value === 'bigint') return ['int', node.value.toString()];
      if (!Number.isFinite(node.value)) return ['float', String(node.value)];
      return Number.isInteger(node.value) ? ['int', String(node.value)] : ['float', String(node.value)];
    case 'Array': return ['seq', node.elements.map(element => tag(element.value))];
    case 'Object':
      return ['map', node.members.map(member => {
        if (member.name?.type !== 'String')
          throw rejected('ParseRejectedError', `unsupported member name node ${member.name?.type}`);
        return [member.name.value, tag(member.value)];
      })];
    default:
      throw rejected('ParseRejectedError', `unsupported Momoa node ${node?.type}`);
  }
}

export function parse(bytes) {
  const text = decode(bytes);
  // Documented default export yamlToMomoa(yaml): yaml 2.9.1 parseDocument, then the
  // package's own transform of the document tree (aliases expanded) to a Momoa
  // Document. It throws the first yaml error, or when the document has no contents.
  let document;
  try { document = yamlToMomoa(text); }
  catch (error) {
    if (error?.name === 'YAMLParseError' || error?.message === 'YAML content null')
      throw rejected('ParseRejectedError', error.message);
    throw error;
  }
  if (document?.type !== 'Document') throw rejected('ParseRejectedError', 'no Momoa Document returned');
  return { tree: tag(document.body) };
}
