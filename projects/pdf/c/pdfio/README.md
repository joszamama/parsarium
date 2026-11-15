# pdfio — PDF / C

Pinned release: `1.6.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/c/pdfio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf c pdfio
python3 parsarium.py run pdf c pdfio controls/pdf/one-page.pdf
python3 parsarium.py replay pdf c pdfio CORPUS_DIR runs/pdf-pdfio-replay
python3 parsarium.py afl build pdf c pdfio
python3 parsarium.py afl prepare pdf c pdfio runs/pdf-pdfio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
