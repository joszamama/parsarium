# graphicsmagick — PNG / C

Pinned release: `1.3.49`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/graphicsmagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c graphicsmagick
python3 parsarium.py run png c graphicsmagick controls/png/red-green.png
python3 parsarium.py replay png c graphicsmagick CORPUS_DIR runs/png-graphicsmagick-replay
python3 parsarium.py afl build png c graphicsmagick
python3 parsarium.py afl prepare png c graphicsmagick runs/png-graphicsmagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
