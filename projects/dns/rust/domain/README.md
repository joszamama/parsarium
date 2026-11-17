# domain — DNS / Rust

Pinned release: `0.12.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/rust/domain/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns rust domain
python3 parsarium.py run dns rust domain controls/dns/response.bin
python3 parsarium.py replay dns rust domain CORPUS_DIR runs/dns-domain-replay
python3 parsarium.py afl build dns rust domain
python3 parsarium.py afl prepare dns rust domain runs/dns-domain-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
