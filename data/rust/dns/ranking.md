# Rust × DNS: selected parsers (pilot)

One verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

crates.io recent_downloads (90 days), from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [hickory-proto](https://docs.rs/hickory-proto/0.26.3/hickory_proto/op/struct.Message.html#method.from_vec) | 0.26.3 | 107,121,455 | Hickory DNS proto (formerly trust-dns-proto): BinDecoder and Message/Record decoders |

**hickory-proto 0.26.3** (MIT OR Apache-2.0) parses local bytes with `hickory_proto::op::Message::from_vec(buffer: &[u8]) -> Result<Message, DecodeError>`. Both controls match the oracle summary. The response control covers 479 library lines in 55 files. AFL++ feedback repeats 3 times per control; response and query give 703/446 parser features and 285/178 AFL++ tuples, differing by 259 features and 107 tuples ([receipt](hickory-proto-feedback-differential.json)). Own pure-Rust decoder (serialize/binary/decoder.rs, op/message.rs, rr/record.rs, rr/domain/name.rs). trust-dns-proto is the same project under its earlier crate name. The crate drops the reserved Z bit, so z reports AD and CD only.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | trust-dns-proto | 67,753,440 | `trust_dns_proto::op::Message::from_vec(&[u8])` | Hickory DNS proto (formerly trust-dns) |
| 2 | domain | 13,501,697 | `domain::base::Message::from_octets(bytes)` | NLnet Labs domain |
| 3 | simple-dns | 13,178,526 | `simple_dns::Packet::parse(&[u8])` | simple-dns |
| 4 | dns-parser | 5,386,460 | `dns_parser::Packet::parse(&[u8])` | dns-parser |
| 5 | dns-message-parser | 120,778 | `dns_message_parser::Dns::decode(Bytes)` | dns-message-parser |
| 6 | rustdns | 102,165 | `rustdns::Message::from_slice(&[u8])` | rustdns |
| 7 | dns-protocol | 30,680 |  | dns-protocol |
| 8 | dnsparse | 5,876 |  | dnsparse |
| 9 | packet-dissector-dns | 3,416 |  |  |
| 10 | dns_parse | 2,774 |  |  |

## Checked, excluded or recorded separately

- **mdns-sd** (excluded): mDNS service-discovery daemon; its message parser is not a documented public bytes API.
