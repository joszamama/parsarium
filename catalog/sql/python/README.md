# SQL / Python — pilot

**Status:** pilot_ten_selected_search_bounded; incomplete. 10 verified third-party paths, 0 verified standard APIs, 10 verified Docker harnesses.

Ten verified Python SQL paths after a bounded PyPI Simple index name search (rounds 1-2: five normalized-name queries, 41 hits; round 3 on 2026-11-18: five more queries, 28 hits; all hits kept) and PyPI Stats last_month metrics for targeted leads (rounds 1-2 captured 2026-11-17, round 3 on 2026-11-18 from the same source, compared with that one-day offset). Selected: sqlparse 0.6.1 (125,550,021; sqlparse regex lexer and token-grouping engine (non-validating)); sqlglot 30.33.0 (91,735,974; sqlglot pure-Python tokenizer and recursive-descent parser); sqlfluff 4.5.0 (11,606,805; sqlfluff lexer and dialect grammar matcher); pglast 8.8 (10,961,367; PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser)); sqloxide 0.61.1 (511,801; sqlparser-rs); mo-sql-parsing 11.699.26234 (103,062; mo-sql-parsing grammar on the mo-parsing engine); polyglot-sql 0.14.1 (9,851; polyglot-sql tokenizer and recursive-descent parser (sqlglot-style)); psqlparse2 0.0.17 (3,025; PostgreSQL grammar (libpg_query extraction of the PostgreSQL server parser)); mindsdb-sql-parser 0.13.8 (2,499; mindsdb_sql_parser SLY grammar); antlr-tsql 0.12.6 (126; antlr-tsql ANTLR 4 T-SQL grammar with antlr-ast tree shaping). sqlparse is non-validating (it accepts invalid SQL). sqlfluff is a linter whose documented sqlfluff.parse returns the ansi parse tree. pglast is source-built with LLVM coverage instead of the optimised wheel and shares the libpg_query family with the C cell. sqloxide is source-built with Rust coverage; its parser is sqlparser-rs 0.61.0, the family of the Rust sqlparser path. mo-sql-parsing runs on its mo-parsing engine. psqlparse2 (round 3) is source-built from its sdist with LLVM coverage of its Cython wrapper and its vendored libpg_query 16-5.1.0, a second libpg_query-family path beside pglast. polyglot-sql (round 3) is source-built with Rust coverage; its parser crate is the same polyglot-sql 0.14.1 source as the Rust polyglot-sql path. mindsdb-sql-parser (round 3) is pure Python on its vendored SLY engine; its predecessor mindsdb-sql is excluded. antlr-tsql (round 3) is an ANTLR 4 T-SQL grammar on the antlr4 Python runtime; its tree does not type literals, so the adapter classifies constant terminals by their quotes (greenlion precedent), and its metric is very small. Ten paths is the ceiling. Counts below 10,000 are weak adoption evidence; this is not a definitive top-ten ranking. CPython sqlite3 is an engine binding with no syntax tree and is recorded, not counted. Two valid controls establish only the tested dialect-neutral subset.

[Ranking and search limits](../../../data/python/sql/ranking.md) · [Standard API inventory](../../../data/python/sql/standard.json)

## Third-party parsers

- [sqlparse](sqlparse/README.md) — verified Docker harness
- [sqlglot](sqlglot/README.md) — verified Docker harness
- [sqlfluff](sqlfluff/README.md) — verified Docker harness
- [pglast](pglast/README.md) — verified Docker harness
- [sqloxide](sqloxide/README.md) — verified Docker harness
- [mo-sql-parsing](mo-sql-parsing/README.md) — verified Docker harness
- [polyglot-sql](polyglot-sql/README.md) — verified Docker harness
- [psqlparse2](psqlparse2/README.md) — verified Docker harness
- [mindsdb-sql-parser](mindsdb-sql-parser/README.md) — verified Docker harness
- [antlr-tsql](antlr-tsql/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
