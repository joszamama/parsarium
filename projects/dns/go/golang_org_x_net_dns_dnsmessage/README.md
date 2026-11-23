# golang.org/x/net/dns/dnsmessage — DNS / Go

Pinned release: `v0.63.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/go/golang-org-x-net-dns-dnsmessage/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns go golang_org_x_net_dns_dnsmessage
python3 parsarium.py run dns go golang_org_x_net_dns_dnsmessage controls/dns/response.bin
python3 parsarium.py replay dns go golang_org_x_net_dns_dnsmessage CORPUS_DIR runs/dns-golang_org_x_net_dns_dnsmessage-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build dns go golang_org_x_net_dns_dnsmessage
python3 parsarium.py afl prepare dns go golang_org_x_net_dns_dnsmessage runs/dns-golang_org_x_net_dns_dnsmessage-afl --fandango 100
python3 parsarium.py afl run runs/dns-golang_org_x_net_dns_dnsmessage-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
