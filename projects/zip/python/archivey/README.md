# archivey — ZIP / Python

Pinned release: `0.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/archivey/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python archivey
python3 parsarium.py run zip python archivey controls/zip/hello.zip
python3 parsarium.py replay zip python archivey CORPUS_DIR runs/zip-archivey-replay
python3 parsarium.py afl build zip python archivey
python3 parsarium.py afl prepare zip python archivey runs/zip-archivey-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
