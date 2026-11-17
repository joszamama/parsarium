# podofo — PDF / C++

Pinned release: `1.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/cpp/podofo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp podofo
python3 parsarium.py run pdf cpp podofo controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp podofo CORPUS_DIR runs/pdf-podofo-replay
python3 parsarium.py afl build pdf cpp podofo
python3 parsarium.py afl prepare pdf cpp podofo runs/pdf-podofo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
