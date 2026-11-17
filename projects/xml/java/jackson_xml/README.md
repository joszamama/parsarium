# jackson-dataformat-xml — XML / Java

Pinned release: `2.23.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/java/jackson-dataformat-xml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml java jackson_xml
python3 parsarium.py run xml java jackson_xml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java jackson_xml CORPUS_DIR runs/xml-jackson_xml-replay
python3 parsarium.py afl build xml java jackson_xml
python3 parsarium.py afl prepare xml java jackson_xml runs/xml-jackson_xml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
