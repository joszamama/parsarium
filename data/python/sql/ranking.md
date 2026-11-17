# Python × SQL: pilot ranking

One third-party path is control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

PyPI Stats last_month downloads (mirrors excluded), captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [sqlparse](https://sqlparse.readthedocs.io/en/0.6.1/api.html#sqlparse.parse) | 0.6.1 | 125,550,021 | `sqlparse.parse(local SQL text) -> tuple of grouped Statement token trees`; dialect: none (sqlparse has no dialect option) | sqlparse regex lexer and token-grouping engine (non-validating) |

Receipts: [sqlparse](../../../projects/sql/python/sqlparse/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/python/sqlparse/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| sqlparse | 125,550,021 | selected | sqlparse lexer and grouping engine |
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
