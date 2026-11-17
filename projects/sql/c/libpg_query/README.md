# libpg_query — SQL / C

Pinned release: `18.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/c/libpg-query/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql c libpg_query
python3 parsarium.py run sql c libpg_query controls/sql/select-join.sql
python3 parsarium.py replay sql c libpg_query CORPUS_DIR runs/sql-libpg_query-replay
python3 parsarium.py afl build sql c libpg_query
python3 parsarium.py afl prepare sql c libpg_query runs/sql-libpg_query-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
