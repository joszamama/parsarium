# io.trino:trino-parser — SQL / Java

Pinned release: `484`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/java/io-trino-trino-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql java trino_parser
python3 parsarium.py run sql java trino_parser controls/sql/select-join.sql
python3 parsarium.py replay sql java trino_parser CORPUS_DIR runs/sql-trino_parser-replay
python3 parsarium.py afl build sql java trino_parser
python3 parsarium.py afl prepare sql java trino_parser runs/sql-trino_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
