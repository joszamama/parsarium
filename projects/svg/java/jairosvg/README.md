# jairosvg — SVG / Java

Pinned release: `1.0.16`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/jairosvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java jairosvg
python3 parsarium.py run svg java jairosvg controls/svg/red-green.svg
python3 parsarium.py replay svg java jairosvg CORPUS_DIR runs/svg-jairosvg-replay
python3 parsarium.py afl build svg java jairosvg
python3 parsarium.py afl prepare svg java jairosvg runs/svg-jairosvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
