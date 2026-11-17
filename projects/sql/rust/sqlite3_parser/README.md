# sqlite3-parser — SQL / Rust

Pinned release: `0.17.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/rust/sqlite3-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql rust sqlite3_parser
python3 parsarium.py run sql rust sqlite3_parser controls/sql/select-join.sql
python3 parsarium.py replay sql rust sqlite3_parser CORPUS_DIR runs/sql-sqlite3_parser-replay
python3 parsarium.py afl build sql rust sqlite3_parser
python3 parsarium.py afl prepare sql rust sqlite3_parser runs/sql-sqlite3_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
