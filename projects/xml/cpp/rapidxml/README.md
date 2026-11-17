# rapidxml — XML / C++

Pinned release: `1.13`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/cpp/rapidxml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml cpp rapidxml
python3 parsarium.py run xml cpp rapidxml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml cpp rapidxml CORPUS_DIR runs/xml-rapidxml-replay
python3 parsarium.py afl build xml cpp rapidxml
python3 parsarium.py afl prepare xml cpp rapidxml runs/xml-rapidxml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
