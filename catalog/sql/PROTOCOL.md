# SQL cell protocol

This cell applies the [general protocol](../../PROTOCOL.md) to SQL statement text that a library parses into a syntax tree. Nothing is executed: no database server, connection, query plan or result set is part of a verified path.

## Format scope

The tested subset is dialect-neutral SQL that PostgreSQL, MySQL, SQLite and ANSI-style grammars all accept:

- a `SELECT` with qualified column references, table and column aliases with `AS`, an aggregate call (`COUNT(*)`, `SUM(...)`), one `INNER JOIN ... ON`, a `WHERE` conjunction with comparison operators, one `GROUP BY` and one `ORDER BY` key, a string and an integer literal;
- an `INSERT INTO t (columns) VALUES (...), (...)` with integer, decimal and string literals.

Each control is one ASCII statement ending in `;` and a newline. Identifiers are lowercase and unquoted; no keyword is used as an identifier. There are no comments, vendor functions, quoted identifiers, `LIMIT`/`TOP`/`FETCH`, casts, parameters, procedural blocks or DDL options. The subset says nothing about dialect-specific syntax.

An adapter must name the dialect it selects, when the API offers a choice: for example PostgreSQL for libpg_query and its bindings, MySQL for vitess and TiDB, `GenericDialect` for sqlparser-rs, the default (Calcite `SqlParser.config()` or JSqlParser's default) for Java. That choice is recorded in the project manifest and catalog row.

## Eligibility

A path qualifies when its documented API takes local SQL text and returns a statement object or syntax tree from which the summary below can be read. Excluded or left as leads in `data/<ecosystem>/sql/leads.json`:

- **Formatters, highlighters, splitters and tokenizers** that return text or a flat token list (sql-formatter, doctrine/sql-formatter, jdorn/sql-formatter, sqlformat).
- **Query builders and ORMs** that emit SQL rather than read it.
- **Database engines and drivers.** `sqlite3_prepare` (C, and Python's `sqlite3`) compiles a statement into a VDBE bytecode program. SQLite offers no public syntax tree, so it is recorded as an engine lead and used only in the oracle cross-check. DuckDB, PostgreSQL server packages and drivers are leads on the same grounds unless a documented parser API returning a statement tree is verified.
- **Schema-only parsers** (iamcal/sql-parser, simple-ddl-parser) that cannot parse the `SELECT` control. They stay leads with that evidence.
- **Proc-macro, derive or planner crates** that only consume another parser's AST (sqlparser_derive, datafusion-sql). These are shared-family leads.

`sqlparse` (Python) is a non-validating parser: `sqlparse.parse` groups tokens into a tree of `Statement`, `Identifier`, `IdentifierList`, `Where`, `Comparison`, `Function` and `Parenthesis` nodes, and it accepts invalid SQL. Its grouped tree is a parse tree that can give the summary, so it is eligible, flagged as non-validating. A path that returns only a flat token stream is not.

## Observable result

The harness walks the parser's own tree and reports, per statement:

| Field | Meaning |
| --- | --- |
| `statement_count` | Number of statements, with no empty statement for the trailing `;`. |
| `kind` | `select` or `insert`. |
| `tables` | Sorted, unique, lowercase base-table names. Aliases are not tables. |
| `select_items` | Number of projected expressions (select only). |
| `joins` | Number of join operators (select only). |
| `where` | Whether a `WHERE` predicate is present (select only). |
| `group_by`, `order_by` | Number of grouping and ordering keys (select only). |
| `functions` | Sorted, unique, lowercase function names called (select only). |
| `columns`, `rows` | Target column count and `VALUES` row count (insert only). |
| `literals` | Sorted `[kind, text]` pairs, `kind` `string` or `number`. Strings are the unquoted value. Numbers are the source text, which here equals the canonical decimal form (`10`, `19.5`, `250`). |

An adapter may convert a parser's numeric value to text only if the result equals the source text for these controls. A harness that only reports accept/reject does not qualify.

## Controls

- `controls/sql/select-join.sql`: the primary control, 212 bytes, SHA-256 `331b604d98d4d6c553e86b0fdc866c3c415260df7f1f59c5c2c71d1dfc7be3ca`.
- `controls/sql/insert-values.sql`: the fixed second control for AFL++ feedback, 103 bytes, SHA-256 `df8f5805de6eb11bd431411bb8642e95b5a53c13c37306a6bd38ad9edf5c8c35`.

`controls/sql/expected.json` holds the hand-written summaries. `controls/sql/check_controls.py` is the independent oracle check. It confirms the hashes and the literal and table spellings against the text. It then has SQLite, through Python's in-process `sqlite3`, compile each statement with an `EXPLAIN` prefix against an empty in-memory schema that declares `customers` and `orders`. `sqlite3_prepare` must accept the statement, and an authorizer callback must report the same statement kind, tables and functions as the oracle. SQLite 3.54.1 was observed. Limits: SQLite is one dialect and does not check the column, join, grouping or literal counts. Those come only from the hand-written oracle. The controls are never executed, and no data is read or written.

## Shared families

The PostgreSQL grammar extracted by libpg_query is shared by its C library, Go `pg_query_go`, Rust `pg_query`, Python `pglast`, JavaScript `libpg-query`/`@pgsql/parser` and the PHP `flow-php/pg-query-ext` extension. These are distinct package paths over one parser family. The family is recorded, and their metrics are never combined. vitess `sqlparser` is the origin of `xwb1989/sqlparser` and `blastrain/vitess-sqlparser`, and sqlparser-rs underlies DataFusion, polyglot-sql forks and the `sqlparser-ts`/`sqlparser-rs` WASM npm packages.

## Adoption

Paths are ranked within one ecosystem by that ecosystem's existing primary metric, the same source the JSON and XML pilot cells use. C and C++ use Debian popcon `sourcemax` from the pinned snapshot in `data/curation`. The C and C++ search is one source-name search, so it does not separate languages. The ceiling is ten, and no cell is padded.

## AFL++

The overlay must show parser-derived feedback on both controls. Each control runs three times under `afl-showmap`. The receipt records tuple counts, the tuples unique to each control and, where the bridge reports source features, per-file parser line differences. Repeats must be identical, and the two controls must differ. No campaign is run and no malformed input is tested.

## Fandango

Fanbase ships no SQL grammar (its `specs/` directory, checked 2026-11-17, has 33 formats and none is SQL). [`fuzzing/fandango/specs/sql.fan`](../../fuzzing/fandango/specs/sql.fan) is a local bounded seed grammar for this subset: `SELECT` with optional join, `WHERE`, `GROUP BY` and `ORDER BY`, and multi-row `INSERT`, over the two control tables. It is a valid-seed generator, not a complete SQL grammar.
