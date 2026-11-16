# osiemsiedem/intervention-image-vips-driver — ASCII PNM / PHP

Pinned release: `v0.11.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/php/osiemsiedem-intervention-image-vips-driver/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm php osiemsiedem_intervention_image_vips_driver
python3 parsarium.py run ascii_pnm php osiemsiedem_intervention_image_vips_driver controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm php osiemsiedem_intervention_image_vips_driver CORPUS_DIR runs/ascii_pnm-osiemsiedem_intervention_image_vips_driver-replay
python3 parsarium.py afl build ascii_pnm php osiemsiedem_intervention_image_vips_driver
python3 parsarium.py afl prepare ascii_pnm php osiemsiedem_intervention_image_vips_driver runs/ascii_pnm-osiemsiedem_intervention_image_vips_driver-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
