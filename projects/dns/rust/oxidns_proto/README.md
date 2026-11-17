# oxidns-proto — DNS / Rust

Pinned release: `0.1.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/rust/oxidns-proto/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns rust oxidns_proto
python3 parsarium.py run dns rust oxidns_proto controls/dns/response.bin
python3 parsarium.py replay dns rust oxidns_proto CORPUS_DIR runs/dns-oxidns_proto-replay
python3 parsarium.py afl build dns rust oxidns_proto
python3 parsarium.py afl prepare dns rust oxidns_proto runs/dns-oxidns_proto-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
