# patool — ZIP / Python

Pinned release: `4.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/patool/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python patool
python3 parsarium.py run zip python patool controls/zip/hello.zip
python3 parsarium.py replay zip python patool CORPUS_DIR runs/zip-patool-replay
python3 parsarium.py afl build zip python patool
python3 parsarium.py afl prepare zip python patool runs/zip-patool-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
