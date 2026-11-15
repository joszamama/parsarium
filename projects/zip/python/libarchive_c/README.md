# libarchive-c — ZIP / Python

Pinned release: `5.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/libarchive-c/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python libarchive_c
python3 parsarium.py run zip python libarchive_c controls/zip/hello.zip
python3 parsarium.py replay zip python libarchive_c CORPUS_DIR runs/zip-libarchive_c-replay
python3 parsarium.py afl build zip python libarchive_c
python3 parsarium.py afl prepare zip python libarchive_c runs/zip-libarchive_c-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
