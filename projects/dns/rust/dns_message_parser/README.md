# dns-message-parser — DNS / Rust

Pinned release: `0.9.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/rust/dns-message-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns rust dns_message_parser
python3 parsarium.py run dns rust dns_message_parser controls/dns/response.bin
python3 parsarium.py replay dns rust dns_message_parser CORPUS_DIR runs/dns-dns_message_parser-replay
python3 parsarium.py afl build dns rust dns_message_parser
python3 parsarium.py afl prepare dns rust dns_message_parser runs/dns-dns_message_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
