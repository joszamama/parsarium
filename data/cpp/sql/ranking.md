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
| antlr4-cpp-runtime | 6,770 | excluded | — |
| sqlitebrowser | 5,167 | excluded | DB Browser for SQLite internal SQLite schema parser |
| soci | 518 | excluded | — |
| kdb | 237 | excluded | KDb SQL parser (bison) |
| mysql++ | 178 | excluded | — |
| libvsqlitepp | 111 | excluded | SQLite |
| sqlitestudio | 42 | excluded | SQLiteStudio SQLite parser (Lemon) |
| libpg-query | 41 | excluded | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| duckdb | 40 | selected | DuckDB PEG parser (own grammar and transformer) |
| libodb | 28 | excluded | — |
| cppdb | 15 | excluded | — |
| hsql (hyrise/sql-parser) | n/a | unresolved | Hyrise sql-parser (Bison/Flex) |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
