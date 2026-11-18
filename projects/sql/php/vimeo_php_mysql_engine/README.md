# vimeo/php-mysql-engine — SQL / PHP

Pinned release: `0.7.15`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/php/vimeo-php-mysql-engine/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql php vimeo_php_mysql_engine
python3 parsarium.py run sql php vimeo_php_mysql_engine controls/sql/select-join.sql
python3 parsarium.py replay sql php vimeo_php_mysql_engine CORPUS_DIR runs/sql-vimeo_php_mysql_engine-replay
python3 parsarium.py afl build sql php vimeo_php_mysql_engine
python3 parsarium.py afl prepare sql php vimeo_php_mysql_engine runs/sql-vimeo_php_mysql_engine-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
