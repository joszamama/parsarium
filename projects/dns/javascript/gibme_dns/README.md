# @gibme/dns — DNS / JavaScript

Pinned release: `22.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/javascript/gibme-dns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns javascript gibme_dns
python3 parsarium.py run dns javascript gibme_dns controls/dns/response.bin
python3 parsarium.py replay dns javascript gibme_dns CORPUS_DIR runs/dns-gibme_dns-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build dns javascript gibme_dns
python3 parsarium.py afl prepare dns javascript gibme_dns runs/dns-gibme_dns-afl --fandango 100
python3 parsarium.py afl run runs/dns-gibme_dns-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** Two valid controls (a query and a response with CNAME, A, AAAA and MX answers). They do not establish EDNS0, DNSSEC, TXT or authority/additional behaviour.
