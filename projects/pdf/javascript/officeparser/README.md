# officeparser — PDF / JavaScript

Pinned release: `8.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/officeparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript officeparser
python3 parsarium.py run pdf javascript officeparser controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript officeparser CORPUS_DIR runs/pdf-officeparser-replay
python3 parsarium.py afl build pdf javascript officeparser
python3 parsarium.py afl prepare pdf javascript officeparser runs/pdf-officeparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
