# minizip — ZIP / C++

Pinned release: `1.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/minizip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp minizip
python3 parsarium.py run zip cpp minizip controls/zip/hello.zip
python3 parsarium.py replay zip cpp minizip CORPUS_DIR runs/zip-minizip-replay
python3 parsarium.py afl build zip cpp minizip
python3 parsarium.py afl prepare zip cpp minizip runs/zip-minizip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
