# Rust × SQL: pilot ranking

One third-party path is control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

crates.io recent_downloads (trailing 90 days), captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [sqlparser](https://docs.rs/sqlparser/0.64.0/sqlparser/parser/struct.Parser.html#method.parse_sql) | 0.64.0 | 18,971,518 | `Parser::parse_sql(&GenericDialect, local UTF-8 text) -> Vec<Statement>`; dialect: GenericDialect | sqlparser-rs tokenizer and recursive-descent parser |

Receipts: [sqlparser](../../../projects/sql/rust/sqlparser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/rust/sqlparser/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| sqlparser | 18,971,518 | selected | sqlparser-rs recursive-descent parser |
| sqlparser_derive | 12,207,766 | excluded | sqlparser-rs |
| datafusion-sql | 8,022,751 | excluded | sqlparser-rs |
| sqlformat | 5,159,931 | excluded | — |
| pg_query | 2,607,956 | unresolved | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| sqlite3-parser | 1,003,820 | unresolved | SQLite grammar (Lemon, Rust port) |
| polyglot-sql | 113,477 | unresolved | polyglot-sql |
| gluesql-core | 83,297 | excluded | sqlparser-rs |
| sql_query_builder | 15,937 | excluded | — |
| nom-sql | 1,551 | unresolved | nom-sql |
| sql-parse | 746 | unresolved | sql-parse |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
