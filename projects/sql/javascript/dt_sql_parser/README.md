# dt-sql-parser — SQL / JavaScript

Pinned release: `4.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/javascript/dt-sql-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql javascript dt_sql_parser
python3 parsarium.py run sql javascript dt_sql_parser controls/sql/select-join.sql
python3 parsarium.py replay sql javascript dt_sql_parser CORPUS_DIR runs/sql-dt_sql_parser-replay
python3 parsarium.py afl build sql javascript dt_sql_parser
python3 parsarium.py afl prepare sql javascript dt_sql_parser runs/sql-dt_sql_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
