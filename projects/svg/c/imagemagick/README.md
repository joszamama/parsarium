# imagemagick — SVG / C

Pinned release: `7.1.2-35`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/imagemagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg c imagemagick
python3 parsarium.py run svg c imagemagick controls/svg/red-green.svg
python3 parsarium.py replay svg c imagemagick CORPUS_DIR runs/svg-imagemagick-replay
python3 parsarium.py afl build svg c imagemagick
python3 parsarium.py afl prepare svg c imagemagick runs/svg-imagemagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
