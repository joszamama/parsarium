# JavaScript × DNS: selected parsers (pilot)

Two verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

npm downloads, 2026-10-17:2026-11-15 (30 days), from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [dns-packet](https://github.com/mafintosh/dns-packet/blob/v5.6.1/README.md#packet-decodebuf-offset) | 5.6.1 | 81,519,355 | dns-packet (mafintosh) decoder, index.js |
| 2 | [@dnsquery/dns-packet](https://github.com/dnsquery/dns-packet/blob/main/README.md#packet-decodebuf-offset) | 6.1.1 | 785,358 | dns-packet family (fork of mafintosh dns-packet) |

**dns-packet 5.6.1** (MIT) parses local bytes with `dnsPacket.decode(buf: Buffer) -> packet object`. Both controls match the oracle summary. The response control covers 407 library lines in 6 files. AFL++ feedback repeats 3 times per control; response and query give 45/21 parser features and 65/41 AFL++ tuples, differing by 24 features and 24 tuples ([receipt](dns-packet-feedback-differential.json)). Own JavaScript decoder (name decompression, header and per-type rdata codecs in index.js). A and AAAA text comes from its dependency @leichtgewicht/ip-codec 2.0.5. Forks @dnsquery/dns-packet and @leichtgewicht/dns-packet share this family; multicast-dns uses it for mDNS.

**@dnsquery/dns-packet 6.1.1** (MIT) parses local bytes with `decode(buf: Uint8Array | Buffer) -> packet object`. Both controls match the oracle summary. The response control covers 517 library lines in 7 files. AFL++ feedback repeats 3 times per control; response and query give 60/35 parser features and 80/55 AFL++ tuples, differing by 25 features and 25 tuples ([receipt](dnsquery-dns-packet-feedback-differential.json)). Shared family with dns-packet: the README calls it a fork with TypeScript types that does not use Node.js primitives. Its index.js is a separate TypeScript build (about 3,100 differing non-whitespace lines from dns-packet 5.6.1) and reads integers through its own buffer_utils.js; the decoding algorithm and record codecs follow dns-packet. A/AAAA text comes from @leichtgewicht/ip-codec 2.0.5. Kept as a substantive rewrite: only 53 of its 1,222 distinct non-test source lines (4.3%) occur in dns-packet 5.6.1, and 364 of 1,220 (29.8%) after normalising whitespace, semicolons, declarations and quotes; the decoding algorithm and record layout still follow dns-packet.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | dns2 | 304,498 | `Packet.parse(buffer)` | dns2 own Packet parser |
| 2 | @leichtgewicht/dns-packet | 121,612 | `decode(buf)` | dns-packet fork |
| 3 | native-dns-packet | 72,104 | `Packet.parse(buffer)` | native-dns-packet |
| 4 | dns-js | 13,675 | `DNSPacket.parse(buffer)` | dns-js |
| 5 | mdns-js-packet | 4,819 | `DNSPacket.parse(buffer)` | dns-js family |
| 6 | dns-message | 127 |  |  |
| 7 | dnspacket-ts | 98 |  |  |
| 8 | @serverless-dns/dns-parser | 19 |  |  |

## Checked, excluded or recorded separately

- **multicast-dns** (excluded): mDNS network API over dns-packet; no own parser.
