# @appland/sql-parser — SQL / JavaScript

Pinned release: `1.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/javascript/appland-sql-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql javascript appland_sql_parser
python3 parsarium.py run sql javascript appland_sql_parser controls/sql/select-join.sql
python3 parsarium.py replay sql javascript appland_sql_parser CORPUS_DIR runs/sql-appland_sql_parser-replay
python3 parsarium.py afl build sql javascript appland_sql_parser
python3 parsarium.py afl prepare sql javascript appland_sql_parser runs/sql-appland_sql_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
