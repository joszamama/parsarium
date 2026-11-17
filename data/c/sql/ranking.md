# C × SQL: pilot ranking

No path is verified yet, so nothing is ranked. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

Debian popcon sourcemax installations by source package (pinned snapshot), captured 2026-11-17 ([snapshot](registry-snapshot.json)).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| sqlite3 | 297,378 | excluded | SQLite (Lemon-generated parse.y) |
| postgresql-18 | 104,539 | excluded | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| sqlcipher | 3,786 | excluded | SQLite (fork) |
| libgda5 | 2,105 | unresolved | libgda Lemon-generated SQL parser |
| libpg-query | 41 | unresolved | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| duckdb | 40 | excluded | DuckDB (libpg_query-derived grammar) |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
