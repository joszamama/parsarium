import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const yaml = require('yaml-js');
const { YAMLError } = require('yaml-js/lib/errors');

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
  let value;
  // Documented single-document load(string) (PyYAML-port Loader: reader, scanner,
  // parser, composer, constructor, resolver); a YAMLError rejects the input.
  try { value = yaml.load(text); }
  catch (error) {
    if (error instanceof YAMLError) throw rejected('ParseRejectedError', String(error.message || error));
    throw error;
  }
  return { tree: tag(value === undefined ? null : value) };
}
