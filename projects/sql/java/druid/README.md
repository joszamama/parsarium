# com.alibaba:druid — SQL / Java

Pinned release: `1.2.28`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/java/com-alibaba-druid/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql java druid
python3 parsarium.py run sql java druid controls/sql/select-join.sql
python3 parsarium.py replay sql java druid CORPUS_DIR runs/sql-druid-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build sql java druid
python3 parsarium.py afl prepare sql java druid runs/sql-druid-afl --fandango 100
python3 parsarium.py afl run runs/sql-druid-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
