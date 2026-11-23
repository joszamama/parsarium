# wapmorgan/mp3info — MP3 / PHP

Pinned release: `0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/php/wapmorgan-mp3info/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 php wapmorgan_mp3info
python3 parsarium.py run mp3 php wapmorgan_mp3info controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 php wapmorgan_mp3info CORPUS_DIR runs/mp3-wapmorgan_mp3info-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build mp3 php wapmorgan_mp3info
python3 parsarium.py afl prepare mp3 php wapmorgan_mp3info runs/mp3-wapmorgan_mp3info-afl --fandango 100
python3 parsarium.py afl run runs/mp3-wapmorgan_mp3info-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
