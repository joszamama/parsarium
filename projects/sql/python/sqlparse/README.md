# sqlparse — SQL / Python

Pinned release: `0.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/python/sqlparse/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql python sqlparse
python3 parsarium.py run sql python sqlparse controls/sql/select-join.sql
python3 parsarium.py replay sql python sqlparse CORPUS_DIR runs/sql-sqlparse-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build sql python sqlparse
python3 parsarium.py afl prepare sql python sqlparse runs/sql-sqlparse-afl --fandango 100
python3 parsarium.py afl run runs/sql-sqlparse-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
