# sqlglot-rust — SQL / Rust

Pinned release: `0.11.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/rust/sqlglot-rust/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql rust sqlglot_rust
python3 parsarium.py run sql rust sqlglot_rust controls/sql/select-join.sql
python3 parsarium.py replay sql rust sqlglot_rust CORPUS_DIR runs/sql-sqlglot_rust-replay
python3 parsarium.py afl build sql rust sqlglot_rust
python3 parsarium.py afl prepare sql rust sqlglot_rust runs/sql-sqlglot_rust-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
