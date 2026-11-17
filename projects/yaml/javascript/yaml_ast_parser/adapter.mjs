import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const yaml = require('yaml-ast-parser');

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

// Typed tree from the documented AST: YamlMap.mappings (YAMLMapping key/value),
// YAMLSequence.items, YAMLAnchorReference.value (the anchored node) and YAMLScalar.value
// typed with the documented determineScalarType / parseYamlBoolean / parseYamlInteger /
// parseYamlFloat helpers (YAML 1.2 core schema).
function scalar(node) {
  switch (yaml.determineScalarType(node)) {
    case yaml.ScalarType.null: return ['null'];
    case yaml.ScalarType.bool: return ['bool', yaml.parseYamlBoolean(node.value)];
    case yaml.ScalarType.int: return ['int', String(yaml.parseYamlInteger(node.value))];
    case yaml.ScalarType.float: return ['float', String(yaml.parseYamlFloat(node.value))];
    case yaml.ScalarType.string: return ['str', node.value];
  }
  throw rejected('ParseRejectedError', 'unsupported scalar type');
}

function tree(node) {
  if (node === null || node === undefined) return ['null'];
  switch (node.kind) {
    case yaml.Kind.SCALAR: return scalar(node);
    case yaml.Kind.SEQ: return ['seq', node.items.map(tree)];
    case yaml.Kind.ANCHOR_REF: return tree(node.value);
    case yaml.Kind.MAP: return ['map', node.mappings.map(mapping => {
      if (!mapping.key || mapping.key.kind !== yaml.Kind.SCALAR)
        throw rejected('ParseRejectedError', 'non-scalar mapping key');
      return [mapping.key.value, tree(mapping.value)];
    })];
  }
  throw rejected('ParseRejectedError', `unsupported YAML node kind ${node.kind}`);
}

export function parse(bytes) {
  const text = decode(bytes);
  // Documented load(string): the root YAMLNode carries every recovered error.
  const root = yaml.load(text);
  if (root && root.errors && root.errors.length !== 0)
    throw rejected('ParseRejectedError', `yaml-ast-parser reported ${root.errors.length} errors`);
  return { tree: tree(root) };
}
