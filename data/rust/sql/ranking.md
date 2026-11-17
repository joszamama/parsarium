# Rust × SQL: pilot ranking

No path is verified yet, so nothing is ranked. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

crates.io recent_downloads (trailing 90 days), captured 2026-11-17 ([snapshot](registry-snapshot.json)).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| sqlparser | 18,971,518 | unresolved | sqlparser-rs recursive-descent parser |
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
