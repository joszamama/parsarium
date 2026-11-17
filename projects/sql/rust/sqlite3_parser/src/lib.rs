//! sqlite3-parser (lemon-rs port of SQLite's Lemon grammar) over local SQL text; the summary is read from its AST only.
use std::collections::BTreeSet;
use std::error::Error;

use serde_json::{json, Value as Json};
use sqlite3_parser::ast::{
    Cmd, Expr, FromClause, InsertBody, JoinConstraint, Literal, OneSelect, ResultColumn, Select,
    SelectTable, Stmt,
};
use sqlite3_parser::lexer::sql::Parser;
use sqlite3_parser::{Bump, FallibleIterator};

#[derive(Default)]
struct Walk {
    tables: BTreeSet<String>,
    functions: BTreeSet<String>,
    literals: Vec<(String, String)>,
}

impl Walk {
    fn expr(&mut self, expr: &Expr) {
        match expr {
            Expr::Between { lhs, start, end, .. } => {
                self.expr(lhs);
                self.expr(start);
                self.expr(end);
            }
            Expr::Binary(lhs, _, rhs) => {
                self.expr(lhs);
                self.expr(rhs);
            }
            Expr::FunctionCall { name, args, .. } => {
                self.functions.insert(name.0.to_lowercase());
                for arg in args.iter().flat_map(|args| args.iter()) {
                    self.expr(arg);
                }
            }
            Expr::FunctionCallStar { name, .. } => {
                self.functions.insert(name.0.to_lowercase());
            }
            Expr::InList { lhs, rhs, .. } => {
                self.expr(lhs);
                for item in rhs.iter().flat_map(|rhs| rhs.iter()) {
                    self.expr(item);
                }
            }
            Expr::InSelect { lhs, rhs, .. } => {
                self.expr(lhs);
                self.select(rhs);
            }
            Expr::Exists(select) | Expr::Subquery(select) => self.select(select),
            Expr::IsNull(inner) | Expr::NotNull(inner) | Expr::Unary(_, inner) => self.expr(inner),
            Expr::Parenthesized(items) => items.iter().for_each(|item| self.expr(item)),
            Expr::Literal(Literal::Numeric(text)) => {
                self.literals.push(("number".into(), (*text).to_string()));
            }
            Expr::Literal(Literal::String(text)) => {
                // The AST keeps the quoted token; strip the quotes and undo '' escapes.
                let inner = text.strip_prefix('\'').and_then(|t| t.strip_suffix('\'')).unwrap_or(text);
                self.literals.push(("string".into(), inner.replace("''", "'")));
            }
            _ => {}
        }
    }

    fn from(&mut self, from: &FromClause) {
        if let Some(table) = from.select {
            self.table(table);
        }
        for joined in from.joins.iter().flat_map(|joins| joins.iter()) {
            self.table(&joined.table);
            if let Some(JoinConstraint::On(expr)) = &joined.constraint {
                self.expr(expr);
            }
        }
    }

    fn table(&mut self, table: &SelectTable) {
        match table {
            SelectTable::Table(name, _, _) => {
                self.tables.insert(name.name.0.to_lowercase());
            }
            SelectTable::Select(select, _) => self.select(select),
            SelectTable::Sub(from, _) => self.from(from),
            SelectTable::TableCall(_, args, _) => {
                for arg in args.iter().flat_map(|args| args.iter()) {
                    self.expr(arg);
                }
            }
        }
    }

    fn select(&mut self, select: &Select) {
        match &select.body.select {
            OneSelect::Select { columns, from, where_clause, group_by, having, .. } => {
                for column in columns.iter() {
                    if let ResultColumn::Expr(expr, _) = column {
                        self.expr(expr);
                    }
                }
                if let Some(from) = from {
                    self.from(from);
                }
                where_clause.iter().for_each(|expr| self.expr(expr));
                group_by.iter().flat_map(|keys| keys.iter()).for_each(|expr| self.expr(expr));
                having.iter().for_each(|expr| self.expr(expr));
            }
            OneSelect::Values(rows) => rows.iter().flat_map(|row| row.iter()).for_each(|expr| self.expr(expr)),
        }
        select.order_by.iter().flat_map(|keys| keys.iter()).for_each(|key| self.expr(&key.expr));
    }

    fn literals(&mut self) -> Vec<Json> {
        self.literals.sort();
        self.literals.iter().map(|(kind, text)| json!([kind, text])).collect()
    }
}

fn select_summary(select: &Select) -> Result<Json, Box<dyn Error>> {
    let OneSelect::Select { columns, from, where_clause, group_by, .. } = &select.body.select else {
        return Err("SELECT body is VALUES".into());
    };
    if select.body.compounds.is_some() {
        return Err("compound SELECT is outside the summary".into());
    }
    let mut walk = Walk::default();
    walk.select(select);
    let joins = from.as_ref().and_then(|from| from.joins.as_ref()).map_or(0, |joins| joins.len());
    Ok(json!({
        "kind": "select", "tables": walk.tables.iter().collect::<Vec<_>>(),
        "select_items": columns.len(), "joins": joins, "where": where_clause.is_some(),
        "group_by": group_by.map_or(0, |keys| keys.len()),
        "order_by": select.order_by.map_or(0, |keys| keys.len()),
        "functions": walk.functions.iter().collect::<Vec<_>>(), "literals": walk.literals(),
    }))
}

fn summarize(statement: &Stmt) -> Result<Json, Box<dyn Error>> {
    match statement {
        Stmt::Select(select) => select_summary(select),
        Stmt::Insert { tbl_name, columns, body, .. } => {
            let InsertBody::Select(select, _) = body else {
                return Err("INSERT body is DEFAULT VALUES".into());
            };
            let OneSelect::Values(rows) = &select.body.select else {
                return Err("INSERT body is not VALUES".into());
            };
            let mut walk = Walk::default();
            walk.select(select);
            Ok(json!({"kind": "insert", "tables": [tbl_name.name.0.to_lowercase()],
                      "columns": columns.as_ref().map_or(0, |names| names.len()),
                      "rows": rows.len(), "literals": walk.literals()}))
        }
        other => Ok(json!({"kind": format!("{other:?}").split(['(', ' ', '{']).next().unwrap_or("").to_lowercase()})),
    }
}

pub fn parse(data: &[u8]) -> Result<String, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let bump = Bump::new();
    let mut parser = Parser::new(&bump, data);
    let mut summaries = Vec::new();
    while let Some(cmd) = parser.next()? {
        let Cmd::Stmt(statement) = &cmd else {
            return Err("EXPLAIN is outside the summary".into());
        };
        summaries.push(summarize(statement)?);
    }
    Ok(serde_json::to_string(&json!({"statement_count": summaries.len(), "statements": summaries}))?)
}
