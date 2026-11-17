# org.apache.calcite:calcite-core — SQL / Java

Pinned release: `1.42.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/java/org-apache-calcite-calcite-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql java calcite
python3 parsarium.py run sql java calcite controls/sql/select-join.sql
python3 parsarium.py replay sql java calcite CORPUS_DIR runs/sql-calcite-replay
python3 parsarium.py afl build sql java calcite
python3 parsarium.py afl prepare sql java calcite runs/sql-calcite-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
