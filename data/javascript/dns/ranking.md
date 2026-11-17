# JavaScript × DNS: selected parsers (pilot)

One verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

npm downloads, 2026-10-17:2026-11-15 (30 days), from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [dns-packet](https://github.com/mafintosh/dns-packet/blob/v5.6.1/README.md#packet-decodebuf-offset) | 5.6.1 | 81,519,355 | dns-packet (mafintosh) decoder, index.js |

**dns-packet 5.6.1** (MIT) parses local bytes with `dnsPacket.decode(buf: Buffer) -> packet object`. Both controls match the oracle summary. The response control covers 407 library lines in 6 files. AFL++ feedback repeats 3 times per control; response and query give 45/21 parser features and 65/41 AFL++ tuples, differing by 24 features and 24 tuples ([receipt](dns-packet-feedback-differential.json)). Own JavaScript decoder (name decompression, header and per-type rdata codecs in index.js). A and AAAA text comes from its dependency @leichtgewicht/ip-codec 2.0.5. Forks @dnsquery/dns-packet and @leichtgewicht/dns-packet share this family; multicast-dns uses it for mDNS.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | @dnsquery/dns-packet | 785,358 | `decode(buf)` | dns-packet fork |
| 2 | dns2 | 304,498 | `Packet.parse(buffer)` | dns2 own Packet parser |
| 3 | @leichtgewicht/dns-packet | 121,612 | `decode(buf)` | dns-packet fork |
| 4 | native-dns-packet | 72,104 | `Packet.parse(buffer)` | native-dns-packet |
| 5 | dns-js | 13,675 | `DNSPacket.parse(buffer)` | dns-js |
| 6 | mdns-js-packet | 4,819 | `DNSPacket.parse(buffer)` | dns-js family |
| 7 | dns-message | 127 |  |  |
| 8 | dnspacket-ts | 98 |  |  |
| 9 | @serverless-dns/dns-parser | 19 |  |  |

## Checked, excluded or recorded separately

- **multicast-dns** (excluded): mDNS network API over dns-packet; no own parser.
