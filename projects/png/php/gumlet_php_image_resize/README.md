# gumlet/php-image-resize — PNG / PHP

Pinned release: `3.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/gumlet-php-image-resize/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php gumlet_php_image_resize
python3 parsarium.py run png php gumlet_php_image_resize controls/png/red-green.png
python3 parsarium.py replay png php gumlet_php_image_resize CORPUS_DIR runs/png-gumlet_php_image_resize-replay
python3 parsarium.py afl build png php gumlet_php_image_resize
python3 parsarium.py afl prepare png php gumlet_php_image_resize runs/png-gumlet_php_image_resize-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
