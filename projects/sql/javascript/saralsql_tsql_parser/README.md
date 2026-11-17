# @saralsql/tsql-parser — SQL / JavaScript

Pinned release: `0.4.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/javascript/saralsql-tsql-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql javascript saralsql_tsql_parser
python3 parsarium.py run sql javascript saralsql_tsql_parser controls/sql/select-join.sql
python3 parsarium.py replay sql javascript saralsql_tsql_parser CORPUS_DIR runs/sql-saralsql_tsql_parser-replay
python3 parsarium.py afl build sql javascript saralsql_tsql_parser
python3 parsarium.py afl prepare sql javascript saralsql_tsql_parser runs/sql-saralsql_tsql_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
