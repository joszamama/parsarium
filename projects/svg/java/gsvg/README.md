# gsvg — SVG / Java

Pinned release: `1.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/gsvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java gsvg
python3 parsarium.py run svg java gsvg controls/svg/red-green.svg
python3 parsarium.py replay svg java gsvg CORPUS_DIR runs/svg-gsvg-replay
python3 parsarium.py afl build svg java gsvg
python3 parsarium.py afl prepare svg java gsvg runs/svg-gsvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
