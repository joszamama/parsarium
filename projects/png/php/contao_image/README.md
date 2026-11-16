# contao/image — PNG / PHP

Pinned release: `1.2.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/contao-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php contao_image
python3 parsarium.py run png php contao_image controls/png/red-green.png
python3 parsarium.py replay png php contao_image CORPUS_DIR runs/png-contao_image-replay
python3 parsarium.py afl build png php contao_image
python3 parsarium.py afl prepare png php contao_image runs/png-contao_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
