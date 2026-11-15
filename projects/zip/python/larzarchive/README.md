# larzarchive — ZIP / Python

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/larzarchive/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python larzarchive
python3 parsarium.py run zip python larzarchive controls/zip/hello.zip
python3 parsarium.py replay zip python larzarchive CORPUS_DIR runs/zip-larzarchive-replay
python3 parsarium.py afl build zip python larzarchive
python3 parsarium.py afl prepare zip python larzarchive runs/zip-larzarchive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
