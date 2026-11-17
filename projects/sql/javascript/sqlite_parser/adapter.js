'use strict';
// sqlite-parser: sqliteParser(text) returns the AST built by its PEG.js-generated SQLite
// grammar (lib/parser.js). Every summary field is read from that AST.
const sqliteParser = require('sqlite-parser');

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
    if (item.type !== 'literal') return;
    if (item.variant === 'decimal') found.push(['number', String(item.value)]);
    else if (item.variant === 'text') found.push(['string', String(item.value)]);
  });
  return found.sort(byteOrder);
}

function listLength(node) {
  if (!node) return 0;
  if (Array.isArray(node)) return node.length;
  if (node.type === 'expression' && node.variant === 'list') return node.expression.length;
  return 1;
}

function summarize(statement) {
  if (statement.variant === 'select') {
    const tables = [];
    let joins = 0;
    walk(statement.from, item => {
      if (item.type === 'identifier' && item.variant === 'table') tables.push(item.name.toLowerCase());
      if (item.type === 'join') joins++;
    });
    const functions = [];
    walk(statement, item => { if (item.type === 'function') functions.push(item.name.name.toLowerCase()); });
    return {
      kind: 'select',
      tables: sortedUnique(tables),
      select_items: statement.result.length,
      joins,
      where: listLength(statement.where) > 0,
      group_by: listLength(statement.group),
      order_by: listLength(statement.order),
      functions: sortedUnique(functions),
      literals: literals(statement),
    };
  }
  if (statement.variant === 'insert') {
    const rows = Array.isArray(statement.result) ? statement.result : [];
    return {
      kind: 'insert',
      tables: [statement.into.name.toLowerCase()],
      columns: (statement.into.columns || []).length,
      rows: rows.filter(item => item.type === 'expression' && item.variant === 'list').length,
      literals: literals(statement.result),
    };
  }
  return { kind: String(statement.variant) };
}

function parse(bytes) {
  let text;
  try { text = decoder.decode(bytes); }
  catch (error) {
    if (!(error instanceof TypeError)) throw error;
    throw rejected('InputDecodeError', 'input is not valid UTF-8');
  }
  let tree;
  try { tree = sqliteParser(text); }
  catch (error) { throw rejected('ParseRejectedError', String(error?.message || error)); }
  const summaries = tree.statement.map(summarize);
  return { statement_count: summaries.length, statements: summaries };
}

module.exports = { parse };
