# tess4j-pdfbox — PDF / Java

Pinned release: `5.20.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/tess4j-pdfbox/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java tess4j_pdfbox
python3 parsarium.py run pdf java tess4j_pdfbox controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java tess4j_pdfbox CORPUS_DIR runs/pdf-tess4j_pdfbox-replay
python3 parsarium.py afl build pdf java tess4j_pdfbox
python3 parsarium.py afl prepare pdf java tess4j_pdfbox runs/pdf-tess4j_pdfbox-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
