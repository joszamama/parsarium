# untangle — XML / Python

Pinned release: `1.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/python/untangle/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml python untangle
python3 parsarium.py run xml python untangle controls/xml/catalog-ns.xml
python3 parsarium.py replay xml python untangle CORPUS_DIR runs/xml-untangle-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml python untangle
python3 parsarium.py afl prepare xml python untangle runs/xml-untangle-afl --fandango 100
python3 parsarium.py afl run runs/xml-untangle-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
