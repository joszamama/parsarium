# github.com/pganalyze/pg_query_go/v6 — SQL / Go

Pinned release: `v6.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/go/github-com-pganalyze-pg-query-go-v6/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql go github_com_pganalyze_pg_query_go_v6
python3 parsarium.py run sql go github_com_pganalyze_pg_query_go_v6 controls/sql/select-join.sql
python3 parsarium.py replay sql go github_com_pganalyze_pg_query_go_v6 CORPUS_DIR runs/sql-github_com_pganalyze_pg_query_go_v6-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build sql go github_com_pganalyze_pg_query_go_v6
python3 parsarium.py afl prepare sql go github_com_pganalyze_pg_query_go_v6 runs/sql-github_com_pganalyze_pg_query_go_v6-afl --fandango 100
python3 parsarium.py afl run runs/sql-github_com_pganalyze_pg_query_go_v6-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
