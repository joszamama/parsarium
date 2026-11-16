# orbitale/imagemagick-php — ASCII PNM / PHP

Pinned release: `v3.3.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/php/orbitale-imagemagick-php/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm php orbitale_imagemagick_php
python3 parsarium.py run ascii_pnm php orbitale_imagemagick_php controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm php orbitale_imagemagick_php CORPUS_DIR runs/ascii_pnm-orbitale_imagemagick_php-replay
python3 parsarium.py afl build ascii_pnm php orbitale_imagemagick_php
python3 parsarium.py afl prepare ascii_pnm php orbitale_imagemagick_php runs/ascii_pnm-orbitale_imagemagick_php-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
