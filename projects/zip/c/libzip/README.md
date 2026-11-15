# libzip — ZIP / C

Pinned release: `1.12.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/c/libzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip c libzip
python3 parsarium.py run zip c libzip controls/zip/hello.zip
python3 parsarium.py replay zip c libzip CORPUS_DIR runs/zip-libzip-replay
python3 parsarium.py afl build zip c libzip
python3 parsarium.py afl prepare zip c libzip runs/zip-libzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
