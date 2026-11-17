'use strict';
// sqllens: parse(text, 'postgres') returns {ast, errors, cst}. The documented `cst` is the full
// ANTLR4 parse tree of its forked PostgreSQL grammar (dist/generated/postgres). Its lowered IR
// marks INSERT as unsupported ("non-query"), so every summary field is read from the CST by
// rule-context class name.
const { parse: parseSql } = require('sqllens');

const decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true });

function rejected(name, message) {
  const error = new Error(message);
  error.name = name;
  return error;
}

const rule = node => (node.ruleIndex === undefined ? null : node.constructor.name.replace(/Context$/, ''));

function find(node, name, found = []) {
  if (!node) return found;
  if (rule(node) === name) found.push(node);
  for (const child of node.children || []) find(child, name, found);
  return found;
}

function first(node, name) {
  return find(node, name)[0];
}

function byteOrder(a, b) {
  const left = a.join('\u0000'), right = b.join('\u0000');
  return left < right ? -1 : left > right ? 1 : 0;
}

function sortedUnique(values) {
  return [...new Set(values)].sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
}

function unquote(text) {
  if (text.length < 2 || text[0] !== "'" || text[text.length - 1] !== "'") return text;
  return text.slice(1, -1).split("''").join("'");
}

function literals(node) {
  const found = [];
  for (const name of ['Iconst', 'Fconst']) {
    for (const item of find(node, name)) found.push(['number', item.getText()]);
  }
  for (const item of find(node, 'Anysconst')) found.push(['string', unquote(item.getText())]);
  return found.sort(byteOrder);
}

function summarize(statement) {
  const insert = first(statement, 'Insertstmt');
  if (insert) {
    const values = first(insert, 'Values_clause');
    return {
      kind: 'insert',
      tables: [first(insert, 'Insert_target').getText().toLowerCase()],
      columns: find(insert, 'Insert_column_item').length,
      rows: values ? find(values, 'Expr_list').length : 0,
      literals: literals(values),
    };
  }
  const select = first(statement, 'Simple_select_pramary');
  if (select) {
    const from = first(select, 'From_clause');
    const targets = first(select, 'Target_list');
    const tables = find(from, 'Relation_expr').map(item => item.getText().toLowerCase());
    return {
      kind: 'select',
      tables: sortedUnique(tables),
      select_items: (targets?.children || []).filter(item => item.ruleIndex !== undefined).length,
      joins: find(from, 'Joined_table').length,
      where: first(select, 'Where_clause') !== undefined,
      group_by: find(select, 'Group_by_item').length,
      order_by: find(statement, 'Sortby').length,
      functions: sortedUnique(find(select, 'Func_name').map(item => item.getText().toLowerCase())),
      literals: literals(statement),
    };
  }
  return { kind: rule(statement.children?.[0]) || 'unknown' };
}

function parse(bytes) {
  let text;
  try { text = decoder.decode(bytes); }
  catch (error) {
    if (!(error instanceof TypeError)) throw error;
    throw rejected('InputDecodeError', 'input is not valid UTF-8');
  }
  let result;
  try { result = parseSql(text, 'postgres'); }
  catch (error) { throw rejected('ParseRejectedError', String(error?.message || error)); }
  if (result.errors) throw rejected('ParseRejectedError', `${result.errors} syntax error(s)`);
  const summaries = find(result.cst, 'Stmt').map(summarize);
  return { statement_count: summaries.length, statements: summaries };
}

module.exports = { parse };
