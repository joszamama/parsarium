# jimp — PNG / JavaScript

Pinned release: `1.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/jimp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript jimp
python3 parsarium.py run png javascript jimp controls/png/red-green.png
python3 parsarium.py replay png javascript jimp CORPUS_DIR runs/png-jimp-replay
python3 parsarium.py afl build png javascript jimp
python3 parsarium.py afl prepare png javascript jimp runs/png-jimp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
