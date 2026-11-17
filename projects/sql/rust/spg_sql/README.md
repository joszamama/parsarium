# spg-sql — SQL / Rust

Pinned release: `9.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/rust/spg-sql/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql rust spg_sql
python3 parsarium.py run sql rust spg_sql controls/sql/select-join.sql
python3 parsarium.py replay sql rust spg_sql CORPUS_DIR runs/sql-spg_sql-replay
python3 parsarium.py afl build sql rust spg_sql
python3 parsarium.py afl prepare sql rust spg_sql runs/sql-spg_sql-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
