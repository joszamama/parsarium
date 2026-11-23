# sad_spirit/pg_builder — SQL / PHP

Pinned release: `v3.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/php/sad-spirit-pg-builder/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql php sad_spirit_pg_builder
python3 parsarium.py run sql php sad_spirit_pg_builder controls/sql/select-join.sql
python3 parsarium.py replay sql php sad_spirit_pg_builder CORPUS_DIR runs/sql-sad_spirit_pg_builder-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build sql php sad_spirit_pg_builder
python3 parsarium.py afl prepare sql php sad_spirit_pg_builder runs/sql-sad_spirit_pg_builder-afl --fandango 100
python3 parsarium.py afl run runs/sql-sad_spirit_pg_builder-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
