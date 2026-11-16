# icepdf8 — PDF / Java

Pinned release: `8.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/icepdf8/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java icepdf8
python3 parsarium.py run pdf java icepdf8 controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java icepdf8 CORPUS_DIR runs/pdf-icepdf8-replay
python3 parsarium.py afl build pdf java icepdf8
python3 parsarium.py afl prepare pdf java icepdf8 runs/pdf-icepdf8-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
