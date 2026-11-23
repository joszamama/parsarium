# php-xmlreader — XML / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/xml/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build xml php stdlib_xmlreader
python3 parsarium.py run xml php stdlib_xmlreader controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php stdlib_xmlreader CORPUS_DIR runs/xml-stdlib_xmlreader-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml php stdlib_xmlreader
python3 parsarium.py afl prepare xml php stdlib_xmlreader runs/xml-stdlib_xmlreader-afl --fandango 100
python3 parsarium.py afl run runs/xml-stdlib_xmlreader-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
