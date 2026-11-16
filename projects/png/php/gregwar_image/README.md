# gregwar/image — PNG / PHP

Pinned release: `v2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/gregwar-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php gregwar_image
python3 parsarium.py run png php gregwar_image controls/png/red-green.png
python3 parsarium.py replay png php gregwar_image CORPUS_DIR runs/png-gregwar_image-replay
python3 parsarium.py afl build png php gregwar_image
python3 parsarium.py afl prepare png php gregwar_image runs/png-gregwar_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
