'use strict';
// node-sql-parser PostgreSQL build: Parser.astify(text, {database: 'postgresql'}).
// Every summary field is read from the returned AST objects; the SQL text is not inspected.
const { Parser } = require('node-sql-parser/build/postgresql');

const parser = new Parser();
const decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true });
const OPTIONS = { database: 'postgresql' };

function rejected(name, message) {
  const error = new Error(message);
  error.name = name;
  return error;
}

function functionName(node) {
  if (typeof node.name === 'string') return node.name;
  const parts = node.name?.name;
  if (Array.isArray(parts) && parts.length) return String(parts[parts.length - 1].value);
  throw new Error('unexpected function name shape');
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

function literals(statement) {
  const found = [];
  walk(statement, node => {
    if (node.type === 'number') found.push(['number', String(node.value)]);
    else if (node.type === 'single_quote_string') found.push(['string', String(node.value)]);
  });
  return found.sort(byteOrder);
}

function sortedUnique(values) {
  return [...new Set(values)].sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
}

function summarize(statement) {
  if (statement.type === 'select') {
    const from = statement.from || [];
    const functions = [];
    walk(statement, node => {
      if (node.type === 'aggr_func' || node.type === 'function') functions.push(functionName(node).toLowerCase());
    });
    return {
      kind: 'select',
      tables: sortedUnique(from.filter(item => item.table).map(item => item.table.toLowerCase())),
      select_items: statement.columns.length,
      joins: from.filter(item => item.join).length,
      where: statement.where != null,
      group_by: statement.groupby?.columns?.length ?? 0,
      order_by: statement.orderby?.length ?? 0,
      functions: sortedUnique(functions),
      literals: literals(statement),
    };
  }
  if (statement.type === 'insert') {
    return {
      kind: 'insert',
      tables: sortedUnique(statement.table.map(item => item.table.toLowerCase())),
      columns: (statement.columns || []).length,
      rows: statement.values?.values?.length ?? 0,
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
  let ast;
  try { ast = parser.astify(text, OPTIONS); }
  catch (error) {
    if (error?.name === 'SyntaxError' || error?.name === 'peg$SyntaxError') throw rejected('ParseRejectedError', error.message);
    throw error;
  }
  const statements = Array.isArray(ast) ? ast : [ast];
  const summaries = statements.map(summarize);
  return { statement_count: summaries.length, statements: summaries };
}

module.exports = { parse };
