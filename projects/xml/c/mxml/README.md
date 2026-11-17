# mxml — XML / C

Pinned release: `4.0.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/c/mxml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml c mxml
python3 parsarium.py run xml c mxml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml c mxml CORPUS_DIR runs/xml-mxml-replay
python3 parsarium.py afl build xml c mxml
python3 parsarium.py afl prepare xml c mxml runs/xml-mxml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Two valid UTF-8 XML 1.0 controls without DOCTYPE establish mxml's element, attribute, comment, processing-instruction, CDATA and character-data tree for them only. Namespace expanded names, declaration counts and URIs are computed by the adapter from mxml's qnames and xmlns attributes; mxml itself does no namespace processing. mxmlLoadString reads a NUL-terminated string, so bytes after a NUL are not parsed. DTDs, entities beyond the controls' references, other encodings, XML 1.1 and well-formedness rejection are not established. The expected outputs come from controls/xml/check_controls.py (Python pyexpat, a different family from Mini-XML); the expat and libxml2 projects give the same summaries.
