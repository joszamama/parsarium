# googlesql — SQL / C++

Pinned release: `2026.11.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/cpp/googlesql/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql cpp googlesql
python3 parsarium.py run sql cpp googlesql controls/sql/select-join.sql
python3 parsarium.py replay sql cpp googlesql CORPUS_DIR runs/sql-googlesql-replay
python3 parsarium.py afl build sql cpp googlesql
python3 parsarium.py afl prepare sql cpp googlesql runs/sql-googlesql-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
