# jdk-documentbuilder — XML / Java

Pinned release: `25.0.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/java/xml/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build xml java jdk_documentbuilder
python3 parsarium.py run xml java jdk_documentbuilder controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java jdk_documentbuilder CORPUS_DIR runs/xml-jdk_documentbuilder-replay
python3 parsarium.py afl build xml java jdk_documentbuilder
python3 parsarium.py afl prepare xml java jdk_documentbuilder runs/xml-jdk_documentbuilder-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
