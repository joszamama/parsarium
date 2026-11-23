# rxp — XML / C

Pinned release: `1.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/c/rxp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml c rxp
python3 parsarium.py run xml c rxp controls/xml/catalog-ns.xml
python3 parsarium.py replay xml c rxp CORPUS_DIR runs/xml-rxp-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml c rxp
python3 parsarium.py afl prepare xml c rxp runs/xml-rxp-afl --fandango 100
python3 parsarium.py afl run runs/xml-rxp-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** Two valid UTF-8 XML 1.0 controls without DOCTYPE establish RXP's namespace-resolved element, attribute and character-data bits for them only (no validation, no DTD processing beyond defaults). No xmlns declaration count is reported. RXP opens documents by system identifier, so the harness writes the local bytes to a private temporary file. The library includes an HTTP storage layer (src/http.c) that local files do not use. The expected outputs come from controls/xml/check_controls.py (pyexpat), a different family.
