# quick-xml — XML / Rust

Pinned release: `0.42.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/rust/quick-xml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml rust quick_xml
python3 parsarium.py run xml rust quick_xml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml rust quick_xml CORPUS_DIR runs/xml-quick_xml-replay
python3 parsarium.py afl build xml rust quick_xml
python3 parsarium.py afl prepare xml rust quick_xml runs/xml-quick_xml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
