# github.com/xwb1989/sqlparser — SQL / Go

Pinned release: `v0.0.0-20180606152119-120387863bf2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/go/github-com-xwb1989-sqlparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql go github_com_xwb1989_sqlparser
python3 parsarium.py run sql go github_com_xwb1989_sqlparser controls/sql/select-join.sql
python3 parsarium.py replay sql go github_com_xwb1989_sqlparser CORPUS_DIR runs/sql-github_com_xwb1989_sqlparser-replay
python3 parsarium.py afl build sql go github_com_xwb1989_sqlparser
python3 parsarium.py afl prepare sql go github_com_xwb1989_sqlparser runs/sql-github_com_xwb1989_sqlparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
