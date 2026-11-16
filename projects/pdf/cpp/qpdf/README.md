# qpdf — PDF / C++

Pinned release: `12.4.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/cpp/qpdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp qpdf
python3 parsarium.py run pdf cpp qpdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp qpdf CORPUS_DIR runs/pdf-qpdf-replay
python3 parsarium.py afl build pdf cpp qpdf
python3 parsarium.py afl prepare pdf cpp qpdf runs/pdf-qpdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
