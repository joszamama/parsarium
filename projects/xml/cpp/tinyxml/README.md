# tinyxml — XML / C++

Pinned release: `2.6.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/cpp/tinyxml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml cpp tinyxml
python3 parsarium.py run xml cpp tinyxml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml cpp tinyxml CORPUS_DIR runs/xml-tinyxml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml cpp tinyxml
python3 parsarium.py afl prepare xml cpp tinyxml runs/xml-tinyxml-afl --fandango 100
python3 parsarium.py afl run runs/xml-tinyxml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
