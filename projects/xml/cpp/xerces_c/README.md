# xerces-c — XML / C++

Pinned release: `3.3.0` (Apache release tarball, SHA-256 in [source-lock.json](source-lock.json)). [Manifest](manifest.json) · [verification receipt](verification.json)

The harness parses bytes with `XercesDOMParser` over `MemBufInputSource`, namespaces on, validation and external DTD loading off. It reports namespace-resolved element and attribute names, declarations, depth and text. Attributes are sorted per element because DOM leaves `NamedNodeMap` order unspecified.

## Run from the repository root

```sh
python3 parsarium.py build xml cpp xerces_c
python3 parsarium.py run xml cpp xerces_c controls/xml/catalog-ns.xml
python3 parsarium.py replay xml cpp xerces_c CORPUS_DIR runs/xml-xerces-replay
python3 parsarium.py afl build xml cpp xerces_c
python3 parsarium.py afl prepare xml cpp xerces_c runs/xml-xerces-afl
python3 scripts/verify_cpp_json_feedback.py --format xml --slug xerces_c
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
