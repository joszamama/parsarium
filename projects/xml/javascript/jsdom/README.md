# jsdom — XML / JavaScript

Pinned release: `31.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/javascript/jsdom/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml javascript jsdom
python3 parsarium.py run xml javascript jsdom controls/xml/catalog-ns.xml
python3 parsarium.py replay xml javascript jsdom CORPUS_DIR runs/xml-jsdom-replay
python3 parsarium.py afl build xml javascript jsdom
python3 parsarium.py afl prepare xml javascript jsdom runs/xml-jsdom-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
