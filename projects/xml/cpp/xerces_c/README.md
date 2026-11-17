# xerces-c — XML / C++

Pinned release: `3.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

`XercesDOMParser::parse(MemBufInputSource)` accepts local XML bytes. The parser uses Xerces-C++'s own scanner and does not delegate to libxml2 or expat. The [parser-only probe](parser-probe.cpp) is the AFL++ target. It checks feedback and source lines from `IGXMLScanner.cpp`, `IGXMLScanner2.cpp`, and `XMLScanner.cpp` without traversing the DOM. The regular replay remains the format-aware tree result. [Feedback receipt](../../../../fuzzing/afl-native/xml/cpp/xerces_c/differential.json)

[API, control result, and parser family](../../../../catalog/xml/cpp/xerces-c/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml cpp xerces_c
python3 parsarium.py run xml cpp xerces_c controls/xml/catalog-ns.xml
python3 parsarium.py replay xml cpp xerces_c CORPUS_DIR runs/xml-xerces_c-replay
python3 parsarium.py afl build xml cpp xerces_c
python3 parsarium.py afl prepare xml cpp xerces_c runs/xml-xerces_c-afl
python3 projects/xml/cpp/xerces_c/verify-parser-feedback.py
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
