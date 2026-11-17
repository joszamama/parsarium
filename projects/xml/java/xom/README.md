# xom — XML / Java

Pinned release: `1.4.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/java/xom/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml java xom
python3 parsarium.py run xml java xom controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java xom CORPUS_DIR runs/xml-xom-replay
python3 parsarium.py afl build xml java xom
python3 parsarium.py afl prepare xml java xom runs/xml-xom-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
