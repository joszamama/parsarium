# png-js — PNG / JavaScript

Pinned release: `2.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/png-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript png_js
python3 parsarium.py run png javascript png_js controls/png/red-green.png
python3 parsarium.py replay png javascript png_js CORPUS_DIR runs/png-png_js-replay
python3 parsarium.py afl build png javascript png_js
python3 parsarium.py afl prepare png javascript png_js runs/png-png_js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
