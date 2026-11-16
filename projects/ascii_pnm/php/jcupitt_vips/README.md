# jcupitt/vips — ASCII PNM / PHP

Pinned release: `v2.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/php/jcupitt-vips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm php jcupitt_vips
python3 parsarium.py run ascii_pnm php jcupitt_vips controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm php jcupitt_vips CORPUS_DIR runs/ascii_pnm-jcupitt_vips-replay
python3 parsarium.py afl build ascii_pnm php jcupitt_vips
python3 parsarium.py afl prepare ascii_pnm php jcupitt_vips runs/ascii_pnm-jcupitt_vips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
