//! spg-sql (SPG's hand-written PostgreSQL-dialect lexer and parser) over local SQL text; the
//! summary is read from its AST only (SelectStatement, FromClause, InsertStatement and Expr).
use std::collections::BTreeSet;
use std::error::Error;

use serde_json::{json, Value as Json};
use spg_sql::ast::{Expr, Literal, SelectItem, SelectStatement, Statement, TableRef};
use spg_sql::parser::parse_statement;

#[derive(Default)]
struct Walk {
    tables: BTreeSet<String>,
    functions: BTreeSet<String>,
    literals: Vec<(String, String)>,
}

fn decimal(unscaled: i128, scale: u16) -> String {
    let digits = unscaled.unsigned_abs().to_string();
    let scale = scale as usize;
    let sign = if unscaled < 0 { "-" } else { "" };
    if scale == 0 {
        return format!("{sign}{digits}");
    }
    let padded = format!("{digits:0>width$}", width = scale + 1);
    let (whole, fraction) = padded.split_at(padded.len() - scale);
    format!("{sign}{whole}.{fraction}")
}

impl Walk {
    fn expr(&mut self, expr: &Expr) {
        match expr {
            Expr::Binary { lhs, rhs, .. } => {
                self.expr(lhs);
                self.expr(rhs);
            }
            Expr::Unary { expr, .. } => self.expr(expr),
            Expr::FunctionCall { name, args, .. } => {
                // The parser names COUNT(*) `count_star`; it is reported as `count`.
                let name = name.to_lowercase();
                self.functions.insert(if name == "count_star" { "count".into() } else { name });
                args.iter().for_each(|arg| self.expr(arg));
            }
            Expr::InList { .. } | Expr::ScalarSubquery(_) | Expr::Exists { .. } => {}
            Expr::Literal(literal) => match literal {
                Literal::Integer(value) => self.literals.push(("number".into(), value.to_string())),
                Literal::Numeric { unscaled, scale } => {
                    self.literals.push(("number".into(), decimal(*unscaled, *scale)));
                }
                Literal::String(text) => self.literals.push(("string".into(), text.clone())),
                _ => {}
            },
            _ => {}
        }
    }

    fn table(&mut self, table: &TableRef) {
        self.tables.insert(table.name.to_lowercase());
    }

    fn literals(&mut self) -> Vec<Json> {
        self.literals.sort();
        self.literals.iter().map(|(kind, text)| json!([kind, text])).collect()
    }
}

fn select_summary(select: &SelectStatement) -> Result<Json, Box<dyn Error>> {
    if !select.unions.is_empty() {
        return Err("set operation is outside the summary".into());
    }
    let mut walk = Walk::default();
    for item in &select.items {
        if let SelectItem::Expr { expr, .. } = item {
            walk.expr(expr);
        }
    }
    let mut joins = 0;
    if let Some(from) = &select.from {
        walk.table(&from.primary);
        for join in &from.joins {
            joins += 1;
            walk.table(&join.table);
            if let Some(on) = &join.on {
                walk.expr(on);
            }
        }
    }
    select.where_.iter().for_each(|expr| walk.expr(expr));
    select.group_by.iter().flatten().for_each(|expr| walk.expr(expr));
    select.order_by.iter().for_each(|key| walk.expr(&key.expr));
    Ok(json!({
        "kind": "select", "tables": walk.tables.iter().collect::<Vec<_>>(),
        "select_items": select.items.len(), "joins": joins, "where": select.where_.is_some(),
        "group_by": select.group_by.as_ref().map_or(0, |keys| keys.len()),
        "order_by": select.order_by.len(),
        "functions": walk.functions.iter().collect::<Vec<_>>(), "literals": walk.literals(),
    }))
}

fn summarize(statement: &Statement) -> Result<Json, Box<dyn Error>> {
    match statement {
        Statement::Select(select) => select_summary(select),
        Statement::Insert(insert) => {
            if insert.select_source.is_some() {
                return Err("INSERT body is not VALUES".into());
            }
            let mut walk = Walk::default();
            insert.rows.iter().flatten().for_each(|expr| walk.expr(expr));
            Ok(json!({"kind": "insert", "tables": [insert.table.to_lowercase()],
                      "columns": insert.columns.as_ref().map_or(0, |columns| columns.len()),
                      "rows": insert.rows.len(), "literals": walk.literals()}))
        }
        other => Ok(json!({"kind": format!("{other:?}").split(['(', ' ', '{']).next().unwrap_or("").to_lowercase()})),
    }
}

pub fn parse(data: &[u8]) -> Result<String, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    // parse_statement takes exactly one statement and an optional trailing `;`.
    let statement = parse_statement(text).map_err(|error| format!("{error:?}"))?;
    let summary = summarize(&statement)?;
    Ok(serde_json::to_string(&json!({"statement_count": 1, "statements": [summary]}))?)
}
