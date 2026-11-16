# sybio/image-workshop — PNG / PHP

Pinned release: `3.0.0-beta1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/sybio-image-workshop/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php sybio_image_workshop
python3 parsarium.py run png php sybio_image_workshop controls/png/red-green.png
python3 parsarium.py replay png php sybio_image_workshop CORPUS_DIR runs/png-sybio_image_workshop-replay
python3 parsarium.py afl build png php sybio_image_workshop
python3 parsarium.py afl prepare png php sybio_image_workshop runs/png-sybio_image_workshop-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
