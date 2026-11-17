# C × SQL: pilot ranking

Two third-party paths are control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

Debian popcon sourcemax installations by source package (pinned snapshot), captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | libgda | 5.2.10 | 2,105 | `gda_sql_parser_parse_string(GdaSqlParser*, local NUL-terminated SQL text, &remain, &error) -> GdaStatement ("structure": GdaSqlStatement tree)`; dialect: libgda generic parser (gda_sql_parser_new, no provider) | libgda Lemon-generated SQL grammar |
| 2 | [libpg_query](https://github.com/pganalyze/libpg_query/blob/18.1.0/README.md#usage-parsing-a-query) | 18.1.0 | 41 | `pg_query_parse(local NUL-terminated SQL text) -> PgQueryParseResult (JSON parse tree)`; dialect: PostgreSQL 18 grammar | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |

Receipts: [libgda](../../../projects/sql/c/libgda/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/c/libgda/differential.json); [libpg_query](../../../projects/sql/c/libpg_query/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/c/libpg_query/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| sqlite3 | 297,378 | excluded | SQLite (Lemon-generated parse.y) |
| postgresql-18 | 104,539 | excluded | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| sqlcipher | 3,786 | excluded | SQLite (fork) |
| libgda5 | 2,105 | selected | libgda Lemon-generated SQL parser |
| libpg-query | 41 | selected | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| duckdb | 40 | excluded | DuckDB (libpg_query-derived grammar) |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
