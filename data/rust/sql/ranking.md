# Rust × SQL: pilot ranking

Eight third-party paths are control verified against the hand-written oracle in [controls/sql/expected.json](../../../controls/sql/expected.json), with a pinned Docker harness, parser-source coverage and stable AFL++ feedback that differs between the two controls. Paths are ranked only among verified paths in this cell. The ceiling is ten, and the cell is not padded. The scope, controls and oracle are in [catalog/sql/PROTOCOL.md](../../../catalog/sql/PROTOCOL.md).

## Primary within-cell adoption metric

crates.io recent_downloads (trailing 90 days), captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [sqlparser](https://docs.rs/sqlparser/0.64.0/sqlparser/parser/struct.Parser.html#method.parse_sql) | 0.64.0 | 18,971,518 | `Parser::parse_sql(&GenericDialect, local UTF-8 text) -> Vec<Statement>`; dialect: GenericDialect | sqlparser-rs tokenizer and recursive-descent parser |
| 2 | [pg_query](https://docs.rs/pg_query/18.1.0/pg_query/fn.parse.html) | 18.1.0 | 2,607,956 | `pg_query::parse(local UTF-8 text, ParserOptions::DEFAULT) -> ParseResult`; dialect: PostgreSQL | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| 3 | [sqlite3-parser](https://docs.rs/sqlite3-parser/0.17.0/sqlite3_parser/lexer/sql/struct.Parser.html) | 0.17.0 | 1,003,820 | `lexer::sql::Parser::new(&Bump, local bytes) and FallibleIterator::next -> Option<Cmd>`; dialect: SQLite | SQLite grammar (lemon-rs port of SQLite's Lemon parse.y) |
| 4 | [databend-common-ast](https://docs.rs/databend-common-ast/0.2.5/databend_common_ast/parser/fn.parse_sql.html) | 0.2.5 | 6,616 | `parser::tokenize_sql(local UTF-8 text) and parser::parse_sql(&tokens, Dialect::PostgreSQL) -> (Statement, Option<String>)`; dialect: PostgreSQL (crate default) | Databend SQL parser (logos tokenizer, nom/pratt combinators) |
| 5 | [qusql-parse](https://docs.rs/qusql-parse/0.12.0/qusql_parse/fn.parse_statements.html) | 0.12.0 | 3,272 | `parse_statements(local UTF-8 text, &mut Issues, &ParseOptions::new()) -> Vec<Statement>`; dialect: MariaDB (default) | qusql-parse hand-written lexer and recursive-descent parser |
| 6 | [spg-sql](https://docs.rs/spg-sql/9.1.0/spg_sql/parser/fn.parse_statement.html) | 9.1.0 | 2,268 | `parser::parse_statement(local UTF-8 text) -> Statement`; dialect: PostgreSQL | spg-sql hand-written PostgreSQL-dialect lexer and recursive-descent parser |
| 7 | [sqlglot-rust](https://docs.rs/sqlglot-rust/0.11.2/sqlglot_rust/parser/fn.parse_statements.html) | 0.11.2 | 1,707 | `parser::parse_statements(local UTF-8 text, Dialect::Ansi) -> Vec<Statement>`; dialect: ANSI | sqlglot-rust tokenizer and recursive-descent parser (sqlglot-inspired) |
| 8 | [nom-sql](https://docs.rs/nom-sql/0.0.11/nom_sql/fn.parse_query_bytes.html) | 0.0.11 | 1,551 | `parse_query_bytes(local bytes) -> SqlQuery`; dialect: MySQL subset | nom-sql nom combinator parser (MySQL subset) |

Receipts: [sqlparser](../../../projects/sql/rust/sqlparser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/rust/sqlparser/differential.json); [pg_query](../../../projects/sql/rust/pg_query/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/rust/pg_query/differential.json); [sqlite3-parser](../../../projects/sql/rust/sqlite3_parser/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/rust/sqlite3_parser/differential.json); [databend-common-ast](../../../projects/sql/rust/databend_common_ast/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/rust/databend_common_ast/differential.json); [qusql-parse](../../../projects/sql/rust/qusql_parse/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/rust/qusql_parse/differential.json); [spg-sql](../../../projects/sql/rust/spg_sql/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/rust/spg_sql/differential.json); [sqlglot-rust](../../../projects/sql/rust/sqlglot_rust/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/rust/sqlglot_rust/differential.json); [nom-sql](../../../projects/sql/rust/nom_sql/verification.json) and its [AFL++ differential](../../../fuzzing/afl-native/sql/rust/nom_sql/differential.json).

## Leads by the same metric

| Lead | Metric | Status | Parser family |
| --- | ---: | --- | --- |
| sqlparser | 18,971,518 | selected | sqlparser-rs recursive-descent parser |
| sqlparser_derive | 12,207,766 | excluded | sqlparser-rs |
| datafusion-sql | 8,022,751 | excluded | sqlparser-rs |
| sqlformat | 5,159,931 | excluded | — |
| pg_query | 2,607,956 | selected | PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser) |
| sqlite3-parser | 1,003,820 | selected | SQLite grammar (lemon-rs port of SQLite's Lemon parse.y) |
| polyglot-sql | 113,477 | unresolved | polyglot-sql |
| gluesql-core | 83,297 | excluded | sqlparser-rs |
| sql_query_builder | 15,937 | excluded | — |
| databend-common-ast | 6,616 | selected | Databend SQL parser (logos tokenizer, nom/pratt combinators) |
| qusql-parse | 3,272 | selected | qusql-parse hand-written lexer and recursive-descent parser |
| spg-sql | 2,268 | selected | spg-sql hand-written PostgreSQL-dialect lexer and recursive-descent parser |
| sqlglot-rust | 1,707 | selected | sqlglot-rust tokenizer and recursive-descent parser (sqlglot-inspired) |
| nom-sql | 1,551 | selected | nom-sql nom combinator parser (MySQL subset) |
| sql-parse | 746 | excluded | qusql-parse hand-written lexer and recursive-descent parser (predecessor) |

Reasons are in [leads.json](leads.json). Standard and runtime findings are in [standard.json](standard.json).
