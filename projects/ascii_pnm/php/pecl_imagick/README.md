# pecl/imagick — ASCII PNM / PHP

Pinned release: `3.8.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/php/pecl-imagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm php pecl_imagick
python3 parsarium.py run ascii_pnm php pecl_imagick controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm php pecl_imagick CORPUS_DIR runs/ascii_pnm-pecl_imagick-replay
python3 parsarium.py afl build ascii_pnm php pecl_imagick
python3 parsarium.py afl prepare ascii_pnm php pecl_imagick runs/ascii_pnm-pecl_imagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
