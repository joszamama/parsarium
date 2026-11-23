# xml.etree.ElementTree — XML / Python

Pinned release: `3.14.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/python/xml/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build xml python stdlib_elementtree
python3 parsarium.py run xml python stdlib_elementtree controls/xml/two-items.xml
python3 parsarium.py replay xml python stdlib_elementtree CORPUS_DIR runs/xml-stdlib_elementtree-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml python stdlib_elementtree
python3 parsarium.py afl prepare xml python stdlib_elementtree runs/xml-stdlib_elementtree-afl --fandango 100
python3 parsarium.py afl run runs/xml-stdlib_elementtree-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
