# intervention/image — PNG / PHP

Pinned release: `4.4.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/intervention-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php intervention_image
python3 parsarium.py run png php intervention_image controls/png/red-green.png
python3 parsarium.py replay png php intervention_image CORPUS_DIR runs/png-intervention_image-replay
python3 parsarium.py afl build png php intervention_image
python3 parsarium.py afl prepare png php intervention_image runs/png-intervention_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
