# zipc — ZIP / C

Pinned release: `v1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/c/zipc/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip c zipc
python3 parsarium.py run zip c zipc controls/zip/hello.zip
python3 parsarium.py replay zip c zipc CORPUS_DIR runs/zip-zipc-replay
python3 parsarium.py afl build zip c zipc
python3 parsarium.py afl prepare zip c zipc runs/zip-zipc-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
