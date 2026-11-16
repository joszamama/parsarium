# aplus/image — PNG / PHP

Pinned release: `v3.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/aplus-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php aplus_image
python3 parsarium.py run png php aplus_image controls/png/red-green.png
python3 parsarium.py replay png php aplus_image CORPUS_DIR runs/png-aplus_image-replay
python3 parsarium.py afl build png php aplus_image
python3 parsarium.py afl prepare png php aplus_image runs/png-aplus_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
