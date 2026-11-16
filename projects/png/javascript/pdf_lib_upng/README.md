# @pdf-lib/upng — PNG / JavaScript

Pinned release: `1.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/pdf-lib-upng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript pdf_lib_upng
python3 parsarium.py run png javascript pdf_lib_upng controls/png/red-green.png
python3 parsarium.py replay png javascript pdf_lib_upng CORPUS_DIR runs/png-pdf_lib_upng-replay
python3 parsarium.py afl build png javascript pdf_lib_upng
python3 parsarium.py afl prepare png javascript pdf_lib_upng runs/png-pdf_lib_upng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
