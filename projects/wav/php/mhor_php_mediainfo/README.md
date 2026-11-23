# mhor/php-mediainfo — WAV / PHP

Pinned release: `5.8.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/mhor-php-mediainfo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php mhor_php_mediainfo
python3 parsarium.py run wav php mhor_php_mediainfo controls/wav/32768-samples.wav
python3 parsarium.py replay wav php mhor_php_mediainfo CORPUS_DIR runs/wav-mhor_php_mediainfo-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build wav php mhor_php_mediainfo
python3 parsarium.py afl prepare wav php mhor_php_mediainfo runs/wav-mhor_php_mediainfo-afl --fandango 100
python3 parsarium.py afl run runs/wav-mhor_php_mediainfo-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
