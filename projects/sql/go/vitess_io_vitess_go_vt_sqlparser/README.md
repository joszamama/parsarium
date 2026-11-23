# vitess.io/vitess/go/vt/sqlparser — SQL / Go

Pinned release: `v0.24.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/go/vitess-io-vitess-go-vt-sqlparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql go vitess_io_vitess_go_vt_sqlparser
python3 parsarium.py run sql go vitess_io_vitess_go_vt_sqlparser controls/sql/select-join.sql
python3 parsarium.py replay sql go vitess_io_vitess_go_vt_sqlparser CORPUS_DIR runs/sql-vitess_io_vitess_go_vt_sqlparser-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build sql go vitess_io_vitess_go_vt_sqlparser
python3 parsarium.py afl prepare sql go vitess_io_vitess_go_vt_sqlparser runs/sql-vitess_io_vitess_go_vt_sqlparser-afl --fandango 100
python3 parsarium.py afl run runs/sql-vitess_io_vitess_go_vt_sqlparser-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
