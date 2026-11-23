# minidom — XML / Rust

Pinned release: `0.19.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/rust/minidom/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml rust minidom
python3 parsarium.py run xml rust minidom controls/xml/catalog-ns.xml
python3 parsarium.py replay xml rust minidom CORPUS_DIR runs/xml-minidom-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml rust minidom
python3 parsarium.py afl prepare xml rust minidom runs/xml-minidom-afl --fandango 100
python3 parsarium.py afl run runs/xml-minidom-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** DOM wrapper over rxml's RawReader; shares the selected rxml lexer and raw parser family. minidom resolves prefixes itself in TreeBuilder. Inherits rxml's restricted XML 1.0 subset: comments and processing instructions are rejected by default, so the second control is order-default-ns-restricted.xml.
