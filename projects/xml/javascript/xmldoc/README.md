# xmldoc — XML / JavaScript (candidate)

Pinned release: `3.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json) · [candidate row](../../../../data/javascript/xml/xmldoc-candidate.json) · [feedback receipt](../../../../data/javascript/xml/xmldoc-feedback-differential.json)

Measured path: `new XmlDocument(text)`. xmldoc builds its tree from `sax.parser(true)` without namespace processing, so outputs are raw qualified names and `xmlns` declarations stay ordinary attributes. Processing instructions and anything outside the root element are not kept. [oracle.py](oracle.py) runs expat without namespace processing over the same fields.

## Run from the repository root

```sh
python3 parsarium.py build xml javascript xmldoc
python3 parsarium.py run xml javascript xmldoc controls/xml/catalog-ns.xml
python3 parsarium.py replay xml javascript xmldoc CORPUS_DIR runs/xml-xmldoc-replay
python3 parsarium.py afl build xml javascript xmldoc
python3 parsarium.py afl prepare xml javascript xmldoc runs/xml-xmldoc-afl
python3 scripts/verify_javascript_xml_xmldoc.py --check
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
