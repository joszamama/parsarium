# pdf4qt — PDF / C++

Pinned release: `1.6.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/cpp/pdf4qt/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp pdf4qt
python3 parsarium.py run pdf cpp pdf4qt controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp pdf4qt CORPUS_DIR runs/pdf-pdf4qt-replay
python3 parsarium.py afl build pdf cpp pdf4qt
python3 parsarium.py afl prepare pdf cpp pdf4qt runs/pdf-pdf4qt-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
