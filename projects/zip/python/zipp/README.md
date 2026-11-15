# zipp — ZIP / Python

Pinned release: `4.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/zipp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python zipp
python3 parsarium.py run zip python zipp controls/zip/hello.zip
python3 parsarium.py replay zip python zipp CORPUS_DIR runs/zip-zipp-replay
python3 parsarium.py afl build zip python zipp
python3 parsarium.py afl prepare zip python zipp runs/zip-zipp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
