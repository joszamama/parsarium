# tinyxml — XML / C++

Pinned release: `2.6.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/cpp/tinyxml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml cpp tinyxml
python3 parsarium.py run xml cpp tinyxml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml cpp tinyxml CORPUS_DIR runs/xml-tinyxml-replay
python3 parsarium.py afl build xml cpp tinyxml
python3 parsarium.py afl prepare xml cpp tinyxml runs/xml-tinyxml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
