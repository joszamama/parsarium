# mo-sql-parsing — SQL / Python

Pinned release: `11.699.26234`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/python/mo-sql-parsing/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql python mo_sql_parsing
python3 parsarium.py run sql python mo_sql_parsing controls/sql/select-join.sql
python3 parsarium.py replay sql python mo_sql_parsing CORPUS_DIR runs/sql-mo_sql_parsing-replay
python3 parsarium.py afl build sql python mo_sql_parsing
python3 parsarium.py afl prepare sql python mo_sql_parsing runs/sql-mo_sql_parsing-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
