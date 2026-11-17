//! pg_query (Rust bindings to libpg_query, PostgreSQL grammar) over local SQL text.
//! The summary is read from the protobuf parse tree that pg_query::parse returns:
//! typed SelectStmt/InsertStmt fields for clause counts, and a walk of the same tree
//! (serialized through its own serde derive) for RangeVar, FuncCall, JoinExpr and A_Const.
use std::collections::BTreeSet;
use std::error::Error;

use pg_query::protobuf::{InsertStmt, SelectStmt};
use pg_query::NodeEnum;
use serde_json::{json, Value as Json};

#[derive(Default)]
struct Walk {
    tables: BTreeSet<String>,
    functions: BTreeSet<String>,
    joins: usize,
    literals: Vec<(String, String)>,
}

impl Walk {
    fn visit(&mut self, value: &Json) {
        match value {
            Json::Object(map) => {
                for (key, child) in map {
                    match (key.as_str(), child) {
                        ("RangeVar", Json::Object(range)) => {
                            if let Some(Json::String(name)) = range.get("relname") {
                                self.tables.insert(name.to_lowercase());
                            }
                        }
                        ("FuncCall", Json::Object(call)) => {
                            let last = call.get("funcname").and_then(Json::as_array)
                                .and_then(|parts| parts.last())
                                .and_then(|part| part.pointer("/node/String/sval"))
                                .and_then(Json::as_str);
                            if let Some(name) = last {
                                self.functions.insert(name.to_lowercase());
                            }
                        }
                        ("JoinExpr", Json::Object(_)) => self.joins += 1,
                        ("AConst", Json::Object(constant)) => {
                            match constant.get("val").and_then(Json::as_object)
                                .and_then(|val| val.iter().next()) {
                                Some((kind, inner)) if kind == "Ival" => {
                                    let number = inner.get("ival").and_then(Json::as_i64).unwrap_or(0);
                                    self.literals.push(("number".into(), number.to_string()));
                                }
                                Some((kind, inner)) if kind == "Fval" => {
                                    let text = inner.get("fval").and_then(Json::as_str).unwrap_or("");
                                    self.literals.push(("number".into(), text.to_string()));
                                }
                                Some((kind, inner)) if kind == "Sval" => {
                                    let text = inner.get("sval").and_then(Json::as_str).unwrap_or("");
                                    self.literals.push(("string".into(), text.to_string()));
                                }
                                _ => {}
                            }
                        }
                        _ => {}
                    }
                    self.visit(child);
                }
            }
            Json::Array(items) => items.iter().for_each(|item| self.visit(item)),
            _ => {}
        }
    }

    fn literals(&mut self) -> Vec<Json> {
        self.literals.sort();
        self.literals.iter().map(|(kind, text)| json!([kind, text])).collect()
    }
}

fn select_summary(select: &SelectStmt, tree: &Json) -> Result<Json, Box<dyn Error>> {
    if select.larg.is_some() || select.rarg.is_some() || !select.values_lists.is_empty() {
        return Err("set operation or VALUES is outside the summary".into());
    }
    let mut walk = Walk::default();
    walk.visit(tree);
    Ok(json!({
        "kind": "select", "tables": walk.tables.iter().collect::<Vec<_>>(),
        "select_items": select.target_list.len(), "joins": walk.joins,
        "where": select.where_clause.is_some(), "group_by": select.group_clause.len(),
        "order_by": select.sort_clause.len(),
        "functions": walk.functions.iter().collect::<Vec<_>>(), "literals": walk.literals(),
    }))
}

fn insert_summary(insert: &InsertStmt, tree: &Json) -> Result<Json, Box<dyn Error>> {
    let relation = insert.relation.as_ref().ok_or("INSERT without a target relation")?;
    let rows = match insert.select_stmt.as_ref().and_then(|node| node.node.as_ref()) {
        Some(NodeEnum::SelectStmt(select)) => select.values_lists.len(),
        _ => return Err("INSERT body is not VALUES".into()),
    };
    let mut walk = Walk::default();
    walk.visit(tree);
    Ok(json!({"kind": "insert", "tables": [relation.relname.to_lowercase()],
              "columns": insert.cols.len(), "rows": rows, "literals": walk.literals()}))
}

pub fn parse(data: &[u8]) -> Result<String, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let result = pg_query::parse(text, pg_query::ParserOptions::DEFAULT)?;
    let mut summaries = Vec::new();
    for raw in &result.protobuf.stmts {
        let node = raw.stmt.as_ref().and_then(|stmt| stmt.node.as_ref()).ok_or("empty statement")?;
        let tree = serde_json::to_value(node)?;
        summaries.push(match node {
            NodeEnum::SelectStmt(select) => select_summary(select, &tree)?,
            NodeEnum::InsertStmt(insert) => insert_summary(insert, &tree)?,
            other => json!({"kind": format!("{other:?}").split(['(', ' ', '{']).next().unwrap_or("").to_lowercase()}),
        });
    }
    Ok(serde_json::to_string(&json!({"statement_count": summaries.len(), "statements": summaries}))?)
}
