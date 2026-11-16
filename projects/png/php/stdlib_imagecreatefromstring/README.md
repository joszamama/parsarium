# php-imagecreatefromstring — PNG / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/png/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build png php stdlib_imagecreatefromstring
python3 parsarium.py run png php stdlib_imagecreatefromstring controls/png/red-green.png
python3 parsarium.py replay png php stdlib_imagecreatefromstring CORPUS_DIR runs/png-stdlib_imagecreatefromstring-replay
python3 parsarium.py afl build png php stdlib_imagecreatefromstring
python3 parsarium.py afl prepare png php stdlib_imagecreatefromstring runs/png-stdlib_imagecreatefromstring-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
