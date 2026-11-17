'use strict';
// rawsql-ts: SqlParser.parseMany(text) returns a typed query model (SimpleSelectQuery, InsertQuery)
// built by its own hand-written tokenizer and recursive-descent parsers. Every summary field is
// read from those model objects.
const { SqlParser } = require('rawsql-ts');

const decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true });

function rejected(name, message) {
  const error = new Error(message);
  error.name = name;
  return error;
}

function walk(node, visit) {
  if (Array.isArray(node)) { for (const item of node) walk(item, visit); return; }
  if (node === null || typeof node !== 'object') return;
  visit(node);
  for (const value of Object.values(node)) walk(value, visit);
}

const kind = node => node?.constructor?.name;

function byteOrder(a, b) {
  const left = a.join('\u0000'), right = b.join('\u0000');
  return left < right ? -1 : left > right ? 1 : 0;
}

function sortedUnique(values) {
  return [...new Set(values)].sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
}

function literals(node) {
  const found = [];
  walk(node, item => {
    if (kind(item) !== 'LiteralValue') return;
    if (item.isStringLiteral) found.push(['string', String(item.value)]);
    else if (typeof item.value === 'number') found.push(['number', String(item.value)]);
  });
  return found.sort(byteOrder);
}

function tableName(source) {
  const datasource = source?.datasource;
  return kind(datasource) === 'TableSource' ? datasource.qualifiedName.name.name.toLowerCase() : null;
}

function summarize(query) {
  if (kind(query) === 'SimpleSelectQuery') {
    const from = query.fromClause;
    const sources = from ? [from.source, ...(from.joins || []).map(join => join.source)] : [];
    const functions = [];
    walk(query, item => {
      if (kind(item) === 'FunctionCall') functions.push(String(item.qualifiedName.name.value ?? item.qualifiedName.name.name).toLowerCase());
    });
    return {
      kind: 'select',
      tables: sortedUnique(sources.map(tableName).filter(name => name !== null)),
      select_items: query.selectClause.items.length,
      joins: from ? (from.joins || []).length : 0,
      where: query.whereClause != null,
      group_by: query.groupByClause ? query.groupByClause.grouping.length : 0,
      order_by: query.orderByClause ? query.orderByClause.order.length : 0,
      functions: sortedUnique(functions),
      literals: literals(query),
    };
  }
  if (kind(query) === 'InsertQuery') {
    const values = query.selectQuery;
    return {
      kind: 'insert',
      tables: [tableName(query.insertClause.source)],
      columns: (query.insertClause.columns || []).length,
      rows: kind(values) === 'ValuesQuery' ? values.tuples.length : 0,
      literals: literals(values),
    };
  }
  return { kind: String(kind(query)) };
}

function parse(bytes) {
  let text;
  try { text = decoder.decode(bytes); }
  catch (error) {
    if (!(error instanceof TypeError)) throw error;
    throw rejected('InputDecodeError', 'input is not valid UTF-8');
  }
  let queries;
  try { queries = SqlParser.parseMany(text); }
  catch (error) { throw rejected('ParseRejectedError', String(error?.message || error)); }
  const summaries = queries.map(summarize);
  return { statement_count: summaries.length, statements: summaries };
}

module.exports = { parse };
