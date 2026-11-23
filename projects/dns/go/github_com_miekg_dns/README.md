# github.com/miekg/dns — DNS / Go

Pinned release: `v1.1.73`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/go/github-com-miekg-dns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns go github_com_miekg_dns
python3 parsarium.py run dns go github_com_miekg_dns controls/dns/response.bin
python3 parsarium.py replay dns go github_com_miekg_dns CORPUS_DIR runs/dns-github_com_miekg_dns-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build dns go github_com_miekg_dns
python3 parsarium.py afl prepare dns go github_com_miekg_dns runs/dns-github_com_miekg_dns-afl --fandango 100
python3 parsarium.py afl run runs/dns-github_com_miekg_dns-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
