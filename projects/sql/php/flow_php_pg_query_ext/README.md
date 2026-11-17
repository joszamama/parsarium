# flow-php/pg-query-ext — SQL / PHP

Pinned release: `0.48.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/php/flow-php-pg-query-ext/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql php flow_php_pg_query_ext
python3 parsarium.py run sql php flow_php_pg_query_ext controls/sql/select-join.sql
python3 parsarium.py replay sql php flow_php_pg_query_ext CORPUS_DIR runs/sql-flow_php_pg_query_ext-replay
python3 parsarium.py afl build sql php flow_php_pg_query_ext
python3 parsarium.py afl prepare sql php flow_php_pg_query_ext runs/sql-flow_php_pg_query_ext-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** One run records Clang/LLVM source coverage of the pg_query extension (ext/pg_query.c) and of source-built libpg_query 18.0.0 (PostgreSQL raw parser, memory contexts and JSON output functions) linked into pg_query.so, for one pg_query_parse() call on a valid control. PHP itself is a plain build and is not covered; the JSON decode and summary walk in summary.php run no extension or libpg_query code. AFL++ feedback comes from the native overlay: ext/pg_query.c plus libpg_query src_backend_parser_gram.c, src_backend_parser_scan.c and src_backend_parser_parser.c, instrumented through an allowlist while the same harness runs; the PHP runtime, the JSON output functions and the rest of libpg_query add no AFL++ tuples, and the full-harness maps equal the parse-only fuzz-target maps. Replay is per case.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
