# atelier/svg — SVG / PHP

Pinned release: `v1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/atelier-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php atelier_svg
python3 parsarium.py run svg php atelier_svg controls/svg/red-green.svg
python3 parsarium.py replay svg php atelier_svg CORPUS_DIR runs/svg-atelier_svg-replay
python3 parsarium.py afl build svg php atelier_svg
python3 parsarium.py afl prepare svg php atelier_svg runs/svg-atelier_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
