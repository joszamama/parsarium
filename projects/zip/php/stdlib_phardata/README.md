# php-phardata — ZIP / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/zip/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build zip php stdlib_phardata
python3 parsarium.py run zip php stdlib_phardata controls/zip/hello.zip
python3 parsarium.py replay zip php stdlib_phardata CORPUS_DIR runs/zip-stdlib_phardata-replay
python3 parsarium.py afl build zip php stdlib_phardata
python3 parsarium.py afl prepare zip php stdlib_phardata runs/zip-stdlib_phardata-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
