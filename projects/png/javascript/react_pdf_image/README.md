# @react-pdf/image — PNG / JavaScript

Pinned release: `3.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/react-pdf-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript react_pdf_image
python3 parsarium.py run png javascript react_pdf_image controls/png/red-green.png
python3 parsarium.py replay png javascript react_pdf_image CORPUS_DIR runs/png-react_pdf_image-replay
python3 parsarium.py afl build png javascript react_pdf_image
python3 parsarium.py afl prepare png javascript react_pdf_image runs/png-react_pdf_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
