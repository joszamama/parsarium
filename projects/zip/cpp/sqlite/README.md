# sqlite — ZIP / C++

Pinned release: `3.54.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/sqlite/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp sqlite
python3 parsarium.py run zip cpp sqlite controls/zip/hello.zip
python3 parsarium.py replay zip cpp sqlite CORPUS_DIR runs/zip-sqlite-replay
python3 parsarium.py afl build zip cpp sqlite
python3 parsarium.py afl prepare zip cpp sqlite runs/zip-sqlite-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
