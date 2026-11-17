# Rust × DNS: selected parsers (pilot)

Two verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

crates.io recent_downloads (90 days), from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17 (round-2 targeted lookups under `round2_targeted`, same source and day). Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [hickory-proto](https://docs.rs/hickory-proto/0.26.3/hickory_proto/op/struct.Message.html#method.from_vec) | 0.26.3 | 36,097,977 | Hickory DNS proto (formerly trust-dns-proto): BinDecoder and Message/Record decoders |
| 2 | [dns-parser](https://docs.rs/dns-parser/0.8.0/dns_parser/struct.Packet.html#method.parse) | 0.8.0 | 524,293 | dns-parser (src/parser.rs, header.rs, name.rs, rdata/*) |

**hickory-proto 0.26.3** (MIT OR Apache-2.0) parses local bytes with `hickory_proto::op::Message::from_vec(buffer: &[u8]) -> Result<Message, DecodeError>`. Both controls match the oracle summary. The response control covers 479 library lines in 55 files. AFL++ feedback repeats 3 times per control; response and query give 703/446 parser features and 285/178 AFL++ tuples, differing by 259 features and 107 tuples ([receipt](hickory-proto-feedback-differential.json)). Own pure-Rust decoder (serialize/binary/decoder.rs, op/message.rs, rr/record.rs, rr/domain/name.rs). trust-dns-proto is the same project under its earlier crate name. The crate drops the reserved Z bit, so z reports AD and CD only.

**dns-parser 0.8.0** (MIT OR Apache-2.0) parses local bytes with `dns_parser::Packet::parse(data: &[u8]) -> Result<Packet, Error>`. Both controls match the oracle summary. The response control covers 250 library lines in 29 files. AFL++ feedback repeats 3 times per control; response and query give 351/181 parser features and 129/79 AFL++ tuples, differing by 170 features and 52 tuples ([receipt](dns-parser-feedback-differential.json)). Own pure-Rust decoder (tailhook), the parser behind older mDNS crates; no code from hickory-proto or simple-dns. The header keeps AD and CD but not the reserved Z bit, so z reports AD and CD only. ResourceRecord has no numeric type field: the harness maps the decoded RData variant (A, AAAA, CNAME, NS, PTR, MX) to its type number. Last release 2018 (edition 2015 crate).

## Remaining leads

| Order | Lead | Metric | Status | Input API lead | Family |
| ---: | --- | ---: | --- | --- | --- |
| 1 | simple-dns | 4,084,902 | unresolved | `simple_dns::Packet::parse(&[u8])` | simple-dns |
| 2 | domain | 2,135,993 | unresolved | `domain::base::Message::from_octets(bytes)` | NLnet Labs domain |
| 3 | dns-message-parser | 7,679 | unresolved | `dns_message_parser::Dns::decode(Bytes)` | dns-message-parser |
| 4 | rustdns | 2,786 | unresolved | `rustdns::Message::from_slice(&[u8])` | rustdns |
| 5 | dns-protocol | 2,785 | unresolved |  | dns-protocol |
| 6 | packet-dissector-dns | 1,980 | unresolved |  |  |
| 7 | dns_parse | 1,056 | unresolved |  |  |
| 8 | dnsparse | 11 | unresolved |  | dnsparse |

## Checked, excluded or recorded separately

- **trust-dns-proto** (excluded): Predecessor of the already selected hickory-proto: trust-dns-proto 0.23.2 is the last release of the same project before the rename to hickory-proto (0.24). It passed both DNS controls and the full gate, but the decoder code is largely the same: 72% of trust-dns-proto's distinct non-test lines in serialize/binary (BinDecoder), 83% in rr/domain (name decoding) and 53% in op (Message/Header) are identical in hickory-proto 0.26.3 (44% over the whole crate, which also carries resolver/runtime code). Shared family with a stronger selected path; not counted. Evidence: data/rust/dns/trust-dns-proto-demoted.json.
- **mdns-sd** (excluded): mDNS service-discovery daemon; its message parser is not a documented public bytes API.
