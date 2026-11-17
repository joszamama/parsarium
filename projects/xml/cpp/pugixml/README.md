# pugixml — XML / C++

Pinned release: `1.16`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/cpp/pugixml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml cpp pugixml
python3 parsarium.py run xml cpp pugixml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml cpp pugixml CORPUS_DIR runs/xml-pugixml-replay
python3 parsarium.py afl build xml cpp pugixml
python3 parsarium.py afl prepare xml cpp pugixml runs/xml-pugixml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
