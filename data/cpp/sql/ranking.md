# C++ × SQL: pilot ranking

Two third-party paths are control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

Debian popcon sourcemax installations by source package (pinned snapshot), captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Debian installations (popcon) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [duckdb](https://github.com/duckdb/duckdb/blob/v2.0.0/src/include/duckdb/parser/parser.hpp) | 2.0.0 | 40 | `duckdb::Parser::GetBuiltinParser(); Parser::ParseQuery(local SQL text) -> Parser::statements (SQLStatement trees)`; dialect: DuckDB built-in grammar (Parser::GetBuiltinParser; no client context) | DuckDB PEG parser (own grammar and transformer) |

## Supplemental star-fallback ranking

GitHub stars (secondary, repository interest, not downloads), from the GitHub REST API on 2026-11-18 ([snapshot](registry-snapshot.json), key `round_6_star_fallback`). These paths fill slots left after the popcon path, are ranked only among themselves, and are never compared with popcon counts.

| Rank | Package | Release | Stars | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [googlesql](https://github.com/google/googlesql/blob/2026.11.2/googlesql/parser/parser.h) | 2026.11.2 | 2,642 | `googlesql::ParseNextStatement(local SQL text, ParserOptions{LanguageOptions()}) -> ParserOutput::statement() (ASTStatement tree)`; dialect: GoogleSQL default grammar (no catalog, no analyzer) | GoogleSQL (formerly ZetaSQL) Textmapper-generated parser |

Receipts: [duckdb](../../../projects/sql/cpp/duckdb/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/cpp/duckdb/differential.json); [googlesql](../../../projects/sql/cpp/googlesql/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/cpp/googlesql/differential.json).

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
| hsql (hyrise/sql-parser) | n/a (813 stars) | excluded_no_release | Hyrise sql-parser (Bison/Flex) |
| cybergarage/usql | n/a (55 stars) | excluded_below_threshold | cybergarage uSQL parser |
| sqltoast (jaypipes/sqltoast) | n/a (33 stars) | excluded_below_threshold | sqltoast hand-written C++ parser |
| GoogleSQL (google/zetasql) | n/a (2,642 stars) | selected | GoogleSQL (formerly ZetaSQL) Textmapper-generated parser |
| ClickHouse parsers | n/a | excluded | ClickHouse server parser (internal) |
| sqlcheck (jarulraj/sqlcheck) | n/a (2,520 stars) | excluded_not_parser | — |
| Hyrise (hyrise/hyrise) | n/a (872 stars) | excluded | Hyrise sql-parser (Bison/Flex) |
| SQLines (dmtolpeko/sqlines) | n/a (432 stars) | excluded_no_release | — |
| constexpr-sql (mkitzan/constexpr-sql) | n/a (142 stars) | excluded_no_release | constexpr-sql compile-time parser |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).

The C and C++ GitHub-star fallback (2026-11-18) applies to this cell; star counts in the table above are GitHub `stargazers_count` from the [snapshot](registry-snapshot.json) (`round_6_star_fallback`), not popcon values. Twenty bounded repository searches with `stars:>=100` are recorded there.
