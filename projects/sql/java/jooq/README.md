# org.jooq:jooq — SQL / Java

Pinned release: `3.21.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/java/org-jooq-jooq/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql java jooq
python3 parsarium.py run sql java jooq controls/sql/select-join.sql
python3 parsarium.py replay sql java jooq CORPUS_DIR runs/sql-jooq-replay
python3 parsarium.py afl build sql java jooq
python3 parsarium.py afl prepare sql java jooq runs/sql-jooq-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
