# minizip-ng — ZIP / C

Pinned release: `4.2.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/c/minizip-ng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip c minizip-ng
python3 parsarium.py run zip c minizip-ng controls/zip/hello.zip
python3 parsarium.py replay zip c minizip-ng CORPUS_DIR runs/zip-minizip-ng-replay
python3 parsarium.py afl build zip c minizip-ng
python3 parsarium.py afl prepare zip c minizip-ng runs/zip-minizip-ng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
