# unzipper-esm — ZIP / JavaScript

Pinned release: `0.13.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/unzipper-esm/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript unzipper_esm
python3 parsarium.py run zip javascript unzipper_esm controls/zip/hello.zip
python3 parsarium.py replay zip javascript unzipper_esm CORPUS_DIR runs/zip-unzipper_esm-replay
python3 parsarium.py afl build zip javascript unzipper_esm
python3 parsarium.py afl prepare zip javascript unzipper_esm runs/zip-unzipper_esm-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
