# zipfile36 — ZIP / Python

Pinned release: `0.1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/zipfile36/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python zipfile36
python3 parsarium.py run zip python zipfile36 controls/zip/hello.zip
python3 parsarium.py replay zip python zipfile36 CORPUS_DIR runs/zip-zipfile36-replay
python3 parsarium.py afl build zip python zipfile36
python3 parsarium.py afl prepare zip python zipfile36 runs/zip-zipfile36-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
