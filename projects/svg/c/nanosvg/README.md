# nanosvg — SVG / C

Pinned release: `2023-12-29`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/nanosvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg c nanosvg
python3 parsarium.py run svg c nanosvg controls/svg/red-green.svg
python3 parsarium.py replay svg c nanosvg CORPUS_DIR runs/svg-nanosvg-replay
python3 parsarium.py afl build svg c nanosvg
python3 parsarium.py afl prepare svg c nanosvg runs/svg-nanosvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
