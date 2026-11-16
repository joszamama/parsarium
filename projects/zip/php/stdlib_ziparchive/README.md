# php-ziparchive — ZIP / PHP

Pinned release: `8.5.12`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/php/zip/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build zip php stdlib_ziparchive
python3 parsarium.py run zip php stdlib_ziparchive controls/zip/hello.zip
python3 parsarium.py replay zip php stdlib_ziparchive CORPUS_DIR runs/zip-stdlib_ziparchive-replay
python3 parsarium.py afl build zip php stdlib_ziparchive
python3 parsarium.py afl prepare zip php stdlib_ziparchive runs/zip-stdlib_ziparchive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
