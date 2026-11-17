# dns-messages — DNS / Python

Pinned release: `1.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/python/dns-messages/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns python dns_messages
python3 parsarium.py run dns python dns_messages controls/dns/response.bin
python3 parsarium.py replay dns python dns_messages CORPUS_DIR runs/dns-dns_messages-replay
python3 parsarium.py afl build dns python dns_messages
python3 parsarium.py afl prepare dns python dns_messages runs/dns-dns_messages-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
