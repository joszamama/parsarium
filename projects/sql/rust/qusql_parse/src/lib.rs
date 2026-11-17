//! qusql-parse (hand-written lexer and recursive-descent parser, default MariaDB dialect) over
//! local SQL text. The summary is read from its AST only: typed Select/InsertReplace fields and
//! the crate's Visitor walk for table references, joins, function calls and literals.
use std::collections::BTreeSet;
use std::convert::Infallible;
use std::error::Error;

use qusql_parse::{
    parse_statements, walk_expression, walk_table_reference, Expression, Function, Issues, Level,
    ParseOptions, Statement, TableReference, Visitor,
};
use serde_json::{json, Value as Json};

struct Walk<'s> {
    src: &'s str,
    tables: BTreeSet<String>,
    functions: BTreeSet<String>,
    joins: usize,
    literals: Vec<(String, String)>,
}

fn function_name(function: &Function) -> String {
    match function {
        Function::Other(parts) => parts.last().map_or(String::new(), |part| part.value.to_lowercase()),
        named => format!("{named:?}").to_lowercase(),
    }
}

impl<'a, 's> Visitor<'a> for Walk<'s> {
    type T = ();
    type E = Infallible;

    fn visit_expression(&mut self, expr: &Expression<'a>) -> Result<(), Infallible> {
        match expr {
            Expression::Function(call) => {
                self.functions.insert(function_name(&call.function));
            }
            Expression::AggregateFunction(call) => {
                self.functions.insert(function_name(&call.function));
            }
            // Numbers are reported as the source text of their span.
            Expression::Integer(integer) => {
                self.literals.push(("number".into(), self.src[integer.span.clone()].to_string()));
            }
            Expression::Float(float) => {
                self.literals.push(("number".into(), self.src[float.span.clone()].to_string()));
            }
            Expression::String(string) => {
                self.literals.push(("string".into(), string.value.to_string()));
            }
            _ => {}
        }
        walk_expression(self, expr)
    }

    fn visit_table_reference(&mut self, reference: &TableReference<'a>) -> Result<(), Infallible> {
        match reference {
            TableReference::Table { identifier, .. } => {
                self.tables.insert(identifier.identifier.value.to_lowercase());
            }
            TableReference::Join { .. } => self.joins += 1,
            _ => {}
        }
        walk_table_reference(self, reference)
    }
}

fn summarize(src: &str, statement: &Statement) -> Result<Json, Box<dyn Error>> {
    let mut walk = Walk { src, tables: BTreeSet::new(), functions: BTreeSet::new(), joins: 0, literals: Vec::new() };
    let _ = walk.visit_statement(statement);
    walk.literals.sort();
    let literals: Vec<Json> = walk.literals.iter().map(|(kind, text)| json!([kind, text])).collect();
    match statement {
        Statement::Select(select) => Ok(json!({
            "kind": "select", "tables": walk.tables.iter().collect::<Vec<_>>(),
            "select_items": select.select_exprs.len(), "joins": walk.joins,
            "where": select.where_.is_some(),
            "group_by": select.group_by.as_ref().map_or(0, |(_, keys)| keys.len()),
            "order_by": select.order_by.as_ref().map_or(0, |(_, keys)| keys.len()),
            "functions": walk.functions.iter().collect::<Vec<_>>(), "literals": literals,
        })),
        Statement::InsertReplace(insert) => {
            let (_, rows) = insert.values.as_ref().ok_or("INSERT body is not VALUES")?;
            Ok(json!({"kind": "insert", "tables": [insert.table.identifier.value.to_lowercase()],
                      "columns": insert.columns.len(), "rows": rows.len(), "literals": literals}))
        }
        other => Ok(json!({"kind": format!("{other:?}").split(['(', ' ', '{']).next().unwrap_or("").to_lowercase()})),
    }
}

pub fn parse(data: &[u8]) -> Result<String, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let options = ParseOptions::new();
    let mut issues = Issues::new(text);
    let statements = parse_statements(text, &mut issues, &options);
    // The parser recovers from errors; any error-level issue rejects the input.
    if issues.get().iter().any(|issue| matches!(issue.level, Level::Error)) {
        return Err(format!("parse errors: {issues}").into());
    }
    let summaries = statements.iter().map(|statement| summarize(text, statement)).collect::<Result<Vec<_>, _>>()?;
    Ok(serde_json::to_string(&json!({"statement_count": summaries.len(), "statements": summaries}))?)
}
