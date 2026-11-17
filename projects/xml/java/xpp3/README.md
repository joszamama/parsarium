# xpp3 — XML / Java

Pinned release: `1.1.4c`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/java/xpp3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml java xpp3
python3 parsarium.py run xml java xpp3 controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java xpp3 CORPUS_DIR runs/xml-xpp3-replay
python3 parsarium.py afl build xml java xpp3
python3 parsarium.py afl prepare xml java xpp3 runs/xml-xpp3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
