// Local bytes are decoded as strict UTF-8 text and passed once to TomlVisitor.visit(text),
// @effected/toml's documented event walker. It parses the whole document into its lossless
// syntax tree, runs its semantic analysis (failing on invalid TOML) and yields, in document
// order, TableStart/ArrayTableStart events with the resolved table path (and array index)
// and KeyValue events with the resolved full key path and the parsed TomlKeyValue node.
// Value nodes are typed by the parser: TomlString, TomlInteger, TomlFloat, TomlBoolean,
// TomlDateTimeLiteral (TomlOffsetDateTime, TomlLocalDateTime, TomlLocalDate, TomlLocalTime
// field objects), TomlArray and TomlInlineTable. The typed tree is assembled from those
// events and nodes only; the TOML text is never re-parsed.
import { TomlVisitor, TomlOffsetDateTime, TomlLocalDateTime, TomlLocalDate, TomlLocalTime } from '@effected/toml';
import { Effect, Stream } from 'effect';

const decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true });

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

// Seconds plus the significant digits of the nanosecond field.
function seconds(second, nanosecond) {
  const fraction = pad(nanosecond, 9).replace(/0+$/, '');
  return fraction ? `${pad(second)}.${fraction}` : pad(second);
}

const dateText = value => `${pad(value.year, 4)}-${pad(value.month)}-${pad(value.day)}`;
const timeText = value => `${pad(value.hour)}:${pad(value.minute)}:${seconds(value.second, value.nanosecond)}`;

function dateTime(value) {
  if (value instanceof TomlOffsetDateTime) {
    // The UTC instant: wall-clock fields minus the parsed offset, nanoseconds kept.
    const instant = new Date(0);
    instant.setUTCFullYear(value.year, value.month - 1, value.day);
    instant.setUTCHours(value.hour, value.minute - value.offsetMinutes, value.second);
    const utc = { year: instant.getUTCFullYear(), month: instant.getUTCMonth() + 1, day: instant.getUTCDate(),
                  hour: instant.getUTCHours(), minute: instant.getUTCMinutes(), second: instant.getUTCSeconds(),
                  nanosecond: value.nanosecond };
    return { type: 'datetime', value: `${dateText(utc)}T${timeText(utc)}Z` };
  }
  if (value instanceof TomlLocalDateTime) return { type: 'datetime-local', value: `${dateText(value)}T${timeText(value)}` };
  if (value instanceof TomlLocalDate) return { type: 'date-local', value: dateText(value) };
  if (value instanceof TomlLocalTime) return { type: 'time-local', value: timeText(value) };
  throw new Error(`unexpected @effected/toml date-time ${Object.prototype.toString.call(value)}`);
}

function setPath(table, keys, value) {
  let current = table;
  for (const key of keys.slice(0, -1)) {
    if (!Object.hasOwn(current, key)) current[key] = {};
    current = current[key];
  }
  current[keys.at(-1)] = value;
}

function node(value) {
  switch (value._tag) {
    case 'TomlString': return { type: 'string', value: value.value };
    case 'TomlBoolean': return { type: 'bool', value: String(value.value) };
    case 'TomlInteger': return { type: 'integer', value: BigInt(value.value).toString() };
    case 'TomlFloat': return { type: 'float', value: floatText(value.value) };
    case 'TomlDateTimeLiteral': return dateTime(value.value);
    case 'TomlArray': return value.items.map(node);
    case 'TomlInlineTable': {
      const table = {};
      for (const entry of value.entries) setPath(table, entry.keyPath.map(key => key.value), node(entry.value));
      return table;
    }
  }
  throw new Error(`unexpected @effected/toml value node ${value._tag}`);
}

// Follow a resolved path from the root; an array of tables resolves to its last element,
// the table the most recent ArrayTableStart event opened.
function walk(root, keys) {
  let current = root;
  for (const key of keys) {
    if (!Object.hasOwn(current, key)) current[key] = {};
    current = current[key];
    if (Array.isArray(current)) current = current.at(-1);
  }
  return current;
}

export function tree(events) {
  const root = {};
  for (const event of events) {
    switch (event._tag) {
      case 'TableStart':
        walk(root, event.path);
        break;
      case 'ArrayTableStart': {
        const parent = walk(root, event.path.slice(0, -1));
        const key = event.path.at(-1);
        if (!Object.hasOwn(parent, key)) parent[key] = [];
        if (parent[key].length !== event.index) throw new Error(`array table ${event.path.join('.')} out of order`);
        parent[key].push({});
        break;
      }
      case 'KeyValue':
        walk(root, event.path.slice(0, -1))[event.path.at(-1)] = node(event.node.value);
        break;
      case 'Comment':
        break;
      default:
        throw new Error(`unexpected @effected/toml event ${event._tag}`);
    }
  }
  return root;
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
  return tree(Effect.runSync(Stream.runCollect(TomlVisitor.visit(decoder.decode(bytes)))));
}
