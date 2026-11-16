# graphicsmagick — SVG / C

Pinned release: `1.3.49`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/graphicsmagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg c graphicsmagick
python3 parsarium.py run svg c graphicsmagick controls/svg/red-green.svg
python3 parsarium.py replay svg c graphicsmagick CORPUS_DIR runs/svg-graphicsmagick-replay
python3 parsarium.py afl build svg c graphicsmagick
python3 parsarium.py afl prepare svg c graphicsmagick runs/svg-graphicsmagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
