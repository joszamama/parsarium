# @zip.js/zip.js — ZIP / JavaScript

Pinned release: `2.24.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/zip-js-zip-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript zip_js_zip_js
python3 parsarium.py run zip javascript zip_js_zip_js controls/zip/hello.zip
python3 parsarium.py replay zip javascript zip_js_zip_js CORPUS_DIR runs/zip-zip_js_zip_js-replay
python3 parsarium.py afl build zip javascript zip_js_zip_js
python3 parsarium.py afl prepare zip javascript zip_js_zip_js runs/zip-zip_js_zip_js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
