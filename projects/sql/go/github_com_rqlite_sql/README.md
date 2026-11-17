# github.com/rqlite/sql — SQL / Go

Pinned release: `v0.0.0-20261016220845-5c0832fea6e1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/go/github-com-rqlite-sql/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql go github_com_rqlite_sql
python3 parsarium.py run sql go github_com_rqlite_sql controls/sql/select-join.sql
python3 parsarium.py replay sql go github_com_rqlite_sql CORPUS_DIR runs/sql-github_com_rqlite_sql-replay
python3 parsarium.py afl build sql go github_com_rqlite_sql
python3 parsarium.py afl prepare sql go github_com_rqlite_sql runs/sql-github_com_rqlite_sql-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
