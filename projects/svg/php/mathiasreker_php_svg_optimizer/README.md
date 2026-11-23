# mathiasreker/php-svg-optimizer — SVG / PHP

Pinned release: `10.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/mathiasreker-php-svg-optimizer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php mathiasreker_php_svg_optimizer
python3 parsarium.py run svg php mathiasreker_php_svg_optimizer controls/svg/red-green.svg
python3 parsarium.py replay svg php mathiasreker_php_svg_optimizer CORPUS_DIR runs/svg-mathiasreker_php_svg_optimizer-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg php mathiasreker_php_svg_optimizer
python3 parsarium.py afl prepare svg php mathiasreker_php_svg_optimizer runs/svg-mathiasreker_php_svg_optimizer-afl --fandango 100
python3 parsarium.py afl run runs/svg-mathiasreker_php_svg_optimizer-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
