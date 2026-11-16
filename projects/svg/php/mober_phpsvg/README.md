# mober/phpsvg — SVG / PHP

Pinned release: `v6.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/mober-phpsvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php mober_phpsvg
python3 parsarium.py run svg php mober_phpsvg controls/svg/red-green.svg
python3 parsarium.py replay svg php mober_phpsvg CORPUS_DIR runs/svg-mober_phpsvg-replay
python3 parsarium.py afl build svg php mober_phpsvg
python3 parsarium.py afl prepare svg php mober_phpsvg runs/svg-mober_phpsvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
