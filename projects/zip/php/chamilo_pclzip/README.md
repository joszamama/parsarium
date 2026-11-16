# chamilo/pclzip — ZIP / PHP

Pinned release: `v2.8.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/chamilo-pclzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php chamilo_pclzip
python3 parsarium.py run zip php chamilo_pclzip controls/zip/hello.zip
python3 parsarium.py replay zip php chamilo_pclzip CORPUS_DIR runs/zip-chamilo_pclzip-replay
python3 parsarium.py afl build zip php chamilo_pclzip
python3 parsarium.py afl prepare zip php chamilo_pclzip runs/zip-chamilo_pclzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
