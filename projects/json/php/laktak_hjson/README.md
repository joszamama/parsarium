# laktak/hjson — JSON / PHP

Pinned release: `v2.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/php/laktak-hjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php laktak_hjson
python3 parsarium.py run json php laktak_hjson controls/json/nested-object.json
python3 parsarium.py replay json php laktak_hjson CORPUS_DIR runs/json-laktak_hjson-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json php laktak_hjson
python3 parsarium.py afl prepare json php laktak_hjson runs/json-laktak_hjson-afl --fandango 100
python3 parsarium.py afl run runs/json-laktak_hjson-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
