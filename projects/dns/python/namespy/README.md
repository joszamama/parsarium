# namespy — DNS / Python

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/python/namespy/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns python namespy
python3 parsarium.py run dns python namespy controls/dns/response.bin
python3 parsarium.py replay dns python namespy CORPUS_DIR runs/dns-namespy-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build dns python namespy
python3 parsarium.py afl prepare dns python namespy runs/dns-namespy-afl --fandango 100
python3 parsarium.py afl run runs/dns-namespy-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
