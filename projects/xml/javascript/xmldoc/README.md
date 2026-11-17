# xmldoc — XML / JavaScript

Pinned release: `3.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/javascript/xmldoc/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml javascript xmldoc
python3 parsarium.py run xml javascript xmldoc controls/xml/catalog-ns.xml
python3 parsarium.py replay xml javascript xmldoc CORPUS_DIR runs/xml-xmldoc-replay
python3 parsarium.py afl build xml javascript xmldoc
python3 parsarium.py afl prepare xml javascript xmldoc runs/xml-xmldoc-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
