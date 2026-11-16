# intervention/image-driver-vips — ASCII PNM / PHP

Pinned release: `4.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/php/intervention-image-driver-vips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm php intervention_image_driver_vips
python3 parsarium.py run ascii_pnm php intervention_image_driver_vips controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm php intervention_image_driver_vips CORPUS_DIR runs/ascii_pnm-intervention_image_driver_vips-replay
python3 parsarium.py afl build ascii_pnm php intervention_image_driver_vips
python3 parsarium.py afl prepare ascii_pnm php intervention_image_driver_vips runs/ascii_pnm-intervention_image_driver_vips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
