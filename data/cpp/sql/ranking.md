# C++ × SQL: pilot ranking

No path is verified yet, so nothing is ranked. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

Debian popcon sourcemax installations by source package (pinned snapshot), captured 2026-11-17 ([snapshot](registry-snapshot.json)).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| soci | 518 | excluded | — |
| mysql++ | 178 | excluded | — |
| libvsqlitepp | 111 | excluded | SQLite |
| libpg-query | 41 | excluded | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| duckdb | 40 | unresolved | DuckDB transformer over a libpg_query-derived PostgreSQL grammar |
| libodb | 28 | excluded | — |
| cppdb | 15 | excluded | — |
| hsql (hyrise/sql-parser) | n/a | unresolved | Hyrise sql-parser (Bison/Flex) |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
