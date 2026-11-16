# zipfile38 — ZIP / Python

Pinned release: `0.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/zipfile38/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python zipfile38
python3 parsarium.py run zip python zipfile38 controls/zip/hello.zip
python3 parsarium.py replay zip python zipfile38 CORPUS_DIR runs/zip-zipfile38-replay
python3 parsarium.py afl build zip python zipfile38
python3 parsarium.py afl prepare zip python zipfile38 runs/zip-zipfile38-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
