# pg_query — SQL / Rust

Pinned release: `18.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/rust/pg-query/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql rust pg_query
python3 parsarium.py run sql rust pg_query controls/sql/select-join.sql
python3 parsarium.py replay sql rust pg_query CORPUS_DIR runs/sql-pg_query-replay
python3 parsarium.py afl build sql rust pg_query
python3 parsarium.py afl prepare sql rust pg_query runs/sql-pg_query-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
