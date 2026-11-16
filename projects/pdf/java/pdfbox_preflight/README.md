# pdfbox-preflight — PDF / Java

Pinned release: `3.0.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/pdfbox-preflight/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java pdfbox_preflight
python3 parsarium.py run pdf java pdfbox_preflight controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java pdfbox_preflight CORPUS_DIR runs/pdf-pdfbox_preflight-replay
python3 parsarium.py afl build pdf java pdfbox_preflight
python3 parsarium.py afl prepare pdf java pdfbox_preflight runs/pdf-pdfbox_preflight-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
