# batik-swing — SVG / Java

Pinned release: `1.20`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/batik-swing/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java batik_swing
python3 parsarium.py run svg java batik_swing controls/svg/red-green.svg
python3 parsarium.py replay svg java batik_swing CORPUS_DIR runs/svg-batik_swing-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg java batik_swing
python3 parsarium.py afl prepare svg java batik_swing runs/svg-batik_swing-afl --fandango 100
python3 parsarium.py afl run runs/svg-batik_swing-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
