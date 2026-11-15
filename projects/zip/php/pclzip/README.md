# pclzip/pclzip — ZIP / PHP

Pinned release: `2.8.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/pclzip-pclzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php pclzip
python3 parsarium.py run zip php pclzip controls/zip/hello.zip
python3 parsarium.py replay zip php pclzip CORPUS_DIR runs/zip-pclzip-replay
python3 parsarium.py afl build zip php pclzip
python3 parsarium.py afl prepare zip php pclzip runs/zip-pclzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
