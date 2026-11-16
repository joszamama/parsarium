# matomo/decompress — ZIP / PHP

Pinned release: `3.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/matomo-decompress/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php matomo_decompress
python3 parsarium.py run zip php matomo_decompress controls/zip/hello.zip
python3 parsarium.py replay zip php matomo_decompress CORPUS_DIR runs/zip-matomo_decompress-replay
python3 parsarium.py afl build zip php matomo_decompress
python3 parsarium.py afl prepare zip php matomo_decompress runs/zip-matomo_decompress-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
