# @zip.js/zip.js — ZIP / JavaScript

Pinned release: `2.24.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/zip-js-zip-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript zip_js_zip_js
python3 parsarium.py run zip javascript zip_js_zip_js controls/zip/hello.zip
python3 parsarium.py replay zip javascript zip_js_zip_js CORPUS_DIR runs/zip-zip_js_zip_js-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip javascript zip_js_zip_js
python3 parsarium.py afl prepare zip javascript zip_js_zip_js runs/zip-zip_js_zip_js-afl --fandango 100
python3 parsarium.py afl run runs/zip-zip_js_zip_js-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
