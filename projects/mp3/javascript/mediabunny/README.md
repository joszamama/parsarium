# mediabunny — MP3 / JavaScript

Pinned release: `1.66.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/javascript/mediabunny/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 javascript mediabunny
python3 parsarium.py run mp3 javascript mediabunny controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 javascript mediabunny CORPUS_DIR runs/mp3-mediabunny-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build mp3 javascript mediabunny
python3 parsarium.py afl prepare mp3 javascript mediabunny runs/mp3-mediabunny-afl --fandango 100
python3 parsarium.py afl run runs/mp3-mediabunny-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** Untagged MPEG Layer III only; two valid CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, or MPEG-2.5 support. mediabunny demuxes frames and reads headers; it does not decode MP3 audio without WebCodecs, which this path does not use.
