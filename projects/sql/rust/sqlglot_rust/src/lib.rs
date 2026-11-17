//! sqlglot-rust (sqlglot-inspired Rust tokenizer and parser, ANSI dialect) over local SQL text.
//! The summary is read from its AST only: typed SelectStatement/InsertStatement fields and the
//! crate's Expr::walk for function calls and literals.
use std::collections::BTreeSet;
use std::error::Error;

use serde_json::{json, Value as Json};
use sqlglot_rust::ast::{Expr, InsertSource, SelectItem, SelectStatement, Statement, TableSource};
use sqlglot_rust::parser::parse_statements;
use sqlglot_rust::Dialect;

#[derive(Default)]
struct Walk {
    tables: BTreeSet<String>,
    functions: BTreeSet<String>,
    literals: Vec<(String, String)>,
}

impl Walk {
    fn expr(&mut self, root: &Expr) {
        root.walk(&mut |node| {
            match node {
                Expr::Function { name, .. } => {
                    self.functions.insert(name.to_lowercase());
                }
                // Typed functions (Count, Sum, ...) carry the function in their variant name.
                Expr::TypedFunction { func, .. } => {
                    let name = format!("{func:?}");
                    let name = name.split([' ', '(', '{']).next().unwrap_or("").to_lowercase();
                    self.functions.insert(name);
                }
                Expr::Number(text) => self.literals.push(("number".into(), text.clone())),
                Expr::StringLiteral(text) => self.literals.push(("string".into(), text.clone())),
                _ => {}
            }
            true
        });
    }

    fn source(&mut self, source: &TableSource) {
        if let TableSource::Table(table) = source {
            self.tables.insert(table.name.to_lowercase());
        }
    }

    fn literals(&mut self) -> Vec<Json> {
        self.literals.sort();
        self.literals.iter().map(|(kind, text)| json!([kind, text])).collect()
    }
}

fn select_summary(select: &SelectStatement) -> Json {
    let mut walk = Walk::default();
    for item in &select.columns {
        if let SelectItem::Expr { expr, .. } = item {
            walk.expr(expr);
        }
    }
    if let Some(from) = &select.from {
        walk.source(&from.source);
    }
    for join in &select.joins {
        walk.source(&join.table);
        if let Some(on) = &join.on {
            walk.expr(on);
        }
    }
    select.where_clause.iter().for_each(|expr| walk.expr(expr));
    select.group_by.iter().for_each(|expr| walk.expr(expr));
    select.order_by.iter().for_each(|key| walk.expr(&key.expr));
    json!({
        "kind": "select", "tables": walk.tables.iter().collect::<Vec<_>>(),
        "select_items": select.columns.len(), "joins": select.joins.len(),
        "where": select.where_clause.is_some(), "group_by": select.group_by.len(),
        "order_by": select.order_by.len(),
        "functions": walk.functions.iter().collect::<Vec<_>>(), "literals": walk.literals(),
    })
}

fn summarize(statement: &Statement) -> Result<Json, Box<dyn Error>> {
    match statement {
        Statement::Select(select) => Ok(select_summary(select)),
        Statement::Insert(insert) => {
            let InsertSource::Values(rows) = &insert.source else {
                return Err("INSERT body is not VALUES".into());
            };
            let mut walk = Walk::default();
            rows.iter().flatten().for_each(|expr| walk.expr(expr));
            Ok(json!({"kind": "insert", "tables": [insert.table.name.to_lowercase()],
                      "columns": insert.columns.len(), "rows": rows.len(),
                      "literals": walk.literals()}))
        }
        other => Ok(json!({"kind": format!("{other:?}").split(['(', ' ', '{']).next().unwrap_or("").to_lowercase()})),
    }
}

pub fn parse(data: &[u8]) -> Result<String, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let statements = parse_statements(text, Dialect::Ansi)?;
    let summaries = statements.iter().map(summarize).collect::<Result<Vec<_>, _>>()?;
    Ok(serde_json::to_string(&json!({"statement_count": summaries.len(), "statements": summaries}))?)
}
