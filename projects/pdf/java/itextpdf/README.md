# itextpdf — PDF / Java

Pinned release: `5.5.13`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/itextpdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java itextpdf
python3 parsarium.py run pdf java itextpdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java itextpdf CORPUS_DIR runs/pdf-itextpdf-replay
python3 parsarium.py afl build pdf java itextpdf
python3 parsarium.py afl prepare pdf java itextpdf runs/pdf-itextpdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
