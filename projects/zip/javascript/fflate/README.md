# fflate — ZIP / JavaScript

Pinned release: `0.8.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/fflate/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript fflate
python3 parsarium.py run zip javascript fflate controls/zip/hello.zip
python3 parsarium.py replay zip javascript fflate CORPUS_DIR runs/zip-fflate-replay
python3 parsarium.py afl build zip javascript fflate
python3 parsarium.py afl prepare zip javascript fflate runs/zip-fflate-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
