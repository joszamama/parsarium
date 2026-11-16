# intervention/image-laravel — ASCII PNM / PHP

Pinned release: `4.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/php/intervention-image-laravel/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm php intervention_image_laravel
python3 parsarium.py run ascii_pnm php intervention_image_laravel controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm php intervention_image_laravel CORPUS_DIR runs/ascii_pnm-intervention_image_laravel-replay
python3 parsarium.py afl build ascii_pnm php intervention_image_laravel
python3 parsarium.py afl prepare ascii_pnm php intervention_image_laravel runs/ascii_pnm-intervention_image_laravel-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
