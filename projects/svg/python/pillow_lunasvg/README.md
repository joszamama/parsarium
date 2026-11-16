# pillow-lunasvg — SVG / Python

Pinned release: `0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/pillow-lunasvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python pillow_lunasvg
python3 parsarium.py run svg python pillow_lunasvg controls/svg/red-green.svg
python3 parsarium.py replay svg python pillow_lunasvg CORPUS_DIR runs/svg-pillow_lunasvg-replay
python3 parsarium.py afl build svg python pillow_lunasvg
python3 parsarium.py afl prepare svg python pillow_lunasvg runs/svg-pillow_lunasvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
