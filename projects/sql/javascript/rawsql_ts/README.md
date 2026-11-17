# rawsql-ts — SQL / JavaScript

Pinned release: `0.30.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/javascript/rawsql-ts/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql javascript rawsql_ts
python3 parsarium.py run sql javascript rawsql_ts controls/sql/select-join.sql
python3 parsarium.py replay sql javascript rawsql_ts CORPUS_DIR runs/sql-rawsql_ts-replay
python3 parsarium.py afl build sql javascript rawsql_ts
python3 parsarium.py afl prepare sql javascript rawsql_ts runs/sql-rawsql_ts-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
