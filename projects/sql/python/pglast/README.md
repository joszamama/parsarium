# pglast — SQL / Python

Pinned release: `8.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/python/pglast/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql python pglast
python3 parsarium.py run sql python pglast controls/sql/select-join.sql
python3 parsarium.py replay sql python pglast CORPUS_DIR runs/sql-pglast-replay
python3 parsarium.py afl build sql python pglast
python3 parsarium.py afl prepare sql python pglast runs/sql-pglast-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
