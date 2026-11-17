# pcap4j-core — DNS / Java

Pinned release: `1.8.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/java/pcap4j-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns java pcap4j_core
python3 parsarium.py run dns java pcap4j_core controls/dns/response.bin
python3 parsarium.py replay dns java pcap4j_core CORPUS_DIR runs/dns-pcap4j_core-replay
python3 parsarium.py afl build dns java pcap4j_core
python3 parsarium.py afl prepare dns java pcap4j_core runs/dns-pcap4j_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
