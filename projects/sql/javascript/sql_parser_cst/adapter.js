'use strict';
// sql-parser-cst: parse(text, {dialect: 'sqlite'}) returns a concrete syntax tree from its own
// Peggy grammar (lib/parser.js). Every summary field is read from those CST nodes.
const { parse: parseSql } = require('sql-parser-cst');

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
    if (item.type === 'number_literal') found.push(['number', item.text]);
    else if (item.type === 'string_literal') found.push(['string', String(item.value)]);
  });
  return found.sort(byteOrder);
}

function tableName(node) {
  if (node.type === 'identifier') return node.name.toLowerCase();
  if (node.type === 'member_expr' && node.property?.type === 'identifier') return node.property.name.toLowerCase();
  return null;
}

// Base tables of a FROM expression: join operands, optionally aliased; aliases are not tables.
function relations(node, tables, counts) {
  if (!node) return;
  if (node.type === 'join_expr') {
    counts.joins++;
    relations(node.left, tables, counts);
    relations(node.right, tables, counts);
  } else if (node.type === 'alias') {
    relations(node.expr, tables, counts);
  } else {
    const name = tableName(node);
    if (name !== null) tables.push(name);
  }
}

function clause(statement, type) {
  return statement.clauses.find(item => item.type === type);
}

function summarize(statement) {
  if (statement.type === 'select_stmt') {
    const select = clause(statement, 'select_clause');
    const from = clause(statement, 'from_clause');
    const tables = [], counts = { joins: 0 };
    relations(from?.expr, tables, counts);
    const functions = [];
    walk(statement, item => { if (item.type === 'func_call') functions.push(item.name.name.toLowerCase()); });
    return {
      kind: 'select',
      tables: sortedUnique(tables),
      select_items: select.columns.items.length,
      joins: counts.joins,
      where: clause(statement, 'where_clause') !== undefined,
      group_by: clause(statement, 'group_by_clause')?.columns.items.length ?? 0,
      order_by: clause(statement, 'order_by_clause')?.specifications.items.length ?? 0,
      functions: sortedUnique(functions),
      literals: literals(statement),
    };
  }
  if (statement.type === 'insert_stmt') {
    const insert = clause(statement, 'insert_clause');
    const values = clause(statement, 'values_clause');
    return {
      kind: 'insert',
      tables: [tableName(insert.table)],
      columns: insert.columns ? insert.columns.expr.items.length : 0,
      rows: values ? values.values.items.length : 0,
      literals: literals(values),
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
  let program;
  try { program = parseSql(text, { dialect: 'sqlite' }); }
  catch (error) { throw rejected('ParseRejectedError', String(error?.message || error)); }
  // The trailing ';' yields an `empty` statement node; it is not a statement.
  const summaries = program.statements.filter(item => item.type !== 'empty').map(summarize);
  return { statement_count: summaries.length, statements: summaries };
}

module.exports = { parse };
