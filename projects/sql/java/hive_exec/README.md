# org.apache.hive:hive-exec — SQL / Java

Pinned release: `4.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/java/org-apache-hive-hive-exec/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql java hive_exec
python3 parsarium.py run sql java hive_exec controls/sql/select-join.sql
python3 parsarium.py replay sql java hive_exec CORPUS_DIR runs/sql-hive_exec-replay
python3 parsarium.py afl build sql java hive_exec
python3 parsarium.py afl prepare sql java hive_exec runs/sql-hive_exec-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
