# fs — ZIP / Python

Pinned release: `2.4.16`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/fs/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python fs
python3 parsarium.py run zip python fs controls/zip/hello.zip
python3 parsarium.py replay zip python fs CORPUS_DIR runs/zip-fs-replay
python3 parsarium.py afl build zip python fs
python3 parsarium.py afl prepare zip python fs runs/zip-fs-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
