# com.alibaba:druid — SQL / Java

Pinned release: `1.2.28`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/java/com-alibaba-druid/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql java druid
python3 parsarium.py run sql java druid controls/sql/select-join.sql
python3 parsarium.py replay sql java druid CORPUS_DIR runs/sql-druid-replay
python3 parsarium.py afl build sql java druid
python3 parsarium.py afl prepare sql java druid runs/sql-druid-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
