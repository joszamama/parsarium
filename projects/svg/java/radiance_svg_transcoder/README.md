# radiance-svg-transcoder — SVG / Java

Pinned release: `7.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/radiance-svg-transcoder/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java radiance_svg_transcoder
python3 parsarium.py run svg java radiance_svg_transcoder controls/svg/red-green.svg
python3 parsarium.py replay svg java radiance_svg_transcoder CORPUS_DIR runs/svg-radiance_svg_transcoder-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg java radiance_svg_transcoder
python3 parsarium.py afl prepare svg java radiance_svg_transcoder runs/svg-radiance_svg_transcoder-afl --fandango 100
python3 parsarium.py afl run runs/svg-radiance_svg_transcoder-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
