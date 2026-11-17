# org.apache.flink:flink-sql-parser — SQL / Java

Pinned release: `2.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/java/org-apache-flink-flink-sql-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql java flink_sql_parser
python3 parsarium.py run sql java flink_sql_parser controls/sql/select-join.sql
python3 parsarium.py replay sql java flink_sql_parser CORPUS_DIR runs/sql-flink_sql_parser-replay
python3 parsarium.py afl build sql java flink_sql_parser
python3 parsarium.py afl prepare sql java flink_sql_parser runs/sql-flink_sql_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
