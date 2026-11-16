# pdfminer.six — PDF / Python

Pinned release: `20260107`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pdfminer-six/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pdfminer_six
python3 parsarium.py run pdf python pdfminer_six controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pdfminer_six CORPUS_DIR runs/pdf-pdfminer_six-replay
python3 parsarium.py afl build pdf python pdfminer_six
python3 parsarium.py afl prepare pdf python pdfminer_six runs/pdf-pdfminer_six-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
