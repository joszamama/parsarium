# enshrined/svg-sanitize — SVG / PHP

Pinned release: `1.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/enshrined-svg-sanitize/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php enshrined_svg_sanitize
python3 parsarium.py run svg php enshrined_svg_sanitize controls/svg/red-green.svg
python3 parsarium.py replay svg php enshrined_svg_sanitize CORPUS_DIR runs/svg-enshrined_svg_sanitize-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg php enshrined_svg_sanitize
python3 parsarium.py afl prepare svg php enshrined_svg_sanitize runs/svg-enshrined_svg_sanitize-afl --fandango 100
python3 parsarium.py afl run runs/svg-enshrined_svg_sanitize-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
