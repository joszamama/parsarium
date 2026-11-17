# woodstox-core — XML / Java

Pinned release: `7.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/java/woodstox-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml java woodstox_core
python3 parsarium.py run xml java woodstox_core controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java woodstox_core CORPUS_DIR runs/xml-woodstox_core-replay
python3 parsarium.py afl build xml java woodstox_core
python3 parsarium.py afl prepare xml java woodstox_core runs/xml-woodstox_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
