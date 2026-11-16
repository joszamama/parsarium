# upng-js — PNG / JavaScript

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/upng-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript upng_js
python3 parsarium.py run png javascript upng_js controls/png/red-green.png
python3 parsarium.py replay png javascript upng_js CORPUS_DIR runs/png-upng_js-replay
python3 parsarium.py afl build png javascript upng_js
python3 parsarium.py afl prepare png javascript upng_js runs/png-upng_js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
