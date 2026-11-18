# C++ × SQL: pilot ranking

One third-party path is control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

Debian popcon sourcemax installations by source package (pinned snapshot), captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [duckdb](https://github.com/duckdb/duckdb/blob/v2.0.0/src/include/duckdb/parser/parser.hpp) | 2.0.0 | 40 | `duckdb::Parser::GetBuiltinParser(); Parser::ParseQuery(local SQL text) -> Parser::statements (SQLStatement trees)`; dialect: DuckDB built-in grammar (Parser::GetBuiltinParser; no client context) | DuckDB PEG parser (own grammar and transformer) |

Receipts: [duckdb](../../../projects/sql/cpp/duckdb/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/cpp/duckdb/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| libreoffice | 128,949 | excluded | LibreOffice SQL parser (connectivity OSQLParser, bison) |
| gdal | 39,199 | excluded | GDAL OGR SQL (swq) parser |
| futuresql | 24,225 | excluded | KDE FutureSQL asynchronous database wrapper |
| firebird4.0 | 18,423 | excluded | Firebird DSQL parser (internal) |
| firebird3.0 | 11,394 | excluded | Firebird DSQL parser (internal) |
| antlr4-cpp-runtime | 6,770 | excluded | — |
| mysql-9.7 | 5,827 | excluded | MySQL server grammar (sql_yacc.yy) |
| apache-arrow | 5,700 | excluded | — |
| sqlitebrowser | 5,167 | excluded | DB Browser for SQLite internal SQLite schema parser |
| qgis | 1,927 | excluded | QGIS QgsSQLStatement bison grammar |
| soci | 518 | excluded | — |
| kdb | 237 | excluded | KDb SQL parser (bison) |
| mysql++ | 178 | excluded | — |
| mysql-connector-c++ | 125 | excluded | — |
| libvsqlitepp | 111 | excluded | SQLite |
| sqlitestudio | 42 | excluded | SQLiteStudio SQLite parser (Lemon) |
| libpg-query | 41 | excluded | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| duckdb | 40 | selected | DuckDB PEG parser (own grammar and transformer) |
| libodb | 28 | excluded | — |
| cppdb | 15 | excluded | — |
| sqlsmith | 5 | excluded | — |
| usql | 5 | excluded | — |
| hsql (hyrise/sql-parser) | n/a | unresolved | Hyrise sql-parser (Bison/Flex) |
| cybergarage/usql | n/a | unresolved_no_primary_metric | cybergarage uSQL parser |
| sqltoast (jaypipes/sqltoast) | n/a | unresolved_no_primary_metric | sqltoast hand-written C++ parser |
| GoogleSQL (google/zetasql) | n/a | unresolved_no_primary_metric | GoogleSQL/ZetaSQL analyzer front end |
| ClickHouse parsers | n/a | excluded | ClickHouse server parser (internal) |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
