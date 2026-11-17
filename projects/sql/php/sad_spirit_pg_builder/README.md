# sad_spirit/pg_builder — SQL / PHP

Pinned release: `v3.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/php/sad-spirit-pg-builder/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql php sad_spirit_pg_builder
python3 parsarium.py run sql php sad_spirit_pg_builder controls/sql/select-join.sql
python3 parsarium.py replay sql php sad_spirit_pg_builder CORPUS_DIR runs/sql-sad_spirit_pg_builder-replay
python3 parsarium.py afl build sql php sad_spirit_pg_builder
python3 parsarium.py afl prepare sql php sad_spirit_pg_builder runs/sql-sad_spirit_pg_builder-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
