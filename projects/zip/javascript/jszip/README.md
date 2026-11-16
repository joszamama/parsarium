# jszip — ZIP / JavaScript

Pinned release: `3.10.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/jszip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript jszip
python3 parsarium.py run zip javascript jszip controls/zip/hello.zip
python3 parsarium.py replay zip javascript jszip CORPUS_DIR runs/zip-jszip-replay
python3 parsarium.py afl build zip javascript jszip
python3 parsarium.py afl prepare zip javascript jszip runs/zip-jszip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
