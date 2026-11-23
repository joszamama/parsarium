# vimeo/php-mysql-engine — SQL / PHP

Pinned release: `0.7.15`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/php/vimeo-php-mysql-engine/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql php vimeo_php_mysql_engine
python3 parsarium.py run sql php vimeo_php_mysql_engine controls/sql/select-join.sql
python3 parsarium.py replay sql php vimeo_php_mysql_engine CORPUS_DIR runs/sql-vimeo_php_mysql_engine-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build sql php vimeo_php_mysql_engine
python3 parsarium.py afl prepare sql php vimeo_php_mysql_engine runs/sql-vimeo_php_mysql_engine-afl --fandango 100
python3 parsarium.py afl run runs/sql-vimeo_php_mysql_engine-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
