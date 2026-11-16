# sqlite — ZIP / C

Pinned release: `3.54.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/c/sqlite/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip c sqlite
python3 parsarium.py run zip c sqlite controls/zip/hello.zip
python3 parsarium.py replay zip c sqlite CORPUS_DIR runs/zip-sqlite-replay
python3 parsarium.py afl build zip c sqlite
python3 parsarium.py afl prepare zip c sqlite runs/zip-sqlite-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
