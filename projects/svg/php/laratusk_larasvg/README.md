# laratusk/larasvg — SVG / PHP

Pinned release: `v2.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/laratusk-larasvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php laratusk_larasvg
python3 parsarium.py run svg php laratusk_larasvg controls/svg/red-green.svg
python3 parsarium.py replay svg php laratusk_larasvg CORPUS_DIR runs/svg-laratusk_larasvg-replay
python3 parsarium.py afl build svg php laratusk_larasvg
python3 parsarium.py afl prepare svg php laratusk_larasvg runs/svg-laratusk_larasvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
