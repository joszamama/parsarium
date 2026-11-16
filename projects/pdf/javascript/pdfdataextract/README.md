# pdfdataextract — PDF / JavaScript

Pinned release: `4.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/pdfdataextract/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript pdfdataextract
python3 parsarium.py run pdf javascript pdfdataextract controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript pdfdataextract CORPUS_DIR runs/pdf-pdfdataextract-replay
python3 parsarium.py afl build pdf javascript pdfdataextract
python3 parsarium.py afl prepare pdf javascript pdfdataextract runs/pdf-pdfdataextract-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
