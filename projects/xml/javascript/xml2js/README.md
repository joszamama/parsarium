# xml2js — XML / JavaScript

Pinned release: `0.6.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/javascript/xml2js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml javascript xml2js
python3 parsarium.py run xml javascript xml2js controls/xml/catalog-ns.xml
python3 parsarium.py replay xml javascript xml2js CORPUS_DIR runs/xml-xml2js-replay
python3 parsarium.py afl build xml javascript xml2js
python3 parsarium.py afl prepare xml javascript xml2js runs/xml-xml2js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
