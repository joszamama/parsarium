# duckdb — SQL / C++

Pinned release: `2.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/cpp/duckdb/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql cpp duckdb
python3 parsarium.py run sql cpp duckdb controls/sql/select-join.sql
python3 parsarium.py replay sql cpp duckdb CORPUS_DIR runs/sql-duckdb-replay
python3 parsarium.py afl build sql cpp duckdb
python3 parsarium.py afl prepare sql cpp duckdb runs/sql-duckdb-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
