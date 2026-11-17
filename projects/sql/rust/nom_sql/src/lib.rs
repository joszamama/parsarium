//! nom-sql (nom-combinator MySQL-subset parser) over local SQL bytes; the summary is read from
//! its AST only (SelectStatement, JoinClause, ConditionExpression, InsertStatement).
use std::collections::BTreeSet;
use std::error::Error;

use nom_sql::{
    Column, ConditionBase, ConditionExpression, FieldDefinitionExpression, FunctionExpression,
    JoinConstraint, JoinRightSide, Literal, SqlQuery,
};
use serde_json::{json, Value as Json};

#[derive(Default)]
struct Walk {
    tables: BTreeSet<String>,
    functions: BTreeSet<String>,
    literals: Vec<(String, String)>,
}

impl Walk {
    fn column(&mut self, column: &Column) {
        if let Some(function) = &column.function {
            let name = match function.as_ref() {
                FunctionExpression::CountStar | FunctionExpression::Count(..) => "count",
                FunctionExpression::Sum(..) => "sum",
                FunctionExpression::Avg(..) => "avg",
                FunctionExpression::Max(..) => "max",
                FunctionExpression::Min(..) => "min",
                FunctionExpression::GroupConcat(..) => "group_concat",
            };
            self.functions.insert(name.into());
        }
    }

    fn literal(&mut self, literal: &Literal) {
        match literal {
            Literal::Integer(value) => self.literals.push(("number".into(), value.to_string())),
            Literal::UnsignedInteger(value) => self.literals.push(("number".into(), value.to_string())),
            // FixedPoint keeps the integral part and the fractional digits as integers.
            Literal::FixedPoint(real) => {
                self.literals.push(("number".into(), format!("{}.{}", real.integral, real.fractional)));
            }
            Literal::String(text) => self.literals.push(("string".into(), text.clone())),
            _ => {}
        }
    }

    fn condition(&mut self, condition: &ConditionExpression) {
        match condition {
            ConditionExpression::ComparisonOp(tree) | ConditionExpression::LogicalOp(tree) => {
                self.condition(&tree.left);
                self.condition(&tree.right);
            }
            ConditionExpression::NegationOp(inner) | ConditionExpression::Bracketed(inner) => self.condition(inner),
            ConditionExpression::Base(ConditionBase::Field(column)) => self.column(column),
            ConditionExpression::Base(ConditionBase::Literal(literal)) => self.literal(literal),
            ConditionExpression::Base(ConditionBase::LiteralList(literals)) => {
                literals.iter().for_each(|literal| self.literal(literal));
            }
            _ => {}
        }
    }

    fn literals(&mut self) -> Vec<Json> {
        self.literals.sort();
        self.literals.iter().map(|(kind, text)| json!([kind, text])).collect()
    }
}

fn summarize(query: &SqlQuery) -> Result<Json, Box<dyn Error>> {
    match query {
        SqlQuery::Select(select) => {
            let mut walk = Walk::default();
            for table in &select.tables {
                walk.tables.insert(table.name.to_lowercase());
            }
            for field in &select.fields {
                if let FieldDefinitionExpression::Col(column) = field {
                    walk.column(column);
                }
            }
            for join in &select.join {
                if let JoinRightSide::Table(table) = &join.right {
                    walk.tables.insert(table.name.to_lowercase());
                }
                if let JoinConstraint::On(condition) = &join.constraint {
                    walk.condition(condition);
                }
            }
            select.where_clause.iter().for_each(|condition| walk.condition(condition));
            Ok(json!({
                "kind": "select", "tables": walk.tables.iter().collect::<Vec<_>>(),
                "select_items": select.fields.len(), "joins": select.join.len(),
                "where": select.where_clause.is_some(),
                "group_by": select.group_by.as_ref().map_or(0, |group| group.columns.len()),
                "order_by": select.order.as_ref().map_or(0, |order| order.columns.len()),
                "functions": walk.functions.iter().collect::<Vec<_>>(), "literals": walk.literals(),
            }))
        }
        SqlQuery::Insert(insert) => {
            let mut walk = Walk::default();
            insert.data.iter().flatten().for_each(|literal| walk.literal(literal));
            Ok(json!({"kind": "insert", "tables": [insert.table.name.to_lowercase()],
                      "columns": insert.fields.as_ref().map_or(0, |fields| fields.len()),
                      "rows": insert.data.len(), "literals": walk.literals()}))
        }
        other => Ok(json!({"kind": format!("{other:?}").split(['(', ' ', '{']).next().unwrap_or("").to_lowercase()})),
    }
}

pub fn parse(data: &[u8]) -> Result<String, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    // parse_query_bytes parses one statement; the controls hold one statement each.
    let query = nom_sql::parse_query_bytes(data)?;
    let summary = summarize(&query)?;
    Ok(serde_json::to_string(&json!({"statement_count": 1, "statements": [summary]}))?)
}
