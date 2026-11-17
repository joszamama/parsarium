# ghostscript — PDF / C

Pinned release: `10.08.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/c/ghostscript/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf c ghostscript
python3 parsarium.py run pdf c ghostscript controls/pdf/one-page.pdf
python3 parsarium.py replay pdf c ghostscript CORPUS_DIR runs/pdf-ghostscript-replay
python3 parsarium.py afl build pdf c ghostscript
python3 parsarium.py afl prepare pdf c ghostscript runs/pdf-ghostscript-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
