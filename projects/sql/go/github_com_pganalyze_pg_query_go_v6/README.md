# github.com/pganalyze/pg_query_go/v6 — SQL / Go

Pinned release: `v6.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/go/github-com-pganalyze-pg-query-go-v6/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql go github_com_pganalyze_pg_query_go_v6
python3 parsarium.py run sql go github_com_pganalyze_pg_query_go_v6 controls/sql/select-join.sql
python3 parsarium.py replay sql go github_com_pganalyze_pg_query_go_v6 CORPUS_DIR runs/sql-github_com_pganalyze_pg_query_go_v6-replay
python3 parsarium.py afl build sql go github_com_pganalyze_pg_query_go_v6
python3 parsarium.py afl prepare sql go github_com_pganalyze_pg_query_go_v6 runs/sql-github_com_pganalyze_pg_query_go_v6-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
