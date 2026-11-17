# sqlglot — SQL / Python

Pinned release: `30.33.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/python/sqlglot/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql python sqlglot
python3 parsarium.py run sql python sqlglot controls/sql/select-join.sql
python3 parsarium.py replay sql python sqlglot CORPUS_DIR runs/sql-sqlglot-replay
python3 parsarium.py afl build sql python sqlglot
python3 parsarium.py afl prepare sql python sqlglot runs/sql-sqlglot-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
