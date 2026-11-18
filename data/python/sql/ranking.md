# Python × SQL: pilot ranking

Eight third-party paths are control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

PyPI Stats last_month downloads (mirrors excluded), captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [sqlparse](https://sqlparse.readthedocs.io/en/0.6.1/api.html#sqlparse.parse) | 0.6.1 | 125,550,021 | `sqlparse.parse(local SQL text) -> tuple of grouped Statement token trees`; dialect: none (sqlparse has no dialect option) | sqlparse regex lexer and token-grouping engine (non-validating) |
| 2 | [sqlglot](https://sqlglot.com/sqlglot.html#parse) | 30.33.0 | 91,735,974 | `sqlglot.parse(local SQL text, read=None) -> list of Expression trees`; dialect: sqlglot default dialect (read=None) | sqlglot pure-Python tokenizer and recursive-descent parser |
| 3 | [sqlfluff](https://docs.sqlfluff.com/en/4.5.0/reference/api.html#sqlfluff.parse) | 4.5.0 | 11,606,805 | `sqlfluff.parse(local SQL text, dialect="ansi") -> parse-tree record`; dialect: ansi | sqlfluff lexer and dialect grammar matcher |
| 4 | [pglast](https://pglast.readthedocs.io/en/v8/parser.html#pglast.parser.parse_sql) | 8.8 | 10,961,367 | `pglast.parse_sql(local SQL text) -> tuple of pglast.ast.RawStmt nodes`; dialect: PostgreSQL 18 (libpg_query raw parser) | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| 5 | [sqloxide](https://pypi.org/project/sqloxide/0.61.1/) | 0.61.1 | 511,801 | `sqloxide.parse_sql(local SQL text, dialect="generic") -> list of statement ASTs (Python dicts)`; dialect: generic (sqlparser GenericDialect) | sqlparser-rs |
| 6 | [mo-sql-parsing](https://github.com/klahnakoski/mo-sql-parsing/blob/master/README.md#parsing-sql) | 11.699.26234 | 103,062 | `mo_sql_parsing.parse(local SQL text) -> JSON parse tree`; dialect: common parser (mo_sql_parsing.parse) | mo-sql-parsing grammar on the mo-parsing engine |
| 7 | [psqlparse2](https://github.com/dani-maarouf/psqlparse2#overview) | 0.0.17 | 3,025 | `psqlparse2.query_to_pb(sql: str) -> psqlparse2.pb.pg_query_pb2.ParseResult`; dialect: PostgreSQL | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| 8 | [mindsdb-sql-parser](https://github.com/mindsdb/mindsdb_sql_parser#how-to-use) | 0.13.8 | 2,499 | `mindsdb_sql_parser.parse_sql(sql: str) -> ASTNode`; dialect: MindsDB SQL | mindsdb_sql_parser SLY grammar |

Receipts: [sqlparse](../../../projects/sql/python/sqlparse/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/python/sqlparse/differential.json), [sqlglot](../../../projects/sql/python/sqlglot/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/python/sqlglot/differential.json), [sqlfluff](../../../projects/sql/python/sqlfluff/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/python/sqlfluff/differential.json), [pglast](../../../projects/sql/python/pglast/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/python/pglast/differential.json), [sqloxide](../../../projects/sql/python/sqloxide/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/python/sqloxide/differential.json), [mo-sql-parsing](../../../projects/sql/python/mo_sql_parsing/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/python/mo_sql_parsing/differential.json), [psqlparse2](../../../projects/sql/python/psqlparse2/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/python/psqlparse2/differential.json), [mindsdb-sql-parser](../../../projects/sql/python/mindsdb_sql_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/python/mindsdb_sql_parser/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| sqlparse | 125,550,021 | selected | sqlparse lexer and grouping engine |
| sqlglot | 91,735,974 | selected | sqlglot tokenizer and recursive-descent parser |
| sqlfluff | 11,606,805 | selected | sqlfluff lexer and dialect grammar matcher |
| pglast | 10,961,367 | selected | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| sql-metadata | 4,518,030 | excluded | sqlglot (wrapper) |
| sqlglotrs | 4,371,917 | excluded | sqlglot |
| sqllineage | 1,022,544 | excluded | sqlparse and sqlfluff (wrapper) |
| sql-formatter | 665,038 | excluded | — |
| sqloxide | 511,801 | selected | sqlparser-rs |
| moz-sql-parser | 106,687 | excluded | mo-sql-parsing |
| sqlvalidator | 104,072 | unresolved_blocked | sqlvalidator hand-written lexer and parser |
| mo-sql-parsing | 103,062 | selected | mo-sql-parsing grammar on the mo-parsing engine |
| simple-ddl-parser | 79,894 | excluded | simple-ddl-parser PLY grammar |
| pg-query-python | 16,148 | unresolved_blocked | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| polyglot-sql | 9,851 | unresolved | polyglot-sql tokenizer and recursive-descent parser (sqlglot-style) |
| psqlparse | 8,870 | unresolved_blocked | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| bigquery-sql-parser | 8,116 | excluded | bigquery-sql-parser regular-expression extraction |
| mindsdb-sql | 7,674 | excluded | mindsdb_sql SLY grammar (predecessor of mindsdb_sql_parser) |
| sqltree | 4,432 | unresolved_blocked | sqltree hand-written tokenizer and parser |
| psqlparse2 | 3,025 | selected | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| mindsdb-sql-parser | 2,499 | selected | mindsdb_sql_parser SLY grammar |
| pg-query | 2,220 | excluded | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| sqlparser | 2,053 | excluded | sqlparser 0.0.9 SQL-file runner |
| twsqlparser | 419 | excluded | TWSqlParser two-way SQL template expander |
| antlr-tsql | 126 | unresolved | antlr-tsql ANTLR 4 T-SQL grammar with antlr-ast tree shaping |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
