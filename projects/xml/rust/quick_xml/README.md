# quick-xml — XML / Rust

Pinned release: `0.42.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/rust/quick-xml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml rust quick_xml
python3 parsarium.py run xml rust quick_xml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml rust quick_xml CORPUS_DIR runs/xml-quick_xml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml rust quick_xml
python3 parsarium.py afl prepare xml rust quick_xml runs/xml-quick_xml-afl --fandango 100
python3 parsarium.py afl run runs/xml-quick_xml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
