# spatie/image — PNG / PHP

Pinned release: `3.9.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/spatie-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php spatie_image
python3 parsarium.py run png php spatie_image controls/png/red-green.png
python3 parsarium.py replay png php spatie_image CORPUS_DIR runs/png-spatie_image-replay
python3 parsarium.py afl build png php spatie_image
python3 parsarium.py afl prepare png php spatie_image runs/png-spatie_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
