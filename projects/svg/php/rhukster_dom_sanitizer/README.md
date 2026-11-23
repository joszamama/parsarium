# rhukster/dom-sanitizer — SVG / PHP

Pinned release: `1.0.20`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/rhukster-dom-sanitizer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php rhukster_dom_sanitizer
python3 parsarium.py run svg php rhukster_dom_sanitizer controls/svg/red-green.svg
python3 parsarium.py replay svg php rhukster_dom_sanitizer CORPUS_DIR runs/svg-rhukster_dom_sanitizer-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg php rhukster_dom_sanitizer
python3 parsarium.py afl prepare svg php rhukster_dom_sanitizer runs/svg-rhukster_dom_sanitizer-afl --fandango 100
python3 parsarium.py afl run runs/svg-rhukster_dom_sanitizer-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
