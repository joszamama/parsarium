# opensp — XML / C++

Pinned release: `1.5.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/cpp/opensp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml cpp opensp
python3 parsarium.py run xml cpp opensp controls/xml/catalog-ns.xml
python3 parsarium.py replay xml cpp opensp CORPUS_DIR runs/xml-opensp-replay
python3 parsarium.py afl build xml cpp opensp
python3 parsarium.py afl prepare xml cpp opensp runs/xml-opensp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Two valid UTF-8 XML 1.0 controls without DOCTYPE establish opensp XmlReader's element, attribute, comment, processing-instruction, CDATA and character events for them only, as a raw-name path: qualified names, xmlns attributes, attribute order and decoded values, depth and trimmed text runs. No namespace URI, expanded name or in-scope binding is reported. Coverage counts every libopensp line reached (string, codec and stream helpers included); the XML reader's own lines are reported separately. DTDs, entities beyond the controls' references, other encodings, XML 1.1 and well-formedness rejection are not established. The expected outputs come from oracle.py (Python pyexpat in non-namespace mode, a different family from opensp).
