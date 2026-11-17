# rxml — XML / Rust

Pinned release: `0.14.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/rust/rxml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml rust rxml
python3 parsarium.py run xml rust rxml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml rust rxml CORPUS_DIR runs/xml-rxml-replay
python3 parsarium.py afl build xml rust rxml
python3 parsarium.py afl prepare xml rust rxml runs/xml-rxml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
