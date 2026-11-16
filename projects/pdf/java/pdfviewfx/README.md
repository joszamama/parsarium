# pdfviewfx — PDF / Java

Pinned release: `3.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/pdfviewfx/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java pdfviewfx
python3 parsarium.py run pdf java pdfviewfx controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java pdfviewfx CORPUS_DIR runs/pdf-pdfviewfx-replay
python3 parsarium.py afl build pdf java pdfviewfx
python3 parsarium.py afl prepare pdf java pdfviewfx runs/pdf-pdfviewfx-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
