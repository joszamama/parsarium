'use strict';
// pgsql-ast-parser: parse(text) returns typed PostgreSQL statement ASTs from its own
// nearley grammar and moo lexer. Every summary field is read from those AST objects.
const { parse: parseSql } = require('pgsql-ast-parser');

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
    if (item.type === 'integer' || item.type === 'numeric') found.push(['number', String(item.value)]);
    else if (item.type === 'string') found.push(['string', String(item.value)]);
  });
  return found.sort(byteOrder);
}

function summarize(statement) {
  if (statement.type === 'select') {
    const from = statement.from || [];
    const functions = [];
    walk(statement, item => { if (item.type === 'call') functions.push(item.function.name.toLowerCase()); });
    return {
      kind: 'select',
      tables: sortedUnique(from.filter(item => item.type === 'table').map(item => item.name.name.toLowerCase())),
      select_items: (statement.columns || []).length,
      joins: from.filter(item => item.join).length,
      where: statement.where != null,
      group_by: (statement.groupBy || []).length,
      order_by: (statement.orderBy || []).length,
      functions: sortedUnique(functions),
      literals: literals(statement),
    };
  }
  if (statement.type === 'insert') {
    return {
      kind: 'insert',
      tables: [statement.into.name.toLowerCase()],
      columns: (statement.columns || []).length,
      rows: statement.insert?.type === 'values' ? statement.insert.values.length : 0,
      literals: literals(statement.insert),
    };
  }
  return { kind: String(statement.type) };
}

function parse(bytes) {
  let text;
  try { text = decoder.decode(bytes); }
  catch (error) {
    if (!(error instanceof TypeError)) throw error;
    throw rejected('InputDecodeError', 'input is not valid UTF-8');
  }
  let statements;
  try { statements = parseSql(text); }
  catch (error) { throw rejected('ParseRejectedError', String(error?.message || error)); }
  const summaries = statements.map(summarize);
  return { statement_count: summaries.length, statements: summaries };
}

module.exports = { parse };
