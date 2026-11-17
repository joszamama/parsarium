'use strict';
// @questdb/sql-parser: parseToAst(text) returns {ast, errors}; the AST is built from the
// package's Chevrotain parser for QuestDB SQL. Every summary field is read from that AST.
const { parseToAst } = require('@questdb/sql-parser');

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
    if (item.literalType === 'number') found.push(['number', String(item.raw ?? item.value)]);
    else if (item.literalType === 'string') found.push(['string', String(item.value)]);
  });
  return found.sort(byteOrder);
}

const name = qualified => qualified.parts[qualified.parts.length - 1].toLowerCase();

function summarize(statement) {
  if (statement.type === 'select') {
    const tables = [];
    let joins = 0;
    for (const source of statement.from || []) {
      if (source.type === 'tableRef' && source.table?.type === 'qualifiedName') tables.push(name(source.table));
      for (const join of source.joins || []) {
        joins++;
        if (join.table?.type === 'tableRef' && join.table.table?.type === 'qualifiedName') tables.push(name(join.table.table));
      }
    }
    const functions = [];
    walk(statement, item => { if (item.type === 'function') functions.push(String(item.name).toLowerCase()); });
    return {
      kind: 'select',
      tables: sortedUnique(tables),
      select_items: statement.columns.length,
      joins,
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
      tables: [name(statement.table)],
      columns: (statement.columns || []).length,
      rows: (statement.values || []).length,
      literals: literals(statement.values),
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
  let result;
  try { result = parseToAst(text); }
  catch (error) { throw rejected('ParseRejectedError', String(error?.message || error)); }
  if (result.errors.length) throw rejected('ParseRejectedError', String(result.errors[0]?.message || 'syntax error'));
  const summaries = result.ast.map(summarize);
  return { statement_count: summaries.length, statements: summaries };
}

module.exports = { parse };
