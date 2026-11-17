// Local bytes are decoded as strict UTF-8 text and passed once to
// parse(text, { integersAsBigInt: true }), toml-patch's documented string API. With that
// documented option every TOML integer comes back as a BigInt and every TOML float as a
// Number, so integer 1000 and float 1e3 stay distinct. Date-times come back as the
// package's exported Date subclasses OffsetDateTime, LocalDateTime, LocalDate and LocalTime.
// The typed tree is built only from the returned values; the TOML text is never re-parsed.
import { parse, OffsetDateTime, LocalDateTime, LocalDate, LocalTime } from '@decimalturn/toml-patch';

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

// The four classes extend Date and store their wall-clock fields in the Date's UTC
// fields; Date.prototype.toISOString gives those fields (millisecond precision).
const iso = value => Date.prototype.toISOString.call(value);

function scalarDate(value) {
  // Offset date-time: the Date's instant is the UTC instant.
  if (value instanceof OffsetDateTime) return { type: 'datetime', value: trimFraction(iso(value)) };
  if (value instanceof LocalDateTime) return { type: 'datetime-local', value: trimFraction(iso(value).slice(0, -1)) };
  if (value instanceof LocalDate) return { type: 'date-local', value: iso(value).slice(0, 10) };
  if (value instanceof LocalTime) return { type: 'time-local', value: trimFraction(iso(value).slice(11, -1)) };
  throw new Error(`unexpected toml-patch date ${Object.prototype.toString.call(value)}`);
}

export function tree(value) {
  if (Array.isArray(value)) return value.map(tree);
  switch (typeof value) {
    case 'string': return { type: 'string', value };
    case 'boolean': return { type: 'bool', value: String(value) };
    case 'bigint': return { type: 'integer', value: value.toString() };
    case 'number': return { type: 'float', value: floatText(value) };
    case 'object':
      if (value instanceof Date) return scalarDate(value);
      if (value !== null && [Object.prototype, null].includes(Object.getPrototypeOf(value))) {
        return Object.fromEntries(Object.keys(value).map(key => [key, tree(value[key])]));
      }
  }
  throw new Error(`unexpected toml-patch value ${Object.prototype.toString.call(value)}`);
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
  return tree(parse(decoder.decode(bytes), { integersAsBigInt: true }));
}
