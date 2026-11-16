# minizip-ng — ZIP / C++

Pinned release: `4.2.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/minizip-ng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp minizip-ng
python3 parsarium.py run zip cpp minizip-ng controls/zip/hello.zip
python3 parsarium.py replay zip cpp minizip-ng CORPUS_DIR runs/zip-minizip-ng-replay
python3 parsarium.py afl build zip cpp minizip-ng
python3 parsarium.py afl prepare zip cpp minizip-ng runs/zip-minizip-ng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
