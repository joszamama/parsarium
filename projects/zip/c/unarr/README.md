# unarr — ZIP / C

Pinned release: `1.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/c/unarr/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip c unarr
python3 parsarium.py run zip c unarr controls/zip/hello.zip
python3 parsarium.py replay zip c unarr CORPUS_DIR runs/zip-unarr-replay
python3 parsarium.py afl build zip c unarr
python3 parsarium.py afl prepare zip c unarr runs/zip-unarr-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
