# tspdf — PDF / C++

Pinned release: `0.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/cpp/tspdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp tspdf
python3 parsarium.py run pdf cpp tspdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp tspdf CORPUS_DIR runs/pdf-tspdf-replay
python3 parsarium.py afl build pdf cpp tspdf
python3 parsarium.py afl prepare pdf cpp tspdf runs/pdf-tspdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
