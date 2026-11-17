# sqlfluff — SQL / Python

Pinned release: `4.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/python/sqlfluff/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql python sqlfluff
python3 parsarium.py run sql python sqlfluff controls/sql/select-join.sql
python3 parsarium.py replay sql python sqlfluff CORPUS_DIR runs/sql-sqlfluff-replay
python3 parsarium.py afl build sql python sqlfluff
python3 parsarium.py afl prepare sql python sqlfluff runs/sql-sqlfluff-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
