# JavaScript × DNS: leads (pilot)

No path is verified yet. Leads are ordered by one adoption metric to choose what to verify first; this is not a selection.

## Adoption metric

npm downloads, 2026-10-17:2026-11-15 (30 days), from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Compared only within this cell.

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | [dns-packet](https://github.com/mafintosh/dns-packet#readme) | 81,519,355 | `dnsPacket.decode(buf)` | dns-packet (mafintosh) |
| 2 | [@dnsquery/dns-packet](https://www.npmjs.com/package/@dnsquery/dns-packet) | 785,358 | `decode(buf)` | dns-packet fork |
| 3 | [dns2](https://github.com/song940/node-dns#readme) | 304,498 | `Packet.parse(buffer)` | dns2 own Packet parser |
| 4 | [@leichtgewicht/dns-packet](https://www.npmjs.com/package/@leichtgewicht/dns-packet) | 121,612 | `decode(buf)` | dns-packet fork |
| 5 | [native-dns-packet](https://github.com/tjfontaine/native-dns-packet) | 72,104 | `Packet.parse(buffer)` | native-dns-packet |
| 6 | [dns-js](https://github.com/mdns-js/node-dns-js) | 13,675 | `DNSPacket.parse(buffer)` | dns-js |
| 7 | [mdns-js-packet](https://www.npmjs.com/package/mdns-js-packet) | 4,819 | `DNSPacket.parse(buffer)` | dns-js family |
| 8 | [dns-message](https://www.npmjs.com/package/dns-message) | 127 |  |  |
| 9 | [dnspacket-ts](https://www.npmjs.com/package/dnspacket-ts) | 98 |  |  |
| 10 | [@serverless-dns/dns-parser](https://www.npmjs.com/package/@serverless-dns/dns-parser) | 19 |  |  |

## Excluded or recorded separately

- **multicast-dns** (excluded): mDNS network API over dns-packet; no own parser.
