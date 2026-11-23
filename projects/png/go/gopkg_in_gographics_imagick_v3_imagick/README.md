# gopkg.in/gographics/imagick.v3/imagick — PNG / Go

Pinned release: `v3.7.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/gopkg-in-gographics-imagick-v3-imagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go gopkg_in_gographics_imagick_v3_imagick
python3 parsarium.py run png go gopkg_in_gographics_imagick_v3_imagick controls/png/red-green.png
python3 parsarium.py replay png go gopkg_in_gographics_imagick_v3_imagick CORPUS_DIR runs/png-gopkg_in_gographics_imagick_v3_imagick-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png go gopkg_in_gographics_imagick_v3_imagick
python3 parsarium.py afl prepare png go gopkg_in_gographics_imagick_v3_imagick runs/png-gopkg_in_gographics_imagick_v3_imagick-afl --fandango 100
python3 parsarium.py afl run runs/png-gopkg_in_gographics_imagick_v3_imagick-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
