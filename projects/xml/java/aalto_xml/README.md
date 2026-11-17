# aalto-xml — XML / Java

Pinned release: `1.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/java/aalto-xml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml java aalto_xml
python3 parsarium.py run xml java aalto_xml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java aalto_xml CORPUS_DIR runs/xml-aalto_xml-replay
python3 parsarium.py afl build xml java aalto_xml
python3 parsarium.py afl prepare xml java aalto_xml runs/xml-aalto_xml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
