# packet-dissector-dns — DNS / Rust

Pinned release: `0.6.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/rust/packet-dissector-dns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns rust packet_dissector_dns
python3 parsarium.py run dns rust packet_dissector_dns controls/dns/response.bin
python3 parsarium.py replay dns rust packet_dissector_dns CORPUS_DIR runs/dns-packet_dissector_dns-replay
python3 parsarium.py afl build dns rust packet_dissector_dns
python3 parsarium.py afl prepare dns rust packet_dissector_dns runs/dns-packet_dissector_dns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
