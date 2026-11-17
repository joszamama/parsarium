# simple-dns — DNS / Rust

Pinned release: `0.13.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/rust/simple-dns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns rust simple_dns
python3 parsarium.py run dns rust simple_dns controls/dns/response.bin
python3 parsarium.py replay dns rust simple_dns CORPUS_DIR runs/dns-simple_dns-replay
python3 parsarium.py afl build dns rust simple_dns
python3 parsarium.py afl prepare dns rust simple_dns runs/dns-simple_dns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
