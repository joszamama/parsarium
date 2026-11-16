# phphleb/imageresizer — ASCII PNM / PHP

Pinned release: `v2.0.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/php/phphleb-imageresizer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm php phphleb_imageresizer
python3 parsarium.py run ascii_pnm php phphleb_imageresizer controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm php phphleb_imageresizer CORPUS_DIR runs/ascii_pnm-phphleb_imageresizer-replay
python3 parsarium.py afl build ascii_pnm php phphleb_imageresizer
python3 parsarium.py afl prepare ascii_pnm php phphleb_imageresizer runs/ascii_pnm-phphleb_imageresizer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
