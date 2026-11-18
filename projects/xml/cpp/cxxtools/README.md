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

**Coverage limit:** Two valid UTF-8 XML 1.0 controls without DOCTYPE establish cxxtools XmlReader's element, attribute, comment, processing-instruction, CDATA and character events for them only, as a raw-name path: qualified names, xmlns attributes, attribute order and decoded values, depth and trimmed text runs. No namespace URI, expanded name or in-scope binding is reported. Coverage counts every libcxxtools line reached (string, codec and stream helpers included); the XML reader's own lines are reported separately. DTDs, entities beyond the controls' references, other encodings, XML 1.1 and well-formedness rejection are not established. The expected outputs come from oracle.py (Python pyexpat in non-namespace mode, a different family from cxxtools).
