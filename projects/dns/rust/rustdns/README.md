# rustdns — DNS / Rust

Pinned release: `0.7.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/rust/rustdns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns rust rustdns
python3 parsarium.py run dns rust rustdns controls/dns/response.bin
python3 parsarium.py replay dns rust rustdns CORPUS_DIR runs/dns-rustdns-replay
python3 parsarium.py afl build dns rust rustdns
python3 parsarium.py afl prepare dns rust rustdns runs/dns-rustdns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
