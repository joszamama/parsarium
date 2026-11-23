# xmlbeans — XML / Java

Pinned release: `5.4.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/java/xmlbeans/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml java xmlbeans
python3 parsarium.py run xml java xmlbeans controls/xml/catalog-ns.xml
python3 parsarium.py replay xml java xmlbeans CORPUS_DIR runs/xml-xmlbeans-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml java xmlbeans
python3 parsarium.py afl prepare xml java xmlbeans runs/xml-xmlbeans-afl --fandango 100
python3 parsarium.py afl run runs/xml-xmlbeans-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
