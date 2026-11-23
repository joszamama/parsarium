# hns-dns-wire — DNS / Rust

Pinned release: `0.2.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/rust/hns-dns-wire/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns rust hns_dns_wire
python3 parsarium.py run dns rust hns_dns_wire controls/dns/response.bin
python3 parsarium.py replay dns rust hns_dns_wire CORPUS_DIR runs/dns-hns_dns_wire-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build dns rust hns_dns_wire
python3 parsarium.py afl prepare dns rust hns_dns_wire runs/dns-hns_dns_wire-afl --fandango 100
python3 parsarium.py afl run runs/dns-hns_dns_wire-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
