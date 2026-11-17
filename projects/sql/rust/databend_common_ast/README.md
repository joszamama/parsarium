# databend-common-ast — SQL / Rust

Pinned release: `0.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/rust/databend-common-ast/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql rust databend_common_ast
python3 parsarium.py run sql rust databend_common_ast controls/sql/select-join.sql
python3 parsarium.py replay sql rust databend_common_ast CORPUS_DIR runs/sql-databend_common_ast-replay
python3 parsarium.py afl build sql rust databend_common_ast
python3 parsarium.py afl prepare sql rust databend_common_ast runs/sql-databend_common_ast-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
