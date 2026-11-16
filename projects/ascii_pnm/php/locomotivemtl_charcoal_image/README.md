# locomotivemtl/charcoal-image — ASCII PNM / PHP

Pinned release: `v0.4.3.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/php/locomotivemtl-charcoal-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm php locomotivemtl_charcoal_image
python3 parsarium.py run ascii_pnm php locomotivemtl_charcoal_image controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm php locomotivemtl_charcoal_image CORPUS_DIR runs/ascii_pnm-locomotivemtl_charcoal_image-replay
python3 parsarium.py afl build ascii_pnm php locomotivemtl_charcoal_image
python3 parsarium.py afl prepare ascii_pnm php locomotivemtl_charcoal_image runs/ascii_pnm-locomotivemtl_charcoal_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
