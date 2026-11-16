# @jsquash/png — PNG / JavaScript

Pinned release: `3.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/jsquash-png/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript jsquash_png
python3 parsarium.py run png javascript jsquash_png controls/png/red-green.png
python3 parsarium.py replay png javascript jsquash_png CORPUS_DIR runs/png-jsquash_png-replay
python3 parsarium.py afl build png javascript jsquash_png
python3 parsarium.py afl prepare png javascript jsquash_png runs/png-jsquash_png-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
