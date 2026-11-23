# owen-oj/laravel-getid3 — MP4 / PHP

Pinned release: `v2.6.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/owen-oj-laravel-getid3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php owen_oj_laravel_getid3
python3 parsarium.py run mp4 php owen_oj_laravel_getid3 controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php owen_oj_laravel_getid3 CORPUS_DIR runs/mp4-owen_oj_laravel_getid3-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build mp4 php owen_oj_laravel_getid3
python3 parsarium.py afl prepare mp4 php owen_oj_laravel_getid3 runs/mp4-owen_oj_laravel_getid3-afl --fandango 100
python3 parsarium.py afl run runs/mp4-owen_oj_laravel_getid3-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
