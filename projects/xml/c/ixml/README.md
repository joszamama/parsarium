# ixml — XML / C

Pinned release: `22.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/c/ixml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml c ixml
python3 parsarium.py run xml c ixml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml c ixml CORPUS_DIR runs/xml-ixml-replay
python3 parsarium.py afl build xml c ixml
python3 parsarium.py afl prepare xml c ixml runs/xml-ixml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Two valid UTF-8 XML 1.0 controls without DOCTYPE establish IXML's element, attribute, CDATA and text DOM for them only, as a raw-name path: qualified names, xmlns attributes, attribute order and decoded values, depth and trimmed text runs. IXML drops the order control's comment and processing instruction (both sit in whitespace-only runs). No namespace URI, expanded name or in-scope binding is reported, because IXML's own namespace fields are not conformant on these controls. ixmlParseBufferEx stops at the first NUL byte. DTDs, entities beyond the controls' references, other encodings, XML 1.1 and well-formedness rejection are not established. The expected outputs come from oracle.py (Python pyexpat in non-namespace mode, a different family from IXML).
