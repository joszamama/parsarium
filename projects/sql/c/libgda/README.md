# libgda — SQL / C

Pinned release: `5.2.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/c/libgda/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql c libgda
python3 parsarium.py run sql c libgda controls/sql/select-join.sql
python3 parsarium.py replay sql c libgda CORPUS_DIR runs/sql-libgda-replay
python3 parsarium.py afl build sql c libgda
python3 parsarium.py afl prepare sql c libgda runs/sql-libgda-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
