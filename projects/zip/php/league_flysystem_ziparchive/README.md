# league/flysystem-ziparchive — ZIP / PHP

Pinned release: `3.31.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/league-flysystem-ziparchive/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php league_flysystem_ziparchive
python3 parsarium.py run zip php league_flysystem_ziparchive controls/zip/hello.zip
python3 parsarium.py replay zip php league_flysystem_ziparchive CORPUS_DIR runs/zip-league_flysystem_ziparchive-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip php league_flysystem_ziparchive
python3 parsarium.py afl prepare zip php league_flysystem_ziparchive runs/zip-league_flysystem_ziparchive-afl --fandango 100
python3 parsarium.py afl run runs/zip-league_flysystem_ziparchive-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
