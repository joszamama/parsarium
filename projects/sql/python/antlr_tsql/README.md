# antlr-tsql — SQL / Python

Pinned release: `0.12.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/python/antlr-tsql/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql python antlr_tsql
python3 parsarium.py run sql python antlr_tsql controls/sql/select-join.sql
python3 parsarium.py replay sql python antlr_tsql CORPUS_DIR runs/sql-antlr_tsql-replay
python3 parsarium.py afl build sql python antlr_tsql
python3 parsarium.py afl prepare sql python antlr_tsql runs/sql-antlr_tsql-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
