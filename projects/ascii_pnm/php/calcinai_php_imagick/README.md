# calcinai/php-imagick — ASCII PNM / PHP

Pinned release: `v0.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/php/calcinai-php-imagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm php calcinai_php_imagick
python3 parsarium.py run ascii_pnm php calcinai_php_imagick controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm php calcinai_php_imagick CORPUS_DIR runs/ascii_pnm-calcinai_php_imagick-replay
python3 parsarium.py afl build ascii_pnm php calcinai_php_imagick
python3 parsarium.py afl prepare ascii_pnm php calcinai_php_imagick runs/ascii_pnm-calcinai_php_imagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
