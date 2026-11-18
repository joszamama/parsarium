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

**Coverage limit:** Two valid UTF-8 XML 1.0 controls without DOCTYPE establish OpenSP's XML-mode element, attribute, CDATA and text events for them only, as a raw-name path: qualified names, xmlns attributes, attribute order and decoded values, depth and trimmed text runs. Without a DTD, OpenSP implies an attribute list per element type from the first start tags it sees and reports attributes in that definition order; the harness keeps only attributes specified in each start tag, which on these controls is source order, but attribute order is not established in general. No namespace URI or expanded name is reported. The order control's comment and processing instruction end text runs and are otherwise not reported. DTDs, validation, entities beyond the controls' references, other encodings and well-formedness rejection are not established. The expected outputs come from oracle.py (Python pyexpat in non-namespace mode, a different family).
