# adm-zip — ZIP / JavaScript

Pinned release: `0.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/adm-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript adm_zip
python3 parsarium.py run zip javascript adm_zip controls/zip/hello.zip
python3 parsarium.py replay zip javascript adm_zip CORPUS_DIR runs/zip-adm_zip-replay
python3 parsarium.py afl build zip javascript adm_zip
python3 parsarium.py afl prepare zip javascript adm_zip runs/zip-adm_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
