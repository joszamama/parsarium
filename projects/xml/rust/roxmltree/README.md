# roxmltree — XML / Rust

Pinned release: `0.21.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/rust/roxmltree/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml rust roxmltree
python3 parsarium.py run xml rust roxmltree controls/xml/catalog-ns.xml
python3 parsarium.py replay xml rust roxmltree CORPUS_DIR runs/xml-roxmltree-replay
python3 parsarium.py afl build xml rust roxmltree
python3 parsarium.py afl prepare xml rust roxmltree runs/xml-roxmltree-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
