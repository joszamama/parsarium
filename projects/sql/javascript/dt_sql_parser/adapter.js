'use strict';
// dt-sql-parser: new MySQL().parse(text, errorListener) returns the ANTLR4 parse tree of its
// generated MySQL grammar (dist/lib/mysql/MySqlParser.js). Every summary field is read from
// that tree's rule contexts and terminal tokens.
//
// The published dist is ES module code with extensionless relative imports (it targets
// bundlers). This resolve hook only retries such specifiers from inside dt-sql-parser with
// '.js' or '/index.js'; no package file is changed.
const { registerHooks } = require('node:module');

registerHooks({
  resolve(specifier, context, next) {
    try { return next(specifier, context); }
    catch (error) {
      if (!['ERR_UNSUPPORTED_DIR_IMPORT', 'ERR_MODULE_NOT_FOUND'].includes(error.code)
          || !specifier.startsWith('.')
          || !String(context.parentURL).startsWith('file:///work/node_modules/dt-sql-parser/')) throw error;
      for (const suffix of ['.js', '/index.js']) {
        try { return next(specifier + suffix, context); } catch { /* try the next suffix */ }
      }
      throw error;
    }
  },
});

const { MySQL } = require('dt-sql-parser');

const mysql = new MySQL();
const RULES = mysql.createParser('').ruleNames;
const decoder = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true });

function rejected(name, message) {
  const error = new Error(message);
  error.name = name;
  return error;
}

const rule = node => (node.ruleIndex === undefined ? null : RULES[node.ruleIndex]);

function find(node, name, found = []) {
  if (rule(node) === name) found.push(node);
  for (const child of node.children || []) find(child, name, found);
  return found;
}

function child(node, name) {
  return (node.children || []).find(item => rule(item) === name);
}

function terminals(node) {
  return (node.children || []).filter(item => item.ruleIndex === undefined).map(item => item.getText());
}

function byteOrder(a, b) {
  const left = a.join('\u0000'), right = b.join('\u0000');
  return left < right ? -1 : left > right ? 1 : 0;
}

function sortedUnique(values) {
  return [...new Set(values)].sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
}

function unquote(text) {
  const quote = text[0];
  if ((quote !== "'" && quote !== '"') || text[text.length - 1] !== quote) return text;
  return text.slice(1, -1).split(quote + quote).join(quote);
}

function literals(node) {
  const found = [];
  for (const item of find(node, 'decimalLiteral')) found.push(['number', item.getText()]);
  for (const item of find(node, 'stringLiteral')) found.push(['string', unquote(item.getText())]);
  return found.sort(byteOrder);
}

function functionNames(node) {
  const names = [];
  for (const item of find(node, 'aggregateWindowedFunction')) names.push(terminals(item)[0]);
  for (const item of find(node, 'scalarFunctionName')) names.push(item.getText());
  return sortedUnique(names.map(name => name.toLowerCase()));
}

function summarize(statement) {
  const query = find(statement, 'querySpecification')[0];
  if (query) {
    const from = child(query, 'fromClause');
    const tables = from ? find(from, 'tableName').map(item => item.getText().toLowerCase()) : [];
    return {
      kind: 'select',
      tables: sortedUnique(tables),
      select_items: find(child(query, 'selectElements'), 'selectElement').length,
      joins: from ? find(from, 'joinPart').length : 0,
      where: from ? terminals(from).some(text => text.toUpperCase() === 'WHERE') : false,
      group_by: find(query, 'groupByItem').length,
      order_by: find(query, 'orderByExpression').length,
      functions: functionNames(query),
      literals: literals(query),
    };
  }
  const insert = find(statement, 'insertStatement')[0];
  if (insert) {
    const values = child(insert, 'valuesOrValueList');
    const columns = child(insert, 'fullColumnNames');
    return {
      kind: 'insert',
      tables: [child(insert, 'tableName').getText().toLowerCase()],
      columns: columns ? find(columns, 'columnName').length : 0,
      rows: values ? find(values, 'expressionsWithDefaults').length : 0,
      literals: literals(values),
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
  const errors = [];
  let tree;
  try { tree = mysql.parse(text, error => errors.push(error)); }
  catch (error) { throw rejected('ParseRejectedError', String(error?.message || error)); }
  if (errors.length) throw rejected('ParseRejectedError', String(errors[0]?.message || 'syntax error'));
  const summaries = find(tree, 'sqlStatement').map(summarize);
  return { statement_count: summaries.length, statements: summaries };
}

module.exports = { parse };
