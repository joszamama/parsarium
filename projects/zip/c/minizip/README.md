# minizip — ZIP / C

Pinned release: `1.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/c/minizip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip c minizip
python3 parsarium.py run zip c minizip controls/zip/hello.zip
python3 parsarium.py replay zip c minizip CORPUS_DIR runs/zip-minizip-replay
python3 parsarium.py afl build zip c minizip
python3 parsarium.py afl prepare zip c minizip runs/zip-minizip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
