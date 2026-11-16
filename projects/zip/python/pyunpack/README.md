# pyunpack — ZIP / Python

Pinned release: `0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/pyunpack/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python pyunpack
python3 parsarium.py run zip python pyunpack controls/zip/hello.zip
python3 parsarium.py replay zip python pyunpack CORPUS_DIR runs/zip-pyunpack-replay
python3 parsarium.py afl build zip python pyunpack
python3 parsarium.py afl prepare zip python pyunpack runs/zip-pyunpack-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
