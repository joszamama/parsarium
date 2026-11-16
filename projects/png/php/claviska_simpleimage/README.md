# claviska/simpleimage — PNG / PHP

Pinned release: `4.4.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/claviska-simpleimage/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php claviska_simpleimage
python3 parsarium.py run png php claviska_simpleimage controls/png/red-green.png
python3 parsarium.py replay png php claviska_simpleimage CORPUS_DIR runs/png-claviska_simpleimage-replay
python3 parsarium.py afl build png php claviska_simpleimage
python3 parsarium.py afl prepare png php claviska_simpleimage runs/png-claviska_simpleimage-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
