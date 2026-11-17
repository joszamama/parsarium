# sax — XML / JavaScript

Pinned release: `1.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/javascript/sax/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml javascript sax
python3 parsarium.py run xml javascript sax controls/xml/catalog-ns.xml
python3 parsarium.py replay xml javascript sax CORPUS_DIR runs/xml-sax-replay
python3 parsarium.py afl build xml javascript sax
python3 parsarium.py afl prepare xml javascript sax runs/xml-sax-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
