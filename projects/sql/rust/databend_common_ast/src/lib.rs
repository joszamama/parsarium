//! databend-common-ast (Databend's logos tokenizer and nom parser, default PostgreSQL dialect)
//! over local SQL text. The summary is read from its AST only: typed Query/SelectStmt/InsertStmt
//! fields and the crate's derive-visitor Drive walk for table references, calls and literals.
use std::collections::BTreeSet;
use std::error::Error;

use databend_common_ast::ast::{
    Expr, GroupBy, InsertSource, Literal, SetExpr, Statement, TableReference,
};
use databend_common_ast::parser::{parse_sql, tokenize_sql, Dialect};
use derive_visitor::{Drive, Visitor};
use serde_json::{json, Value as Json};

#[derive(Visitor)]
#[visitor(Expr(enter), TableReference(enter))]
struct Walk<'s> {
    src: &'s str,
    tables: BTreeSet<String>,
    functions: BTreeSet<String>,
    joins: usize,
    literals: Vec<(String, String)>,
}

impl Walk<'_> {
    fn enter_expr(&mut self, expr: &Expr) {
        match expr {
            Expr::FunctionCall { func, .. } => {
                self.functions.insert(func.name.name.to_lowercase());
            }
            // COUNT(*) has its own node in this AST.
            Expr::CountAll { .. } => {
                self.functions.insert("count".into());
            }
            Expr::Literal { span, value } => match value {
                // Numbers are reported as the source text of their span.
                Literal::UInt64(_) | Literal::Float64(_) | Literal::Decimal256 { .. } => {
                    let range = span.as_ref().map(|range| range.start as usize..range.end as usize);
                    let text = range.and_then(|range| self.src.get(range)).unwrap_or("");
                    self.literals.push(("number".into(), text.to_string()));
                }
                Literal::String(text) => self.literals.push(("string".into(), text.clone())),
                _ => {}
            },
            _ => {}
        }
    }

    fn enter_table_reference(&mut self, reference: &TableReference) {
        match reference {
            TableReference::Table { table, .. } => {
                self.tables.insert(table.table.name.to_lowercase());
            }
            TableReference::Join { .. } => self.joins += 1,
            _ => {}
        }
    }
}

fn summarize(src: &str, statement: &Statement) -> Result<Json, Box<dyn Error>> {
    let mut walk = Walk { src, tables: BTreeSet::new(), functions: BTreeSet::new(), joins: 0, literals: Vec::new() };
    statement.drive(&mut walk);
    walk.literals.sort();
    let literals: Vec<Json> = walk.literals.iter().map(|(kind, text)| json!([kind, text])).collect();
    match statement {
        Statement::Query(query) => {
            let SetExpr::Select(select) = &query.body else {
                return Err("query body is not a SELECT".into());
            };
            let group_by = match &select.group_by {
                Some(GroupBy::Normal(keys)) => keys.len(),
                None => 0,
                Some(_) => return Err("GROUP BY form outside the summary".into()),
            };
            Ok(json!({
                "kind": "select", "tables": walk.tables.iter().collect::<Vec<_>>(),
                "select_items": select.select_list.len(), "joins": walk.joins,
                "where": select.selection.is_some(), "group_by": group_by,
                "order_by": query.order_by.len(),
                "functions": walk.functions.iter().collect::<Vec<_>>(), "literals": literals,
            }))
        }
        Statement::Insert(insert) => {
            let InsertSource::Values { rows } = &insert.source else {
                return Err("INSERT body is not parsed VALUES".into());
            };
            Ok(json!({"kind": "insert", "tables": [insert.table.table.name.to_lowercase()],
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
    let tokens = tokenize_sql(text)?;
    // parse_sql takes one statement; the controls hold one statement each.
    let (statement, _format) = parse_sql(&tokens, Dialect::PostgreSQL)?;
    let summary = summarize(text, &statement)?;
    Ok(serde_json::to_string(&json!({"statement_count": 1, "statements": [summary]}))?)
}
