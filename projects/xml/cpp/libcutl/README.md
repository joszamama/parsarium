# libcutl — XML / C++

Pinned release: `1.10.0+ds1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/cpp/libcutl/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml cpp libcutl
python3 parsarium.py run xml cpp libcutl controls/xml/catalog-ns.xml
python3 parsarium.py replay xml cpp libcutl CORPUS_DIR runs/xml-libcutl-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml cpp libcutl
python3 parsarium.py afl prepare xml cpp libcutl runs/xml-libcutl-afl --fandango 100
python3 parsarium.py afl run runs/xml-libcutl-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
