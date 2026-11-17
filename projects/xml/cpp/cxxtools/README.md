# cxxtools — XML / C++

Pinned release: `3.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/cpp/cxxtools/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml cpp cxxtools
python3 parsarium.py run xml cpp cxxtools controls/xml/catalog-ns.xml
python3 parsarium.py replay xml cpp cxxtools CORPUS_DIR runs/xml-cxxtools-replay
python3 parsarium.py afl build xml cpp cxxtools
python3 parsarium.py afl prepare xml cpp cxxtools runs/xml-cxxtools-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
