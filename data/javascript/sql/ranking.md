# JavaScript × SQL: pilot ranking

No path is verified yet, so nothing is ranked. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

npm downloads, last month, captured 2026-11-17 ([snapshot](registry-snapshot.json)).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| sql-formatter | 29,933,061 | excluded | — |
| node-sql-parser | 13,709,122 | unresolved | node-sql-parser PEG.js grammars |
| libpg-query | 11,829,732 | unresolved | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| pgsql-ast-parser | 7,717,032 | unresolved | pgsql-ast-parser nearley grammar |
| pg-query-emscripten | 1,749,295 | unresolved | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| @guanmingchiu/sqlparser-ts | 598,900 | unresolved | sqlparser-rs (WASM) |
| sql-parser-cst | 536,703 | unresolved | sql-parser-cst Peggy grammar |
| dt-sql-parser | 364,059 | unresolved | dt-sql-parser ANTLR grammars |
| js-sql-parser | 157,858 | unresolved | js-sql-parser jison grammar |
| sqlite-parser | 85,900 | unresolved | sqlite-parser PEG.js grammar |
| @pgsql/parser | 78,227 | unresolved | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| pg-query-parser | 31,519 | unresolved | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| sql-parser | 16,843 | unresolved | sql-parser jison grammar |
| sql-ddl-to-json-schema | 12,081 | excluded | — |
| @florajs/sql-parser | 640 | unresolved | node-sql-parser PEG.js (fork) |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
