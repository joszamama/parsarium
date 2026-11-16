# extract-zip — ZIP / JavaScript

Pinned release: `2.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/extract-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript extract_zip
python3 parsarium.py run zip javascript extract_zip controls/zip/hello.zip
python3 parsarium.py replay zip javascript extract_zip CORPUS_DIR runs/zip-extract_zip-replay
python3 parsarium.py afl build zip javascript extract_zip
python3 parsarium.py afl prepare zip javascript extract_zip runs/zip-extract_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
