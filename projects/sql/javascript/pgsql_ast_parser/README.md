# pgsql-ast-parser — SQL / JavaScript

Pinned release: `12.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/javascript/pgsql-ast-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql javascript pgsql_ast_parser
python3 parsarium.py run sql javascript pgsql_ast_parser controls/sql/select-join.sql
python3 parsarium.py replay sql javascript pgsql_ast_parser CORPUS_DIR runs/sql-pgsql_ast_parser-replay
python3 parsarium.py afl build sql javascript pgsql_ast_parser
python3 parsarium.py afl prepare sql javascript pgsql_ast_parser runs/sql-pgsql_ast_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
