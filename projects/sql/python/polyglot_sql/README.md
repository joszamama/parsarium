# polyglot-sql — SQL / Python

Pinned release: `0.14.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/python/polyglot-sql/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql python polyglot_sql
python3 parsarium.py run sql python polyglot_sql controls/sql/select-join.sql
python3 parsarium.py replay sql python polyglot_sql CORPUS_DIR runs/sql-polyglot_sql-replay
python3 parsarium.py afl build sql python polyglot_sql
python3 parsarium.py afl prepare sql python polyglot_sql runs/sql-polyglot_sql-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
