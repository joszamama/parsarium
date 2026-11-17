# htmlparser2 — XML / JavaScript

Pinned release: `12.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/javascript/htmlparser2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml javascript htmlparser2
python3 parsarium.py run xml javascript htmlparser2 controls/xml/catalog-ns.xml
python3 parsarium.py replay xml javascript htmlparser2 CORPUS_DIR runs/xml-htmlparser2-replay
python3 parsarium.py afl build xml javascript htmlparser2
python3 parsarium.py afl prepare xml javascript htmlparser2 runs/xml-htmlparser2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
