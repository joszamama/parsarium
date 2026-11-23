# league/glide — PNG / PHP

Pinned release: `4.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/league-glide/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php league_glide
python3 parsarium.py run png php league_glide controls/png/red-green.png
python3 parsarium.py replay png php league_glide CORPUS_DIR runs/png-league_glide-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png php league_glide
python3 parsarium.py afl prepare png php league_glide runs/png-league_glide-afl --fandango 100
python3 parsarium.py afl run runs/png-league_glide-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
