# org.apache.spark:spark-catalyst_2.12 — SQL / Java

Pinned release: `3.5.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/java/org-apache-spark-spark-catalyst-2-12/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql java spark_catalyst
python3 parsarium.py run sql java spark_catalyst controls/sql/select-join.sql
python3 parsarium.py replay sql java spark_catalyst CORPUS_DIR runs/sql-spark_catalyst-replay
python3 parsarium.py afl build sql java spark_catalyst
python3 parsarium.py afl prepare sql java spark_catalyst runs/sql-spark_catalyst-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
