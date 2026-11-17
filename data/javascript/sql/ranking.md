# JavaScript × SQL: pilot ranking

Five third-party paths are control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

npm downloads, last month, captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [node-sql-parser](https://www.npmjs.com/package/node-sql-parser/v/5.4.0) | 5.4.0 | 13,709,122 | `new Parser().astify(local UTF-8 text, {database: 'postgresql'}) from node-sql-parser/build/postgresql`; dialect: PostgreSQL grammar build (database: postgresql) | node-sql-parser PEG.js grammars (one generated parser per database) |
| 2 | [pgsql-ast-parser](https://www.npmjs.com/package/pgsql-ast-parser/v/12.0.2) | 12.0.2 | 7,717,032 | `parse(local UTF-8 text) -> Statement[]`; dialect: PostgreSQL | pgsql-ast-parser nearley grammar and moo lexer |
| 3 | [sql-parser-cst](https://www.npmjs.com/package/sql-parser-cst/v/0.44.1) | 0.44.1 | 536,703 | `parse(local UTF-8 text, {dialect: 'sqlite'}) -> Program`; dialect: SQLite (dialect: 'sqlite') | sql-parser-cst Peggy grammar |
| 4 | [dt-sql-parser](https://www.npmjs.com/package/dt-sql-parser/v/4.6.1) | 4.6.1 | 364,059 | `new MySQL().parse(local UTF-8 text, errorListener) -> ProgramContext`; dialect: MySQL (MySQL class) | dt-sql-parser ANTLR4 grammars |
| 5 | [sqlite-parser](https://www.npmjs.com/package/sqlite-parser/v/1.0.1) | 1.0.1 | 85,900 | `sqliteParser(local UTF-8 text) -> statement list`; dialect: SQLite | sqlite-parser PEG.js grammar |

Receipts: [node-sql-parser](../../../projects/sql/javascript/node_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/node_sql_parser/differential.json), [pgsql-ast-parser](../../../projects/sql/javascript/pgsql_ast_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/pgsql_ast_parser/differential.json), [sql-parser-cst](../../../projects/sql/javascript/sql_parser_cst/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/sql_parser_cst/differential.json), [dt-sql-parser](../../../projects/sql/javascript/dt_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/dt_sql_parser/differential.json), [sqlite-parser](../../../projects/sql/javascript/sqlite_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/sqlite_parser/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| sql-formatter | 29,933,061 | excluded | — |
| node-sql-parser | 13,709,122 | selected | node-sql-parser PEG.js grammars |
| libpg-query | 11,829,732 | unresolved_coverage_blocker | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| pgsql-ast-parser | 7,717,032 | selected | pgsql-ast-parser nearley grammar |
| pg-query-emscripten | 1,749,295 | unresolved | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| @guanmingchiu/sqlparser-ts | 598,900 | unresolved | sqlparser-rs (WASM) |
| sql-parser-cst | 536,703 | selected | sql-parser-cst Peggy grammar |
| dt-sql-parser | 364,059 | selected | dt-sql-parser ANTLR grammars |
| js-sql-parser | 157,858 | unresolved | js-sql-parser jison grammar |
| sqlite-parser | 85,900 | selected | sqlite-parser PEG.js grammar |
| @pgsql/parser | 78,227 | unresolved | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| pg-query-parser | 31,519 | unresolved | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| sql-parser | 16,843 | unresolved | sql-parser jison grammar |
| sql-ddl-to-json-schema | 12,081 | excluded | — |
| @florajs/sql-parser | 640 | unresolved | node-sql-parser PEG.js (fork) |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
