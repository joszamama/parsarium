# getimagesize — SVG / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/svg/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build svg php stdlib_getimagesize
python3 parsarium.py run svg php stdlib_getimagesize controls/svg/red-green.svg
python3 parsarium.py replay svg php stdlib_getimagesize CORPUS_DIR runs/svg-stdlib_getimagesize-replay
python3 parsarium.py afl build svg php stdlib_getimagesize
python3 parsarium.py afl prepare svg php stdlib_getimagesize runs/svg-stdlib_getimagesize-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
