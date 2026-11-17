# vitess.io/vitess/go/vt/sqlparser — SQL / Go

Pinned release: `v0.24.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/go/vitess-io-vitess-go-vt-sqlparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql go vitess_io_vitess_go_vt_sqlparser
python3 parsarium.py run sql go vitess_io_vitess_go_vt_sqlparser controls/sql/select-join.sql
python3 parsarium.py replay sql go vitess_io_vitess_go_vt_sqlparser CORPUS_DIR runs/sql-vitess_io_vitess_go_vt_sqlparser-replay
python3 parsarium.py afl build sql go vitess_io_vitess_go_vt_sqlparser
python3 parsarium.py afl prepare sql go vitess_io_vitess_go_vt_sqlparser runs/sql-vitess_io_vitess_go_vt_sqlparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
