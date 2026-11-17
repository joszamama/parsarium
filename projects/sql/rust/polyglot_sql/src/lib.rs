//! polyglot-sql (sqlglot-style Rust tokenizer and parser, Generic dialect) over local SQL text.
//! The summary is read from its Expression AST only: typed Select/Insert fields for clause
//! counts and the crate's DFS traversal for tables, function calls and literals.
use std::collections::BTreeSet;
use std::error::Error;

use polyglot_sql::expressions::{Expression, Literal};
use polyglot_sql::traversal::{is_aggregate, ExpressionWalk};
use polyglot_sql::DialectType;
use serde_json::{json, Value as Json};

#[derive(Default)]
struct Walk {
    tables: BTreeSet<String>,
    functions: BTreeSet<String>,
    literals: Vec<(String, String)>,
}

impl Walk {
    fn visit(&mut self, root: &Expression) {
        for node in root.dfs() {
            match node {
                Expression::Table(table) => {
                    self.tables.insert(table.name.name.to_lowercase());
                }
                Expression::Function(function) => {
                    self.functions.insert(function.name.to_lowercase());
                }
                Expression::AggregateFunction(function) => {
                    self.functions.insert(function.name.to_lowercase());
                }
                // Typed aggregate nodes (Count, Sum, ...) carry the function in their variant.
                other if is_aggregate(other) => {
                    self.functions.insert(other.variant_name().to_string());
                }
                Expression::Literal(literal) => match literal.as_ref() {
                    Literal::Number(text) => self.literals.push(("number".into(), text.clone())),
                    Literal::String(text) => self.literals.push(("string".into(), text.clone())),
                    _ => {}
                },
                _ => {}
            }
        }
    }

    fn literals(&mut self) -> Vec<Json> {
        self.literals.sort();
        self.literals.iter().map(|(kind, text)| json!([kind, text])).collect()
    }
}

fn summarize(statement: &Expression) -> Result<Json, Box<dyn Error>> {
    match statement {
        Expression::Select(select) => {
            let mut walk = Walk::default();
            walk.visit(statement);
            Ok(json!({
                "kind": "select", "tables": walk.tables.iter().collect::<Vec<_>>(),
                "select_items": select.expressions.len(), "joins": select.joins.len(),
                "where": select.where_clause.is_some(),
                "group_by": select.group_by.as_ref().map_or(0, |group| group.expressions.len()),
                "order_by": select.order_by.as_ref().map_or(0, |order| order.expressions.len()),
                "functions": walk.functions.iter().collect::<Vec<_>>(), "literals": walk.literals(),
            }))
        }
        Expression::Insert(insert) => {
            if insert.query.is_some() || insert.values.is_empty() {
                return Err("INSERT body is not VALUES".into());
            }
            let mut walk = Walk::default();
            walk.visit(statement);
            Ok(json!({"kind": "insert", "tables": [insert.table.name.name.to_lowercase()],
                      "columns": insert.columns.len(), "rows": insert.values.len(),
                      "literals": walk.literals()}))
        }
        other => Ok(json!({"kind": other.variant_name()})),
    }
}

pub fn parse(data: &[u8]) -> Result<String, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let statements = polyglot_sql::parse(text, DialectType::Generic)?;
    let summaries = statements.iter().map(summarize).collect::<Result<Vec<_>, _>>()?;
    Ok(serde_json::to_string(&json!({"statement_count": summaries.len(), "statements": summaries}))?)
}
