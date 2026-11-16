# jcupitt/vips — PNG / PHP

Pinned release: `v2.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/jcupitt-vips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php jcupitt_vips
python3 parsarium.py run png php jcupitt_vips controls/png/red-green.png
python3 parsarium.py replay png php jcupitt_vips CORPUS_DIR runs/png-jcupitt_vips-replay
python3 parsarium.py afl build png php jcupitt_vips
python3 parsarium.py afl prepare png php jcupitt_vips runs/png-jcupitt_vips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
