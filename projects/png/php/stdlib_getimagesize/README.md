# php-getimagesize — PNG / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/png/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build png php stdlib_getimagesize
python3 parsarium.py run png php stdlib_getimagesize controls/png/red-green.png
python3 parsarium.py replay png php stdlib_getimagesize CORPUS_DIR runs/png-stdlib_getimagesize-replay
python3 parsarium.py afl build png php stdlib_getimagesize
python3 parsarium.py afl prepare png php stdlib_getimagesize runs/png-stdlib_getimagesize-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
