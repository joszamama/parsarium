# xercesImpl — XML / Java

Pinned release: `2.12.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Parser record and lead log](../../../../data/java/xml/ranking.md)

## Run from the repository root

```sh
python3 parsarium.py build xml java xercesimpl
python3 parsarium.py run xml java xercesimpl controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java xercesimpl CORPUS_DIR runs/xml-xercesimpl-replay
python3 parsarium.py afl build xml java xercesimpl
python3 parsarium.py afl prepare xml java xercesimpl runs/xml-xercesimpl-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
