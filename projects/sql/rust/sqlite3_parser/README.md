# sqlite3-parser — SQL / Rust

Pinned release: `0.17.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/rust/sqlite3-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql rust sqlite3_parser
python3 parsarium.py run sql rust sqlite3_parser controls/sql/select-join.sql
python3 parsarium.py replay sql rust sqlite3_parser CORPUS_DIR runs/sql-sqlite3_parser-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build sql rust sqlite3_parser
python3 parsarium.py afl prepare sql rust sqlite3_parser runs/sql-sqlite3_parser-afl --fandango 100
python3 parsarium.py afl run runs/sql-sqlite3_parser-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
