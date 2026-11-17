# @xmldom/xmldom — XML / JavaScript

Pinned release: `0.9.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/javascript/xmldom-xmldom/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml javascript xmldom_xmldom
python3 parsarium.py run xml javascript xmldom_xmldom controls/xml/catalog-ns.xml
python3 parsarium.py replay xml javascript xmldom_xmldom CORPUS_DIR runs/xml-xmldom_xmldom-replay
python3 parsarium.py afl build xml javascript xmldom_xmldom
python3 parsarium.py afl prepare xml javascript xmldom_xmldom runs/xml-xmldom_xmldom-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
