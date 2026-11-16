# pyzipper — ZIP / Python

Pinned release: `0.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/pyzipper/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python pyzipper
python3 parsarium.py run zip python pyzipper controls/zip/hello.zip
python3 parsarium.py replay zip python pyzipper CORPUS_DIR runs/zip-pyzipper-replay
python3 parsarium.py afl build zip python pyzipper
python3 parsarium.py afl prepare zip python pyzipper runs/zip-pyzipper-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
