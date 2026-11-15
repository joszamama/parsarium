# pdfio — PDF / C++

Pinned release: `1.6.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/cpp/pdfio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp pdfio
python3 parsarium.py run pdf cpp pdfio controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp pdfio CORPUS_DIR runs/pdf-pdfio-replay
python3 parsarium.py afl build pdf cpp pdfio
python3 parsarium.py afl prepare pdf cpp pdfio runs/pdf-pdfio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
