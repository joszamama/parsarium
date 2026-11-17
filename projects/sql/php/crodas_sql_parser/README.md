# crodas/sql-parser — SQL / PHP

Pinned release: `v0.1.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/php/crodas-sql-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql php crodas_sql_parser
python3 parsarium.py run sql php crodas_sql_parser controls/sql/select-join.sql
python3 parsarium.py replay sql php crodas_sql_parser CORPUS_DIR runs/sql-crodas_sql_parser-replay
python3 parsarium.py afl build sql php crodas_sql_parser
python3 parsarium.py afl prepare sql php crodas_sql_parser runs/sql-crodas_sql_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
