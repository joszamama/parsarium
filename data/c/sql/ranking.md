# C × SQL: pilot ranking

Three third-party paths are control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

Debian popcon sourcemax installations by source package (pinned snapshot), captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | libgda | 5.2.10 | 2,105 | `gda_sql_parser_parse_string(GdaSqlParser*, local NUL-terminated SQL text, &remain, &error) -> GdaStatement ("structure": GdaSqlStatement tree)`; dialect: libgda generic parser (gda_sql_parser_new, no provider) | libgda Lemon-generated SQL grammar |
| 2 | [libpg_query](https://github.com/pganalyze/libpg_query/blob/18.1.0/README.md#usage-parsing-a-query) | 18.1.0 | 41 | `pg_query_parse(local NUL-terminated SQL text) -> PgQueryParseResult (JSON parse tree)`; dialect: PostgreSQL 18 grammar | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| 3 | [tree-sitter-sql](https://github.com/DerekStride/tree-sitter-sql/tree/v0.3.11) | 0.3.11 | 8 | `ts_parser_parse_string(parser with tree_sitter_sql(), local SQL text) -> TSTree (concrete syntax tree)`; dialect: tree-sitter-sql multi-dialect grammar (no dialect option) | tree-sitter-sql grammar on the tree-sitter C runtime (error-tolerant; trees with ERROR or MISSING nodes rejected) |

Receipts: [libgda](../../../projects/sql/c/libgda/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/c/libgda/differential.json); [libpg_query](../../../projects/sql/c/libpg_query/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/c/libpg_query/differential.json); [tree-sitter-sql](../../../projects/sql/c/tree_sitter_sql/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/c/tree_sitter_sql/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| sqlite3 | 297,378 | excluded | SQLite (Lemon-generated parse.y) |
| mariadb | 119,017 | excluded | MariaDB server and client source package |
| postgresql-18 | 104,539 | excluded | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| unixodbc | 58,128 | excluded | unixODBC driver manager |
| spatialite | 30,735 | excluded | SpatiaLite SQLite extension |
| tree-sitter | 15,318 | excluded | tree-sitter C runtime (no SQL grammar) |
| freetds | 8,190 | excluded | FreeTDS TDS client library |
| sqlcipher | 3,786 | excluded | SQLite (fork) |
| libgda5 | 2,105 | selected | libgda Lemon-generated SQL parser |
| psqlodbc | 1,581 | excluded | PostgreSQL ODBC driver |
| virtuoso-opensource | 967 | excluded | OpenLink Virtuoso SQL/SPARQL engine |
| cowsql | 728 | excluded | SQLite (distributed engine) |
| mdbtools | 579 | excluded | libmdbsql lex/yacc grammar for Access databases |
| mydumper | 382 | excluded | — |
| dqlite | 209 | excluded | SQLite (distributed engine) |
| sqliteodbc | 180 | excluded | SQLite |
| pgpool2 | 57 | excluded | PostgreSQL grammar (copy compiled into pgpool-II) |
| libpg-query | 41 | selected | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| duckdb | 40 | excluded | DuckDB PEG parser (own grammar since 2.0.0; 1.x used a libpg_query-derived grammar) |
| tarantool | 24 | excluded | Tarantool SQL (SQLite-derived front end) |
| libcypher-parser | 22 | excluded | — |
| tree-sitter-sql | 8 | selected | tree-sitter-sql grammar on the tree-sitter C runtime |
| liteparser (sqliteai/liteparser) | n/a | unresolved_no_primary_metric | SQLite grammar (Lemon parse.y extraction) |
| libinjection | n/a | excluded | — |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
