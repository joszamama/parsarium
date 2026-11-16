# pizzip — ZIP / JavaScript

Pinned release: `3.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/pizzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript pizzip
python3 parsarium.py run zip javascript pizzip controls/zip/hello.zip
python3 parsarium.py replay zip javascript pizzip CORPUS_DIR runs/zip-pizzip-replay
python3 parsarium.py afl build zip javascript pizzip
python3 parsarium.py afl prepare zip javascript pizzip runs/zip-pizzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
