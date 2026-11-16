# unarr — ZIP / C++

Pinned release: `1.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/unarr/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp unarr
python3 parsarium.py run zip cpp unarr controls/zip/hello.zip
python3 parsarium.py replay zip cpp unarr CORPUS_DIR runs/zip-unarr-replay
python3 parsarium.py afl build zip cpp unarr
python3 parsarium.py afl prepare zip cpp unarr runs/zip-unarr-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
