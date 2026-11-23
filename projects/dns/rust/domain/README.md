# domain — DNS / Rust

Pinned release: `0.12.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/rust/domain/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns rust domain
python3 parsarium.py run dns rust domain controls/dns/response.bin
python3 parsarium.py replay dns rust domain CORPUS_DIR runs/dns-domain-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build dns rust domain
python3 parsarium.py afl prepare dns rust domain runs/dns-domain-afl --fandango 100
python3 parsarium.py afl run runs/dns-domain-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
