# swinglabs-pdf-renderer — PDF / Java

Pinned release: `1.0.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/swinglabs-pdf-renderer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java swinglabs_pdf_renderer
python3 parsarium.py run pdf java swinglabs_pdf_renderer controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java swinglabs_pdf_renderer CORPUS_DIR runs/pdf-swinglabs_pdf_renderer-replay
python3 parsarium.py afl build pdf java swinglabs_pdf_renderer
python3 parsarium.py afl prepare pdf java swinglabs_pdf_renderer runs/pdf-swinglabs_pdf_renderer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
