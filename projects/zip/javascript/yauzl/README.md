# yauzl — ZIP / JavaScript

Pinned release: `3.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/yauzl/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript yauzl
python3 parsarium.py run zip javascript yauzl controls/zip/hello.zip
python3 parsarium.py replay zip javascript yauzl CORPUS_DIR runs/zip-yauzl-replay
python3 parsarium.py afl build zip javascript yauzl
python3 parsarium.py afl prepare zip javascript yauzl runs/zip-yauzl-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
