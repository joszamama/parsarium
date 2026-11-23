# meyfa/php-svg — SVG / PHP

Pinned release: `v0.16.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/meyfa-php-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php meyfa_php_svg
python3 parsarium.py run svg php meyfa_php_svg controls/svg/red-green.svg
python3 parsarium.py replay svg php meyfa_php_svg CORPUS_DIR runs/svg-meyfa_php_svg-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg php meyfa_php_svg
python3 parsarium.py afl prepare svg php meyfa_php_svg runs/svg-meyfa_php_svg-afl --fandango 100
python3 parsarium.py afl run runs/svg-meyfa_php_svg-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
