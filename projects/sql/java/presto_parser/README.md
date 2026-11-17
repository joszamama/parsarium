# com.facebook.presto:presto-parser — SQL / Java

Pinned release: `0.300`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/java/com-facebook-presto-presto-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql java presto_parser
python3 parsarium.py run sql java presto_parser controls/sql/select-join.sql
python3 parsarium.py replay sql java presto_parser CORPUS_DIR runs/sql-presto_parser-replay
python3 parsarium.py afl build sql java presto_parser
python3 parsarium.py afl prepare sql java presto_parser runs/sql-presto_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
