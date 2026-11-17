# fast-xml-parser — XML / JavaScript

Pinned release: `5.12.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/javascript/fast-xml-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml javascript fast_xml_parser
python3 parsarium.py run xml javascript fast_xml_parser controls/xml/catalog-ns.xml
python3 parsarium.py replay xml javascript fast_xml_parser CORPUS_DIR runs/xml-fast_xml_parser-replay
python3 parsarium.py afl build xml javascript fast_xml_parser
python3 parsarium.py afl prepare xml javascript fast_xml_parser runs/xml-fast_xml_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
