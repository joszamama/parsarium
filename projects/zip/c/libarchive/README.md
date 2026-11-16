# libarchive — ZIP / C

Pinned release: `3.8.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/c/libarchive/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip c libarchive
python3 parsarium.py run zip c libarchive controls/zip/hello.zip
python3 parsarium.py replay zip c libarchive CORPUS_DIR runs/zip-libarchive-replay
python3 parsarium.py afl build zip c libarchive
python3 parsarium.py afl prepare zip c libarchive runs/zip-libarchive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
