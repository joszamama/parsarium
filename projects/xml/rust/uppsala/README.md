# uppsala — XML / Rust

Pinned release: `0.12.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/rust/uppsala/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml rust uppsala
python3 parsarium.py run xml rust uppsala controls/xml/catalog-ns.xml
python3 parsarium.py replay xml rust uppsala CORPUS_DIR runs/xml-uppsala-replay
python3 parsarium.py afl build xml rust uppsala
python3 parsarium.py afl prepare xml rust uppsala runs/xml-uppsala-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
