# qusql-parse — SQL / Rust

Pinned release: `0.12.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/rust/qusql-parse/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql rust qusql_parse
python3 parsarium.py run sql rust qusql_parse controls/sql/select-join.sql
python3 parsarium.py replay sql rust qusql_parse CORPUS_DIR runs/sql-qusql_parse-replay
python3 parsarium.py afl build sql rust qusql_parse
python3 parsarium.py afl prepare sql rust qusql_parse runs/sql-qusql_parse-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
