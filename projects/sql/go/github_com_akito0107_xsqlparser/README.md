# github.com/akito0107/xsqlparser — SQL / Go

Pinned release: `v1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/go/github-com-akito0107-xsqlparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql go github_com_akito0107_xsqlparser
python3 parsarium.py run sql go github_com_akito0107_xsqlparser controls/sql/select-join.sql
python3 parsarium.py replay sql go github_com_akito0107_xsqlparser CORPUS_DIR runs/sql-github_com_akito0107_xsqlparser-replay
python3 parsarium.py afl build sql go github_com_akito0107_xsqlparser
python3 parsarium.py afl prepare sql go github_com_akito0107_xsqlparser runs/sql-github_com_akito0107_xsqlparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
