# libcutl — XML / C++

Pinned release: `1.10.0+ds1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/cpp/libcutl/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml cpp libcutl
python3 parsarium.py run xml cpp libcutl controls/xml/catalog-ns.xml
python3 parsarium.py replay xml cpp libcutl CORPUS_DIR runs/xml-libcutl-replay
python3 parsarium.py afl build xml cpp libcutl
python3 parsarium.py afl prepare xml cpp libcutl runs/xml-libcutl-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
