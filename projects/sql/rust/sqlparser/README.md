# sqlparser — SQL / Rust

Pinned release: `0.64.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/rust/sqlparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql rust sqlparser
python3 parsarium.py run sql rust sqlparser controls/sql/select-join.sql
python3 parsarium.py replay sql rust sqlparser CORPUS_DIR runs/sql-sqlparser-replay
python3 parsarium.py afl build sql rust sqlparser
python3 parsarium.py afl prepare sql rust sqlparser runs/sql-sqlparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
