# sabre/xml — XML / PHP

Pinned release: `4.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/php/sabre-xml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml php sabre_xml
python3 parsarium.py run xml php sabre_xml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php sabre_xml CORPUS_DIR runs/xml-sabre_xml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml php sabre_xml
python3 parsarium.py afl prepare xml php sabre_xml runs/xml-sabre_xml-afl --fandango 100
python3 parsarium.py afl run runs/xml-sabre_xml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** The pinned base image does not bundle php-fuzzer; replay is per case and AFL++ uses the one-shot native XMLReader/libxml2 overlay.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
