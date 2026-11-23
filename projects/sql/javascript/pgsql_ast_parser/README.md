# pgsql-ast-parser — SQL / JavaScript

Pinned release: `12.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/javascript/pgsql-ast-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql javascript pgsql_ast_parser
python3 parsarium.py run sql javascript pgsql_ast_parser controls/sql/select-join.sql
python3 parsarium.py replay sql javascript pgsql_ast_parser CORPUS_DIR runs/sql-pgsql_ast_parser-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build sql javascript pgsql_ast_parser
python3 parsarium.py afl prepare sql javascript pgsql_ast_parser runs/sql-pgsql_ast_parser-afl --fandango 100
python3 parsarium.py afl run runs/sql-pgsql_ast_parser-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
