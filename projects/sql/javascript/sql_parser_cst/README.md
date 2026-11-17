# sql-parser-cst — SQL / JavaScript

Pinned release: `0.44.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/javascript/sql-parser-cst/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql javascript sql_parser_cst
python3 parsarium.py run sql javascript sql_parser_cst controls/sql/select-join.sql
python3 parsarium.py replay sql javascript sql_parser_cst CORPUS_DIR runs/sql-sql_parser_cst-replay
python3 parsarium.py afl build sql javascript sql_parser_cst
python3 parsarium.py afl prepare sql javascript sql_parser_cst runs/sql-sql_parser_cst-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
