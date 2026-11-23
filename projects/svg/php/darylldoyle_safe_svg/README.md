# darylldoyle/safe-svg — SVG / PHP

Pinned release: `2.5.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/darylldoyle-safe-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php darylldoyle_safe_svg
python3 parsarium.py run svg php darylldoyle_safe_svg controls/svg/red-green.svg
python3 parsarium.py replay svg php darylldoyle_safe_svg CORPUS_DIR runs/svg-darylldoyle_safe_svg-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg php darylldoyle_safe_svg
python3 parsarium.py afl prepare svg php darylldoyle_safe_svg runs/svg-darylldoyle_safe_svg-afl --fandango 100
python3 parsarium.py afl run runs/svg-darylldoyle_safe_svg-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
