# pdfnano — PDF / JavaScript

Pinned release: `0.2.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/pdfnano/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript pdfnano
python3 parsarium.py run pdf javascript pdfnano controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript pdfnano CORPUS_DIR runs/pdf-pdfnano-replay
python3 parsarium.py afl build pdf javascript pdfnano
python3 parsarium.py afl prepare pdf javascript pdfnano runs/pdf-pdfnano-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
