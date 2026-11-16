# alchemy/zippy — ZIP / PHP

Pinned release: `2.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/alchemy-zippy/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php alchemy_zippy
python3 parsarium.py run zip php alchemy_zippy controls/zip/hello.zip
python3 parsarium.py replay zip php alchemy_zippy CORPUS_DIR runs/zip-alchemy_zippy-replay
python3 parsarium.py afl build zip php alchemy_zippy
python3 parsarium.py afl prepare zip php alchemy_zippy runs/zip-alchemy_zippy-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
