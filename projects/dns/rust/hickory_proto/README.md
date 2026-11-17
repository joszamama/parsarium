# hickory-proto — DNS / Rust

Pinned release: `0.26.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/rust/hickory-proto/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns rust hickory_proto
python3 parsarium.py run dns rust hickory_proto controls/dns/response.bin
python3 parsarium.py replay dns rust hickory_proto CORPUS_DIR runs/dns-hickory_proto-replay
python3 parsarium.py afl build dns rust hickory_proto
python3 parsarium.py afl prepare dns rust hickory_proto runs/dns-hickory_proto-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
