# libxml++ — XML / C++

Pinned release: `5.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/cpp/libxml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml cpp libxmlpp
python3 parsarium.py run xml cpp libxmlpp controls/xml/catalog-ns.xml
python3 parsarium.py replay xml cpp libxmlpp CORPUS_DIR runs/xml-libxmlpp-replay
python3 parsarium.py afl build xml cpp libxmlpp
python3 parsarium.py afl prepare xml cpp libxmlpp runs/xml-libxmlpp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
