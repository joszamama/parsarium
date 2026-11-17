//! typedpg_pg_query (Rust bindings to its own vendored libpg_query, PostgreSQL grammar) over
//! local SQL text. The summary is read from the protobuf parse tree that
//! typedpg_pg_query::parse returns: typed SelectStmt/InsertStmt fields for clause counts, and
//! the crate's own breadth-first node walk (NodeEnum::nodes) for RangeVar, FuncCall, JoinExpr
//! and A_Const.
use std::collections::BTreeSet;
use std::error::Error;

use serde_json::{json, Value as Json};
use typedpg_pg_query::protobuf::a_const::Val;
use typedpg_pg_query::protobuf::{InsertStmt, SelectStmt};
use typedpg_pg_query::{NodeEnum, NodeRef};

#[derive(Default)]
struct Walk {
    tables: BTreeSet<String>,
    functions: BTreeSet<String>,
    joins: usize,
    literals: Vec<(String, String)>,
}

impl Walk {
    fn of(node: &NodeEnum) -> Self {
        let mut walk = Walk::default();
        for (child, _depth) in node.nodes() {
            match child {
                NodeRef::RangeVar(range) => {
                    walk.tables.insert(range.relname.to_lowercase());
                }
                NodeRef::FuncCall(call) => {
                    let last = call.funcname.last().and_then(|part| match part.node.as_ref() {
                        Some(NodeEnum::String(text)) => Some(text.sval.to_lowercase()),
                        _ => None,
                    });
                    if let Some(name) = last {
                        walk.functions.insert(name);
                    }
                }
                NodeRef::JoinExpr(_) => walk.joins += 1,
                NodeRef::AConst(constant) => match constant.val.as_ref() {
                    Some(Val::Ival(number)) => {
                        walk.literals.push(("number".into(), number.ival.to_string()));
                    }
                    Some(Val::Fval(number)) => {
                        walk.literals.push(("number".into(), number.fval.clone()));
                    }
                    Some(Val::Sval(text)) => {
                        walk.literals.push(("string".into(), text.sval.clone()));
                    }
                    _ => {}
                },
                _ => {}
            }
        }
        walk
    }

    fn literals(&mut self) -> Vec<Json> {
        self.literals.sort();
        self.literals.iter().map(|(kind, text)| json!([kind, text])).collect()
    }
}

fn select_summary(select: &SelectStmt, node: &NodeEnum) -> Result<Json, Box<dyn Error>> {
    if select.larg.is_some() || select.rarg.is_some() || !select.values_lists.is_empty() {
        return Err("set operation or VALUES is outside the summary".into());
    }
    let mut walk = Walk::of(node);
    Ok(json!({
        "kind": "select", "tables": walk.tables.iter().collect::<Vec<_>>(),
        "select_items": select.target_list.len(), "joins": walk.joins,
        "where": select.where_clause.is_some(), "group_by": select.group_clause.len(),
        "order_by": select.sort_clause.len(),
        "functions": walk.functions.iter().collect::<Vec<_>>(), "literals": walk.literals(),
    }))
}

fn insert_summary(insert: &InsertStmt, node: &NodeEnum) -> Result<Json, Box<dyn Error>> {
    let relation = insert.relation.as_ref().ok_or("INSERT without a target relation")?;
    let rows = match insert.select_stmt.as_ref().and_then(|body| body.node.as_ref()) {
        Some(NodeEnum::SelectStmt(select)) => select.values_lists.len(),
        _ => return Err("INSERT body is not VALUES".into()),
    };
    let mut walk = Walk::of(node);
    Ok(json!({"kind": "insert", "tables": [relation.relname.to_lowercase()],
              "columns": insert.cols.len(), "rows": rows, "literals": walk.literals()}))
}

pub fn parse(data: &[u8]) -> Result<String, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let result = typedpg_pg_query::parse(text)?;
    let mut summaries = Vec::new();
    for raw in &result.protobuf.stmts {
        let node = raw.stmt.as_ref().and_then(|stmt| stmt.node.as_ref()).ok_or("empty statement")?;
        summaries.push(match node {
            NodeEnum::SelectStmt(select) => select_summary(select, node)?,
            NodeEnum::InsertStmt(insert) => insert_summary(insert, node)?,
            other => json!({"kind": format!("{other:?}").split(['(', ' ', '{']).next().unwrap_or("").to_lowercase()}),
        });
    }
    Ok(serde_json::to_string(&json!({"statement_count": summaries.len(), "statements": summaries}))?)
}
