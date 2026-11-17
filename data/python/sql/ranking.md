# Python × SQL: pilot ranking

No path is verified yet, so nothing is ranked. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

PyPI Stats last_month downloads (mirrors excluded), captured 2026-11-17 ([snapshot](registry-snapshot.json)).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| sqlparse | 125,550,021 | unresolved | sqlparse lexer and grouping engine |
| sqlglot | 91,735,974 | unresolved | sqlglot tokenizer and recursive-descent parser |
| sqlfluff | 11,606,805 | unresolved | sqlfluff dialect grammars |
| pglast | 10,961,367 | unresolved | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| sql-metadata | 4,518,030 | excluded | sqlparse (wrapper) |
| sqlglotrs | 4,371,917 | excluded | sqlglot |
| sql-formatter | 665,038 | excluded | — |
| sqloxide | 511,801 | unresolved | sqlparser-rs |
| moz-sql-parser | 106,687 | excluded | mo-sql-parsing |
| mo-sql-parsing | 103,062 | unresolved | mo-parsing grammar |
| simple-ddl-parser | 79,894 | excluded | — |
| psqlparse | 8,870 | unresolved | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| sqltree | 4,432 | unresolved | sqltree |
| pg-query | 2,220 | unresolved | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
