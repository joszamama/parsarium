# JavaScript × SQL: pilot ranking

Ten third-party paths are control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

npm downloads, last month, captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | npm downloads (last month) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [node-sql-parser](https://www.npmjs.com/package/node-sql-parser/v/5.4.0) | 5.4.0 | 13,709,122 | `new Parser().astify(local UTF-8 text, {database: 'postgresql'}) from node-sql-parser/build/postgresql`; dialect: PostgreSQL grammar build (database: postgresql) | node-sql-parser PEG.js grammars (one generated parser per database) |
| 2 | [pgsql-ast-parser](https://www.npmjs.com/package/pgsql-ast-parser/v/12.0.2) | 12.0.2 | 7,717,032 | `parse(local UTF-8 text) -> Statement[]`; dialect: PostgreSQL | pgsql-ast-parser nearley grammar and moo lexer |
| 3 | [sql-parser-cst](https://www.npmjs.com/package/sql-parser-cst/v/0.44.1) | 0.44.1 | 536,703 | `parse(local UTF-8 text, {dialect: 'sqlite'}) -> Program`; dialect: SQLite (dialect: 'sqlite') | sql-parser-cst Peggy grammar |
| 4 | [dt-sql-parser](https://www.npmjs.com/package/dt-sql-parser/v/4.6.1) | 4.6.1 | 364,059 | `new MySQL().parse(local UTF-8 text, errorListener) -> ProgramContext`; dialect: MySQL (MySQL class) | dt-sql-parser ANTLR4 grammars |
| 5 | [sqlite-parser](https://www.npmjs.com/package/sqlite-parser/v/1.0.1) | 1.0.1 | 85,900 | `sqliteParser(local UTF-8 text) -> statement list`; dialect: SQLite | sqlite-parser PEG.js grammar |
| 6 | [@appland/sql-parser](https://www.npmjs.com/package/@appland/sql-parser/v/1.5.1) | 1.5.1 | 80,224 | `sqliteParser(local UTF-8 text) -> statement list`; dialect: SQLite | sqlite-parser PEG.js grammar (AppLand fork) |
| 7 | [sqllens](https://www.npmjs.com/package/sqllens/v/1.11.0) | 1.11.0 | 6,624 | `parse(local UTF-8 text, 'postgres') -> {ast, errors, cst}`; dialect: PostgreSQL (dialect 'postgres') | sqllens ANTLR4 grammars (PostgreSQL grammar forked from antlr/grammars-v4) |
| 8 | [rawsql-ts](https://www.npmjs.com/package/rawsql-ts/v/0.30.1) | 0.30.1 | 1,802 | `SqlParser.parseMany(local UTF-8 text) -> SimpleSelectQuery | InsertQuery []`; dialect: Library default (no dialect switch; PostgreSQL-oriented) | rawsql-ts hand-written tokenizer and recursive-descent parser |
| 9 | [@questdb/sql-parser](https://www.npmjs.com/package/@questdb/sql-parser/v/0.1.22) | 0.1.22 | 1,470 | `parseToAst(local UTF-8 text) -> {ast: Statement[], errors}`; dialect: QuestDB SQL | @questdb/sql-parser Chevrotain grammar |
| 10 | [@saralsql/tsql-parser](https://www.npmjs.com/package/@saralsql/tsql-parser/v/0.4.7) | 0.4.7 | 731 | `analyze(local UTF-8 text) -> {ast: Program, issues}`; dialect: T-SQL (SQL Server) | @saralsql/tsql-parser hand-written T-SQL parser |

Receipts: [node-sql-parser](../../../projects/sql/javascript/node_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/node_sql_parser/differential.json), [pgsql-ast-parser](../../../projects/sql/javascript/pgsql_ast_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/pgsql_ast_parser/differential.json), [sql-parser-cst](../../../projects/sql/javascript/sql_parser_cst/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/sql_parser_cst/differential.json), [dt-sql-parser](../../../projects/sql/javascript/dt_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/dt_sql_parser/differential.json), [sqlite-parser](../../../projects/sql/javascript/sqlite_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/sqlite_parser/differential.json), [@appland/sql-parser](../../../projects/sql/javascript/appland_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/appland_sql_parser/differential.json), [sqllens](../../../projects/sql/javascript/sqllens/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/sqllens/differential.json), [rawsql-ts](../../../projects/sql/javascript/rawsql_ts/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/rawsql_ts/differential.json), [@questdb/sql-parser](../../../projects/sql/javascript/questdb_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/questdb_sql_parser/differential.json), [@saralsql/tsql-parser](../../../projects/sql/javascript/saralsql_tsql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/javascript/saralsql_tsql_parser/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| sql-formatter | 29,933,061 | excluded | — |
| node-sql-parser | 13,709,122 | selected | node-sql-parser PEG.js grammars |
| libpg-query | 11,829,732 | unresolved_coverage_blocker | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| pgsql-ast-parser | 7,717,032 | selected | pgsql-ast-parser nearley grammar |
| @zeit/cosmosdb-query | 2,234,610 | excluded | cosmosdb-query PEG.js grammar (Cosmos DB SQL) |
| pgsql-parser | 1,853,514 | unresolved_coverage_blocker | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| pg-query-emscripten | 1,749,295 | unresolved_coverage_blocker | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| plpgsql-parser | 1,647,873 | unresolved_coverage_blocker | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| @derekstride/tree-sitter-sql | 1,186,889 | unresolved_native_coverage_blocker | tree-sitter SQL grammar (generated C parser) |
| @dbml/core | 841,383 | excluded | DBML parser with SQL DDL importers |
| @guanmingchiu/sqlparser-ts | 598,900 | unresolved_coverage_blocker | sqlparser-rs (WASM) |
| sql-parser-cst | 536,703 | selected | sql-parser-cst Peggy grammar |
| dt-sql-parser | 364,059 | selected | dt-sql-parser ANTLR grammars |
| js-sql-parser | 157,858 | excluded_control_fails | js-sql-parser jison grammar |
| @clickhouse/parser | 118,532 | excluded_control_fails | ClickHouse SQL parser (TypeScript port) |
| @materializeinc/sql-parser | 112,478 | excluded | Materialize SQL parser (Rust, WASM) |
| sqlite-parser | 85,900 | selected | sqlite-parser PEG.js grammar |
| @appland/sql-parser | 80,224 | selected | sqlite-parser PEG.js grammar (AppLand fork) |
| @pgsql/parser | 78,227 | unresolved_coverage_blocker | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| sql-parser-mistic | 68,233 | excluded_control_fails | sql-parser jison grammar (fork) |
| postgresql-eslint-parser | 50,933 | unresolved_coverage_blocker | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| pg-query-parser | 31,519 | unresolved_native_coverage_blocker | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| @griffithswaite/ts-plsql-parser | 22,144 | excluded_control_fails | PL/SQL ANTLR4 grammar (antlr/grammars-v4 PlSql) |
| sql-parser | 16,843 | excluded_control_fails | sql-parser jison grammar |
| @openobserve/node-sql-parser | 15,004 | excluded_shared_family_snapshot | node-sql-parser PEG.js grammars (republished snapshot) |
| @joe-re/sql-parser | 12,591 | excluded_control_fails | node-sql-parser PEG.js grammar (early fork, Peggy) |
| sql-ddl-to-json-schema | 12,081 | excluded | — |
| node-sqlparser | 11,959 | excluded_control_fails | node-sqlparser PEG.js grammar |
| sql-surveyor | 10,436 | excluded | antlr4ts-sql grammars (wrapper) |
| sqllens | 6,624 | selected | sqllens ANTLR4 grammars (PostgreSQL grammar forked from antlr/grammars-v4) |
| oracle-sql-parser | 4,486 | excluded | oracle-sql-parser PEG.js grammar |
| rawsql-ts | 1,802 | selected | rawsql-ts hand-written tokenizer and recursive-descent parser |
| @sgress454/node-sql-parser | 1,575 | excluded_byte_identical_grammar | node-sql-parser PEG.js grammars (fork) |
| @questdb/sql-parser | 1,470 | selected | @questdb/sql-parser Chevrotain grammar |
| @tableland/sqlparser | 1,197 | unresolved_coverage_blocker | Tableland Go SQL parser (WASM) |
| @deepnote/sql-parser | 911 | excluded_control_fails | node-sql-parser PEG.js grammar (early fork, via @joe-re/sql-parser) |
| @saralsql/tsql-parser | 731 | selected | @saralsql/tsql-parser hand-written T-SQL parser |
| @florajs/sql-parser | 640 | excluded_control_fails | node-sql-parser PEG.js (fork) |
| sqljs | 637 | excluded | — |
| sql-ast | 340 | excluded | sql-ast MySQL DDL parser |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
