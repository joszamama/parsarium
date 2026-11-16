# libarchive — ZIP / C++

Pinned release: `3.8.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/libarchive/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp libarchive
python3 parsarium.py run zip cpp libarchive controls/zip/hello.zip
python3 parsarium.py replay zip cpp libarchive CORPUS_DIR runs/zip-libarchive-replay
python3 parsarium.py afl build zip cpp libarchive
python3 parsarium.py afl prepare zip cpp libarchive runs/zip-libarchive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
