# com.github.jsqlparser:jsqlparser — SQL / Java

Pinned release: `5.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/sql/java/com-github-jsqlparser-jsqlparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build sql java jsqlparser
python3 parsarium.py run sql java jsqlparser controls/sql/select-join.sql
python3 parsarium.py replay sql java jsqlparser CORPUS_DIR runs/sql-jsqlparser-replay
python3 parsarium.py afl build sql java jsqlparser
python3 parsarium.py afl prepare sql java jsqlparser runs/sql-jsqlparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
