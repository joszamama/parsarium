# gsoap — XML / C++

Pinned release: `2.8.142`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/cpp/gsoap/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml cpp gsoap
python3 parsarium.py run xml cpp gsoap controls/xml/catalog-ns.xml
python3 parsarium.py replay xml cpp gsoap CORPUS_DIR runs/xml-gsoap-replay
python3 parsarium.py afl build xml cpp gsoap
python3 parsarium.py afl prepare xml cpp gsoap runs/xml-gsoap-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
