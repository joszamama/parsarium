# poppler — PDF / C++

Pinned release: `26.11.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/cpp/poppler/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp poppler
python3 parsarium.py run pdf cpp poppler controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp poppler CORPUS_DIR runs/pdf-poppler-replay
python3 parsarium.py afl build pdf cpp poppler
python3 parsarium.py afl prepare pdf cpp poppler runs/pdf-poppler-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
