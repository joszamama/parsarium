# marc1706/fast-image-size — PNG / PHP

Pinned release: `v1.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/marc1706-fast-image-size/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php marc1706_fast_image_size
python3 parsarium.py run png php marc1706_fast_image_size controls/png/red-green.png
python3 parsarium.py replay png php marc1706_fast_image_size CORPUS_DIR runs/png-marc1706_fast_image_size-replay
python3 parsarium.py afl build png php marc1706_fast_image_size
python3 parsarium.py afl prepare png php marc1706_fast_image_size runs/png-marc1706_fast_image_size-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
