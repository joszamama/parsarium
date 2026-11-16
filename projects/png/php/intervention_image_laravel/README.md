# intervention/image-laravel — PNG / PHP

Pinned release: `4.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/intervention-image-laravel/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php intervention_image_laravel
python3 parsarium.py run png php intervention_image_laravel controls/png/red-green.png
python3 parsarium.py replay png php intervention_image_laravel CORPUS_DIR runs/png-intervention_image_laravel-replay
python3 parsarium.py afl build png php intervention_image_laravel
python3 parsarium.py afl prepare png php intervention_image_laravel runs/png-intervention_image_laravel-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
