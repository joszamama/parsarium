# @react-pdf/png-js — PNG / JavaScript

Pinned release: `3.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/react-pdf-png-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript react_pdf_png_js
python3 parsarium.py run png javascript react_pdf_png_js controls/png/red-green.png
python3 parsarium.py replay png javascript react_pdf_png_js CORPUS_DIR runs/png-react_pdf_png_js-replay
python3 parsarium.py afl build png javascript react_pdf_png_js
python3 parsarium.py afl prepare png javascript react_pdf_png_js runs/png-react_pdf_png_js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
