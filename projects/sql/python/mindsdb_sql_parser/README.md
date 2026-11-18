# mindsdb-sql-parser — SQL / Python

Pinned release: `0.13.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/python/mindsdb-sql-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql python mindsdb_sql_parser
python3 parsarium.py run sql python mindsdb_sql_parser controls/sql/select-join.sql
python3 parsarium.py replay sql python mindsdb_sql_parser CORPUS_DIR runs/sql-mindsdb_sql_parser-replay
python3 parsarium.py afl build sql python mindsdb_sql_parser
python3 parsarium.py afl prepare sql python mindsdb_sql_parser runs/sql-mindsdb_sql_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
