# bleksak/sqlite-toolkit — SQL / PHP

Pinned release: `1.0.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/php/bleksak-sqlite-toolkit/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql php bleksak_sqlite_toolkit
python3 parsarium.py run sql php bleksak_sqlite_toolkit controls/sql/select-join.sql
python3 parsarium.py replay sql php bleksak_sqlite_toolkit CORPUS_DIR runs/sql-bleksak_sqlite_toolkit-replay
python3 parsarium.py afl build sql php bleksak_sqlite_toolkit
python3 parsarium.py afl prepare sql php bleksak_sqlite_toolkit runs/sql-bleksak_sqlite_toolkit-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
