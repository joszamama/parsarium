# psqlparse2 — SQL / Python

Pinned release: `0.0.17`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/python/psqlparse2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql python psqlparse2
python3 parsarium.py run sql python psqlparse2 controls/sql/select-join.sql
python3 parsarium.py replay sql python psqlparse2 CORPUS_DIR runs/sql-psqlparse2-replay
python3 parsarium.py afl build sql python psqlparse2
python3 parsarium.py afl prepare sql python psqlparse2 runs/sql-psqlparse2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
