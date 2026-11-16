# pikepdf — PDF / Python

Pinned release: `10.18.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pikepdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pikepdf
python3 parsarium.py run pdf python pikepdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pikepdf CORPUS_DIR runs/pdf-pikepdf-replay
python3 parsarium.py afl build pdf python pikepdf
python3 parsarium.py afl prepare pdf python pikepdf runs/pdf-pikepdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
