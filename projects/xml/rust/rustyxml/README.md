# RustyXML — XML / Rust

Pinned release: `0.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/rust/rustyxml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml rust rustyxml
python3 parsarium.py run xml rust rustyxml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml rust rustyxml CORPUS_DIR runs/xml-rustyxml-replay
python3 parsarium.py afl build xml rust rustyxml
python3 parsarium.py afl prepare xml rust rustyxml runs/xml-rustyxml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
