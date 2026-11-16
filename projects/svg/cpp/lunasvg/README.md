# lunasvg — SVG / C++

Pinned release: `3.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/cpp/lunasvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg cpp lunasvg
python3 parsarium.py run svg cpp lunasvg controls/svg/red-green.svg
python3 parsarium.py replay svg cpp lunasvg CORPUS_DIR runs/svg-lunasvg-replay
python3 parsarium.py afl build svg cpp lunasvg
python3 parsarium.py afl prepare svg cpp lunasvg runs/svg-lunasvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
