# pdfbox — PNG / Java

Pinned release: `3.0.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/pdfbox/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java pdfbox
python3 parsarium.py run png java pdfbox controls/png/red-green.png
python3 parsarium.py replay png java pdfbox CORPUS_DIR runs/png-pdfbox-replay
python3 parsarium.py afl build png java pdfbox
python3 parsarium.py afl prepare png java pdfbox runs/png-pdfbox-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
