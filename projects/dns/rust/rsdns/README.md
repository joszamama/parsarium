# rsdns — DNS / Rust

Pinned release: `0.23.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/rust/rsdns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns rust rsdns
python3 parsarium.py run dns rust rsdns controls/dns/response.bin
python3 parsarium.py replay dns rust rsdns CORPUS_DIR runs/dns-rsdns-replay
python3 parsarium.py afl build dns rust rsdns
python3 parsarium.py afl prepare dns rust rsdns runs/dns-rsdns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
