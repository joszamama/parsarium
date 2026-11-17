# sqllens — SQL / JavaScript

Pinned release: `1.11.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/javascript/sqllens/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql javascript sqllens
python3 parsarium.py run sql javascript sqllens controls/sql/select-join.sql
python3 parsarium.py replay sql javascript sqllens CORPUS_DIR runs/sql-sqllens-replay
python3 parsarium.py afl build sql javascript sqllens
python3 parsarium.py afl prepare sql javascript sqllens runs/sql-sqllens-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
