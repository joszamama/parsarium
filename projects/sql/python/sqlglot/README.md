# sqlglot — SQL / Python

Pinned release: `30.33.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/python/sqlglot/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql python sqlglot
python3 parsarium.py run sql python sqlglot controls/sql/select-join.sql
python3 parsarium.py replay sql python sqlglot CORPUS_DIR runs/sql-sqlglot-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build sql python sqlglot
python3 parsarium.py afl prepare sql python sqlglot runs/sql-sqlglot-afl --fandango 100
python3 parsarium.py afl run runs/sql-sqlglot-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
