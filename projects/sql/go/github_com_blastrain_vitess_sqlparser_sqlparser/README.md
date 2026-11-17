# github.com/blastrain/vitess-sqlparser/sqlparser — SQL / Go

Pinned release: `v0.0.0-20201030050434-a139afbb1aba`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/go/github-com-blastrain-vitess-sqlparser-sqlparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql go github_com_blastrain_vitess_sqlparser_sqlparser
python3 parsarium.py run sql go github_com_blastrain_vitess_sqlparser_sqlparser controls/sql/select-join.sql
python3 parsarium.py replay sql go github_com_blastrain_vitess_sqlparser_sqlparser CORPUS_DIR runs/sql-github_com_blastrain_vitess_sqlparser_sqlparser-replay
python3 parsarium.py afl build sql go github_com_blastrain_vitess_sqlparser_sqlparser
python3 parsarium.py afl prepare sql go github_com_blastrain_vitess_sqlparser_sqlparser runs/sql-github_com_blastrain_vitess_sqlparser_sqlparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
