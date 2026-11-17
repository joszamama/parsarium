# org.apache.shardingsphere:shardingsphere-sql-parser-engine — SQL / Java

Pinned release: `5.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/java/org-apache-shardingsphere-shardingsphere-sql-parser-engine/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql java shardingsphere_sql_parser
python3 parsarium.py run sql java shardingsphere_sql_parser controls/sql/select-join.sql
python3 parsarium.py replay sql java shardingsphere_sql_parser CORPUS_DIR runs/sql-shardingsphere_sql_parser-replay
python3 parsarium.py afl build sql java shardingsphere_sql_parser
python3 parsarium.py afl prepare sql java shardingsphere_sql_parser runs/sql-shardingsphere_sql_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
