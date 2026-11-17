# librsvg — SVG / C

Pinned release: `2.63.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/librsvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg c librsvg
python3 parsarium.py run svg c librsvg controls/svg/red-green.svg
python3 parsarium.py replay svg c librsvg CORPUS_DIR runs/svg-librsvg-replay
python3 parsarium.py afl build svg c librsvg
python3 parsarium.py afl prepare svg c librsvg runs/svg-librsvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
