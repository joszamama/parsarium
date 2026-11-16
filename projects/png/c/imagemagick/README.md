# imagemagick — PNG / C

Pinned release: `7.1.2-35`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/imagemagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c imagemagick
python3 parsarium.py run png c imagemagick controls/png/red-green.png
python3 parsarium.py replay png c imagemagick CORPUS_DIR runs/png-imagemagick-replay
python3 parsarium.py afl build png c imagemagick
python3 parsarium.py afl prepare png c imagemagick runs/png-imagemagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
