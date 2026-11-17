//! sqlparser-rs (GenericDialect) over local SQL text; the summary is read from its AST only.
use std::collections::BTreeSet;
use std::error::Error;
use std::ops::ControlFlow;

use serde_json::{json, Value as Json};
use sqlparser::ast::{
    visit_expressions, visit_relations, Expr, GroupByExpr, OrderByKind, Query, SetExpr,
    Statement, TableObject, Value,
};
use sqlparser::dialect::GenericDialect;
use sqlparser::parser::Parser;

fn tables<V: sqlparser::ast::Visit>(node: &V) -> Vec<String> {
    let mut names = BTreeSet::new();
    let _ = visit_relations(node, |name| {
        if let Some(last) = name.0.last() {
            names.insert(last.to_string().to_lowercase());
        }
        ControlFlow::<()>::Continue(())
    });
    names.into_iter().collect()
}

fn functions_and_literals<V: sqlparser::ast::Visit>(node: &V) -> (Vec<String>, Vec<Json>) {
    let mut functions = BTreeSet::new();
    let mut literals: Vec<(String, String)> = Vec::new();
    let _ = visit_expressions(node, |expr| {
        match expr {
            Expr::Function(function) => {
                if let Some(last) = function.name.0.last() {
                    functions.insert(last.to_string().to_lowercase());
                }
            }
            Expr::Value(value) => match &value.value {
                Value::Number(text, _) => literals.push(("number".into(), text.to_string())),
                Value::SingleQuotedString(text) => literals.push(("string".into(), text.clone())),
                _ => {}
            },
            _ => {}
        }
        ControlFlow::<()>::Continue(())
    });
    literals.sort();
    (functions.into_iter().collect(),
     literals.into_iter().map(|(kind, text)| json!([kind, text])).collect())
}

fn select_summary(query: &Query) -> Result<Json, Box<dyn Error>> {
    let SetExpr::Select(select) = query.body.as_ref() else {
        return Err("query body is not a SELECT".into());
    };
    let joins: usize = select.from.iter().map(|table| table.joins.len()).sum();
    let group_by = match &select.group_by {
        GroupByExpr::Expressions(expressions, _) => expressions.len(),
        GroupByExpr::All(_) => 0,
    };
    let order_by = match query.order_by.as_ref().map(|order| &order.kind) {
        Some(OrderByKind::Expressions(expressions)) => expressions.len(),
        _ => 0,
    };
    let (functions, literals) = functions_and_literals(query);
    Ok(json!({
        "kind": "select", "tables": tables(query), "select_items": select.projection.len(),
        "joins": joins, "where": select.selection.is_some(), "group_by": group_by,
        "order_by": order_by, "functions": functions, "literals": literals,
    }))
}

fn summarize(statement: &Statement) -> Result<Json, Box<dyn Error>> {
    match statement {
        Statement::Query(query) => select_summary(query),
        Statement::Insert(insert) => {
            let TableObject::TableName(name) = &insert.table else {
                return Err("INSERT target is not a table name".into());
            };
            let table = name.0.last().ok_or("empty table name")?.to_string().to_lowercase();
            let rows = match insert.source.as_ref().map(|query| query.body.as_ref()) {
                Some(SetExpr::Values(values)) => values.rows.len(),
                _ => 0,
            };
            let (_, literals) = functions_and_literals(statement);
            Ok(json!({"kind": "insert", "tables": [table], "columns": insert.columns.len(),
                      "rows": rows, "literals": literals}))
        }
        other => Ok(json!({"kind": format!("{other:?}").split(['(', ' ', '{']).next().unwrap_or("").to_lowercase()})),
    }
}

pub fn parse(data: &[u8]) -> Result<String, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let statements = Parser::parse_sql(&GenericDialect {}, text)?;
    let summaries = statements.iter().map(summarize).collect::<Result<Vec<_>, _>>()?;
    Ok(serde_json::to_string(&json!({"statement_count": summaries.len(), "statements": summaries}))?)
}
