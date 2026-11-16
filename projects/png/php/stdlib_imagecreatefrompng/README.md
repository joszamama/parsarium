# php-imagecreatefrompng — PNG / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/png/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build png php stdlib_imagecreatefrompng
python3 parsarium.py run png php stdlib_imagecreatefrompng controls/png/red-green.png
python3 parsarium.py replay png php stdlib_imagecreatefrompng CORPUS_DIR runs/png-stdlib_imagecreatefrompng-replay
python3 parsarium.py afl build png php stdlib_imagecreatefrompng
python3 parsarium.py afl prepare png php stdlib_imagecreatefrompng runs/png-stdlib_imagecreatefrompng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
