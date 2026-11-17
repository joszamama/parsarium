# nom-sql — SQL / Rust

Pinned release: `0.0.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/rust/nom-sql/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql rust nom_sql
python3 parsarium.py run sql rust nom_sql controls/sql/select-join.sql
python3 parsarium.py replay sql rust nom_sql CORPUS_DIR runs/sql-nom_sql-replay
python3 parsarium.py afl build sql rust nom_sql
python3 parsarium.py afl prepare sql rust nom_sql runs/sql-nom_sql-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
