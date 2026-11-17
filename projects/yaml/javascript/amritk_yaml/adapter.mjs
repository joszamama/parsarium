import { parseDocument } from '@amritk/yaml';

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

// Parsarium typed YAML tree (controls/yaml/check_controls.py). JavaScript numbers
// do not keep YAML's int/float distinction: a finite integral number is tagged int.
function tag(value) {
  if (value === null) return ['null'];
  if (typeof value === 'boolean') return ['bool', value];
  if (typeof value === 'string') return ['str', value];
  if (typeof value === 'bigint') return ['int', value.toString()];
  if (typeof value === 'number') {
    if (!Number.isFinite(value)) return ['float', String(value)];
    return Number.isInteger(value) ? ['int', String(value)] : ['float', String(value)];
  }
  if (Array.isArray(value)) return ['seq', value.map(tag)];
  const prototype = value === undefined ? undefined : Object.getPrototypeOf(value);
  if (prototype === Object.prototype || prototype === null)
    return ['map', Object.entries(value).map(([key, item]) => [key, tag(item)])];
  throw rejected('ParseRejectedError', `unsupported YAML value ${Object.prototype.toString.call(value)}`);
}

export function parse(bytes) {
  const text = decode(bytes);
  // Documented parseDocument(source) with default options; any error or warning
  // (including MULTIPLE_DOCUMENTS) rejects the input, then toJS() gives native values.
  const document = parseDocument(text);
  if (document.errors.length !== 0 || document.warnings.length !== 0)
    throw rejected('ParseRejectedError',
                   `@amritk/yaml rejected input (${document.errors.length} errors, ${document.warnings.length} warnings)`);
  return { tree: tag(document.toJS() ?? null) };
}
