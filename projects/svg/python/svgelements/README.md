# svgelements — SVG / Python

Pinned release: `1.9.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/svgelements/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python svgelements
python3 parsarium.py run svg python svgelements controls/svg/red-green.svg
python3 parsarium.py replay svg python svgelements CORPUS_DIR runs/svg-svgelements-replay
python3 parsarium.py afl build svg python svgelements
python3 parsarium.py afl prepare svg python svgelements runs/svg-svgelements-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
