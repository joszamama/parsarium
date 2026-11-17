// Local bytes are decoded as strict UTF-8 text and passed once to
// TOML.parse[1.0](text, { joiner: '\n', bigint: true }), j-toml's documented TOML 1.0
// string API. With bigint: true every TOML integer comes back as a BigInt and every TOML
// float as a Number, so integer 1000 and float 1e3 stay distinct. joiner: '\n' joins the
// lines of multi-line strings with LF (the controls use LF line endings). Date-times come
// back as j-toml's own OffsetDateTime, LocalDateTime, LocalDate and LocalTime classes.
// The typed tree is built only from the returned values; the TOML text is never re-parsed.
import TOML from '@ltd/j-toml';

const { OffsetDateTime, LocalDateTime, LocalDate, LocalTime } = TOML;
const decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true });

// Drop trailing zeros of a fractional-seconds part, and the dot when nothing is left.
function trimFraction(text) {
  return text.replace(/\.(\d*?)0+(?=Z?$)/, (_, digits) => digits ? `.${digits}` : '');
}

// Shortest round-trip digits (Number.prototype.toString) written positionally with at
// least one fractional digit: 1e3 -> 1000.0, 1.5625e-2 -> 0.015625.
export function floatText(value) {
  if (Number.isNaN(value)) return 'nan';
  if (!Number.isFinite(value)) return value > 0 ? 'inf' : '-inf';
  const negative = value < 0 || Object.is(value, -0);
  const [mantissa, exponent = '0'] = Math.abs(value).toString().split('e');
  const dot = mantissa.indexOf('.');
  let digits = mantissa.replace('.', '');
  let point = (dot < 0 ? mantissa.length : dot) + Number(exponent);
  while (digits.length > 1 && digits[0] === '0') {
    digits = digits.slice(1);
    point--;
  }
  let text;
  if (point <= 0) text = `0.${'0'.repeat(-point)}${digits}`;
  else if (point >= digits.length) text = `${digits}${'0'.repeat(point - digits.length)}.0`;
  else text = `${digits.slice(0, point)}.${digits.slice(point)}`;
  return (negative ? '-' : '') + text;
}

const pad = (number, width = 2) => String(number).padStart(width, '0');

// Offset date-time: the UTC instant from OffsetDateTime's documented getUTC* getters
// (millisecond precision), not its as-authored toISOString rendering.
function utcInstant(value) {
  const millis = value.getUTCMilliseconds();
  const text = `${pad(value.getUTCFullYear(), 4)}-${pad(value.getUTCMonth() + 1)}-${pad(value.getUTCDate())}` +
    `T${pad(value.getUTCHours())}:${pad(value.getUTCMinutes())}:${pad(value.getUTCSeconds())}` +
    `.${pad(millis, 3)}Z`;
  return trimFraction(text);
}

export function tree(value) {
  if (Array.isArray(value)) return value.map(tree);
  switch (typeof value) {
    case 'string': return { type: 'string', value };
    case 'boolean': return { type: 'bool', value: String(value) };
    case 'bigint': return { type: 'integer', value: value.toString() };
    case 'number': return { type: 'float', value: floatText(value) };
    case 'object':
      if (value instanceof OffsetDateTime) return { type: 'datetime', value: utcInstant(value) };
      if (value instanceof LocalDateTime) return { type: 'datetime-local', value: trimFraction(value.toISOString()) };
      if (value instanceof LocalDate) return { type: 'date-local', value: value.toISOString() };
      if (value instanceof LocalTime) return { type: 'time-local', value: trimFraction(value.toISOString()) };
      // j-toml tables are instances of its internal null-prototype Table class
      // (Object.getPrototypeOf(table) has a null prototype); they carry no other fields.
      if (value !== null && Object.getPrototypeOf(Object.getPrototypeOf(value)) === null) {
        return Object.fromEntries(Object.keys(value).map(key => [key, tree(value[key])]));
      }
  }
  throw new Error(`unexpected j-toml value ${Object.prototype.toString.call(value)}`);
}

// Canonical JSON with sorted object keys, so key order is not significant.
export function canonical(node) {
  if (Array.isArray(node)) return `[${node.map(canonical).join(',')}]`;
  if (node !== null && typeof node === 'object') {
    return `{${Object.keys(node).sort().map(key => `${JSON.stringify(key)}:${canonical(node[key])}`).join(',')}}`;
  }
  return JSON.stringify(node);
}

export function decode(bytes) {
  return tree(TOML.parse[1.0](decoder.decode(bytes), { joiner: '\n', bigint: true }));
}
