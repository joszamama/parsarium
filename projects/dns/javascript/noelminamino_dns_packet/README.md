# @noelminamino/dns-packet — DNS / JavaScript

Pinned release: `7.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/javascript/noelminamino-dns-packet/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns javascript noelminamino_dns_packet
python3 parsarium.py run dns javascript noelminamino_dns_packet controls/dns/response.bin
python3 parsarium.py replay dns javascript noelminamino_dns_packet CORPUS_DIR runs/dns-noelminamino_dns_packet-replay
python3 parsarium.py afl build dns javascript noelminamino_dns_packet
python3 parsarium.py afl prepare dns javascript noelminamino_dns_packet runs/dns-noelminamino_dns_packet-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Two valid controls (a query and a response with CNAME, A, AAAA and MX answers). They do not establish EDNS0, DNSSEC, TXT or authority/additional behaviour.
