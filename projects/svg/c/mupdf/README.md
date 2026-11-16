# mupdf — SVG / C

Pinned release: `1.28.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/mupdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg c mupdf
python3 parsarium.py run svg c mupdf controls/svg/red-green.svg
python3 parsarium.py replay svg c mupdf CORPUS_DIR runs/svg-mupdf-replay
python3 parsarium.py afl build svg c mupdf
python3 parsarium.py afl prepare svg c mupdf runs/svg-mupdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
