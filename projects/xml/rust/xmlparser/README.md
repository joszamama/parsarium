# xmlparser — XML / Rust

Pinned release: `0.13.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/rust/xmlparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml rust xmlparser
python3 parsarium.py run xml rust xmlparser controls/xml/catalog-ns.xml
python3 parsarium.py replay xml rust xmlparser CORPUS_DIR runs/xml-xmlparser-replay
python3 parsarium.py afl build xml rust xmlparser
python3 parsarium.py afl prepare xml rust xmlparser runs/xml-xmlparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
