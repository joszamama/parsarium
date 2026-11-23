# xpp3 — XML / Java

Pinned release: `1.1.4c`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/java/xpp3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml java xpp3
python3 parsarium.py run xml java xpp3 controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java xpp3 CORPUS_DIR runs/xml-xpp3-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml java xpp3
python3 parsarium.py afl prepare xml java xpp3 runs/xml-xpp3-afl --fandango 100
python3 parsarium.py afl run runs/xml-xpp3-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
