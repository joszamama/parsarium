# xml — XML / Rust

Pinned release: `1.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/rust/xml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml rust xml
python3 parsarium.py run xml rust xml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml rust xml CORPUS_DIR runs/xml-xml-replay
python3 parsarium.py afl build xml rust xml
python3 parsarium.py afl prepare xml rust xml runs/xml-xml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
