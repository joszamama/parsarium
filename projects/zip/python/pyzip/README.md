# pyzip — ZIP / Python

Pinned release: `0.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/pyzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python pyzip
python3 parsarium.py run zip python pyzip controls/zip/hello.zip
python3 parsarium.py replay zip python pyzip CORPUS_DIR runs/zip-pyzip-replay
python3 parsarium.py afl build zip python pyzip
python3 parsarium.py afl prepare zip python pyzip runs/zip-pyzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
