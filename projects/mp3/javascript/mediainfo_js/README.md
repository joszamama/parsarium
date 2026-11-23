# mediainfo.js — MP3 / JavaScript

Pinned release: `0.3.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/javascript/mediainfo-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 javascript mediainfo_js
python3 parsarium.py run mp3 javascript mediainfo_js controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 javascript mediainfo_js CORPUS_DIR runs/mp3-mediainfo_js-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build mp3 javascript mediainfo_js
python3 parsarium.py afl prepare mp3 javascript mediainfo_js runs/mp3-mediainfo_js-afl --fandango 100
python3 parsarium.py afl run runs/mp3-mediainfo_js-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
