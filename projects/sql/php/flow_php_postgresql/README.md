# flow-php/postgresql — SQL / PHP

Pinned release: `0.48.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/php/flow-php-postgresql/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql php flow_php_postgresql
python3 parsarium.py run sql php flow_php_postgresql controls/sql/select-join.sql
python3 parsarium.py replay sql php flow_php_postgresql CORPUS_DIR runs/sql-flow_php_postgresql-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build sql php flow_php_postgresql
python3 parsarium.py afl prepare sql php flow_php_postgresql runs/sql-flow_php_postgresql-afl --fandango 100
python3 parsarium.py afl run runs/sql-flow_php_postgresql-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** One run records two line-coverage sources for the documented sql_parse() call and the summary walk: Xdebug 3.5.3 executed lines in flow-php/postgresql PHP source (Parser, ParsedQuery, the AST Traverser and the protoc-generated Protobuf\AST classes; the Xdebug pseudo-line past the end of each first-loaded class file is removed; google/protobuf runtime lines are recorded separately and not counted) and Clang/LLVM source coverage of pg-query-ext ext/pg_query.c and libpg_query 18.0.0 in pg_query.so. Package PHP lines include the Traverser walk that the harness drives with its own NodeVisitor. AFL++ feedback comes from the native overlay: ext/pg_query.c (pg_query_parse_protobuf) plus libpg_query src_backend_parser_gram.c, src_backend_parser_scan.c and src_backend_parser_parser.c, instrumented through an allowlist while the parse-only fuzz target also runs the PHP protobuf decode; the interpreted package and google/protobuf code add no AFL++ tuples. Their parse-time package lines are recorded per control by the overlay's Xdebug trace as parser source features. Replay is per case.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
