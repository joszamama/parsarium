# zanysoft/laravel-zip — ZIP / PHP

Pinned release: `3.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/zanysoft-laravel-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php zanysoft_laravel_zip
python3 parsarium.py run zip php zanysoft_laravel_zip controls/zip/hello.zip
python3 parsarium.py replay zip php zanysoft_laravel_zip CORPUS_DIR runs/zip-zanysoft_laravel_zip-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip php zanysoft_laravel_zip
python3 parsarium.py afl prepare zip php zanysoft_laravel_zip runs/zip-zanysoft_laravel_zip-afl --fandango 100
python3 parsarium.py afl run runs/zip-zanysoft_laravel_zip-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
