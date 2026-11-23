# daverandom/libdns — DNS / PHP

Pinned release: `v2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/php/daverandom-libdns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns php daverandom_libdns
python3 parsarium.py run dns php daverandom_libdns controls/dns/response.bin
python3 parsarium.py replay dns php daverandom_libdns CORPUS_DIR runs/dns-daverandom_libdns-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build dns php daverandom_libdns
python3 parsarium.py afl prepare dns php daverandom_libdns runs/dns-daverandom_libdns-afl --fandango 100
python3 parsarium.py afl run runs/dns-daverandom_libdns-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
