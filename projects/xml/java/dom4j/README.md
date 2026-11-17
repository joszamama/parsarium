# dom4j — XML / Java

Pinned release: `2.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/java/dom4j/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml java dom4j
python3 parsarium.py run xml java dom4j controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java dom4j CORPUS_DIR runs/xml-dom4j-replay
python3 parsarium.py afl build xml java dom4j
python3 parsarium.py afl prepare xml java dom4j runs/xml-dom4j-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
