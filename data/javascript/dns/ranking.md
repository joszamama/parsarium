# JavaScript × DNS: selected parsers (pilot)

Six verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

npm downloads, 2026-10-17:2026-11-15 (30 days), from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [dns-packet](https://github.com/mafintosh/dns-packet/blob/v5.6.1/README.md#packet-decodebuf-offset) | 5.6.1 | 81,519,355 | dns-packet (mafintosh) decoder, index.js |
| 2 | [@dnsquery/dns-packet](https://github.com/dnsquery/dns-packet/blob/main/README.md#packet-decodebuf-offset) | 6.1.1 | 785,358 | dns-packet family (fork of mafintosh dns-packet) |
| 3 | [dns2](https://github.com/lsongdev/node-dns/blob/master/README.md) | 3.1.1 | 304,498 | dns2 own decoder (packet.js) |
| 4 | [native-dns-packet](https://github.com/tjfontaine/native-dns-packet/blob/master/README.md) | 0.1.1 | 72,104 | native-dns-packet (tjfontaine node-dns packet.js) |
| 5 | [hbo-dnsd](https://github.com/hbouvier/dnsd/blob/master/README.md#example-parse-a-message) | 0.9.8 | 34,937 | dnsd (Iris Couch) decoder (parse.js, message.js) |
| 6 | [dns-js](https://github.com/mdns-js/node-dns-js/blob/master/README.md#example) | 0.3.1 | 13,675 | dns-js (mdns-js) decoder (lib/dnspacket.js, lib/dnsrecord.js) |

**dns-packet 5.6.1** (MIT) parses local bytes with `dnsPacket.decode(buf: Buffer) -> packet object`. Both controls match the oracle summary. The response control covers 407 library lines in 6 files. AFL++ feedback repeats 3 times per control; response and query give 45/21 parser features and 65/41 AFL++ tuples, differing by 24 features and 24 tuples ([receipt](dns-packet-feedback-differential.json)). Own JavaScript decoder (name decompression, header and per-type rdata codecs in index.js). A and AAAA text comes from its dependency @leichtgewicht/ip-codec 2.0.5. Forks @dnsquery/dns-packet and @leichtgewicht/dns-packet share this family; multicast-dns uses it for mDNS.

**@dnsquery/dns-packet 6.1.1** (MIT) parses local bytes with `decode(buf: Uint8Array | Buffer) -> packet object`. Both controls match the oracle summary. The response control covers 517 library lines in 7 files. AFL++ feedback repeats 3 times per control; response and query give 60/35 parser features and 80/55 AFL++ tuples, differing by 25 features and 25 tuples ([receipt](dnsquery-dns-packet-feedback-differential.json)). Shared family with dns-packet: the README calls it a fork with TypeScript types that does not use Node.js primitives. Its index.js is a separate TypeScript build (about 3,100 differing non-whitespace lines from dns-packet 5.6.1) and reads integers through its own buffer_utils.js; the decoding algorithm and record codecs follow dns-packet. A/AAAA text comes from @leichtgewicht/ip-codec 2.0.5. Kept as a substantive rewrite: only 53 of its 1,222 distinct non-test source lines (4.3%) occur in dns-packet 5.6.1, and 364 of 1,220 (29.8%) after normalising whitespace, semicolons, declarations and quotes; the decoding algorithm and record layout still follow dns-packet.

**dns2 3.1.1** (MIT) parses local bytes with `Packet.parse(buffer: Buffer) -> Packet`. Both controls match the oracle summary. The response control covers 1070 library lines in 14 files. AFL++ feedback repeats 3 times per control; response and query give 57/32 parser features and 76/52 AFL++ tuples, differing by 25 features and 24 tuples ([receipt](dns2-feedback-differential.json)). Own pure-JavaScript decoder with no dependencies (packet.js over its bit reader lib/reader.js); 5 of its 1,602 distinct non-test source lines occur in dns-packet 5.6.1. The package also ships UDP/TCP/DoH clients and servers; the harness only calls Packet.parse and constructs no client or server. dns2 decodes the reserved Z bit, AD and CD as separate header fields, which the harness packs into z. A and AAAA text are dns2's own (its toIPv6 compresses the longest zero run). The harness rejects a parse that reports per-record DecodeErrors. Because the documented entry point is require('dns2'), module-load lines of the client and server files count toward the package line total; packet.js alone covers 767 lines on the response control.

**native-dns-packet 0.1.1** (MIT) parses local bytes with `Packet.parse(buffer: Buffer) -> Packet`. Both controls match the oracle summary. The response control covers 433 library lines in 3 files. AFL++ feedback repeats 3 times per control; response and query give 42/21 parser features and 62/41 AFL++ tuples, differing by 23 features and 23 tuples ([receipt](native-dns-packet-feedback-differential.json)). Own JavaScript state-machine decoder (packet.js) reading through its buffercursor dependency; native-dns (a resolver) builds on it. It keeps all three bits after RA (res1, res2, res3), which the harness packs into z. It prints AAAA as eight uncompressed hex groups, which the harness compresses per RFC 5952. Its question parser asserts a single question, so messages with QDCOUNT > 1 are outside its scope. The near-identical forks @luminati-io/native-dns-packet (99.2% shared distinct source lines) and native-node-dns-packet (99.3%) are not counted.

**hbo-dnsd 0.9.8** (Apache-2.0) parses local bytes with `dnsd.parse(buffer: Buffer) -> DNSMessage`. Both controls match the oracle summary. The response control covers 592 library lines in 7 files. AFL++ feedback repeats 3 times per control; response and query give 90/66 parser features and 110/86 AFL++ tuples, differing by 24 features and 24 tuples ([receipt](hbo-dnsd-feedback-differential.json)). Own JavaScript decoder from Iris Couch's dnsd (parse.js reads the header bits, sections and compressed names; message.js builds records). hbo-dnsd is a fork of dnsd 0.9.6 that shares 857 of its 876 distinct non-test source lines (97.8%); only hbo-dnsd, the more downloaded of the pair (34,937 vs 340), is counted, so the family has one path. dnsd decodes AD and CD but drops the reserved Z bit, so z carries AD and CD only (both controls have all three bits clear). It names types, classes and opcodes; the harness maps them back to numbers with the package's own constants.js and opcode table. AAAA comes as eight zero-padded hex groups, which the harness compresses per RFC 5952. The package also ships a DNS server; the harness creates none.

**dns-js 0.3.1** (MIT) parses local bytes with `dns.DNSPacket.parse(buffer: Buffer) -> DNSPacket`. Both controls match the oracle summary. The response control covers 441 library lines in 6 files. AFL++ feedback repeats 3 times per control; response and query give 45/24 parser features and 65/44 AFL++ tuples, differing by 21 features and 21 tuples ([receipt](dns-js-feedback-differential.json)). Own JavaScript decoder written for mdns-js (lib/dnspacket.js and lib/dnsrecord.js over its BufferConsumer); its README says it borrows test fixtures and some parts from native-dns-packet, but only 40 of its 521 distinct non-test source lines (7.7%) occur in native-dns-packet 0.1.1. mdns-js-packet 0.2.0 is the same code under its earlier name (98.1% shared lines) and is not counted. dns-js keeps all three bits after RA (res1..res3, packed into z) and prints AAAA as eight uncompressed hex groups, which the harness compresses per RFC 5952. The coverage subject is the package's lib/ directory, which keeps its nested copy of the debug dependency out.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | @leichtgewicht/dns-packet | 121,612 | `decode(buf)` | dns-packet fork |
| 2 | dns-query | 114,588 |  | dns-packet family (@leichtgewicht/dns-packet) |
| 3 | native-dns | 68,783 |  | native-dns-packet |
| 4 | dohdec | 14,724 |  | dns-packet |
| 5 | bns | 8,888 | `wire.Message.decode(data) (not in the README)` | bns (chjj) |
| 6 | mdns-js-packet | 4,819 | `DNSPacket.parse(buffer)` | dns-js family |
| 7 | @gibme/dns | 1,965 | `new Packet(buffer)` | @gibme/dns |
| 8 | @luminati-io/native-dns-packet | 1,196 |  | native-dns-packet |
| 9 | @noelminamino/dns-packet | 754 | `decode(buf)` | dns-packet family (fork of @dnsquery/dns-packet) |
| 10 | @portable/dns-packet | 594 | `decode(bytes)` | @portable/dns-packet |
| 11 | dnsd | 340 | `dnsd.parse(buffer)` | dnsd (Iris Couch) |
| 12 | native-node-dns-packet | 338 |  | native-dns-packet |
| 13 | dns-message | 127 |  |  |
| 14 | dnspacket-ts | 98 |  |  |
| 15 | @serverless-dns/dns-parser | 19 |  |  |

## Checked, excluded or recorded separately

- **multicast-dns** (excluded): mDNS network API over dns-packet; no own parser.
