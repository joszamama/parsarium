# phpmyadmin/sql-parser — SQL / PHP

Pinned release: `6.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/php/phpmyadmin-sql-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql php phpmyadmin_sql_parser
python3 parsarium.py run sql php phpmyadmin_sql_parser controls/sql/select-join.sql
python3 parsarium.py replay sql php phpmyadmin_sql_parser CORPUS_DIR runs/sql-phpmyadmin_sql_parser-replay
python3 parsarium.py afl build sql php phpmyadmin_sql_parser
python3 parsarium.py afl prepare sql php phpmyadmin_sql_parser runs/sql-phpmyadmin_sql_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
