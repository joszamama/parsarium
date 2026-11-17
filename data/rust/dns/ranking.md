# Rust × DNS: leads (pilot)

No path is verified yet. Leads are ordered by one adoption metric to choose what to verify first; this is not a selection.

## Adoption metric

crates.io recent_downloads (90 days), from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Compared only within this cell.

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | [hickory-proto](https://docs.rs/hickory-proto/latest/hickory_proto/op/message/struct.Message.html#method.from_vec) | 107,121,455 | `hickory_proto::op::Message::from_vec(&[u8])` | Hickory DNS proto (formerly trust-dns) |
| 2 | [trust-dns-proto](https://docs.rs/trust-dns-proto/latest/trust_dns_proto/op/message/struct.Message.html#method.from_vec) | 67,753,440 | `trust_dns_proto::op::Message::from_vec(&[u8])` | Hickory DNS proto (formerly trust-dns) |
| 3 | [domain](https://docs.rs/domain/latest/domain/base/message/struct.Message.html#method.from_octets) | 13,501,697 | `domain::base::Message::from_octets(bytes)` | NLnet Labs domain |
| 4 | [simple-dns](https://docs.rs/simple-dns/latest/simple_dns/struct.Packet.html#method.parse) | 13,178,526 | `simple_dns::Packet::parse(&[u8])` | simple-dns |
| 5 | [dns-parser](https://docs.rs/dns-parser/latest/dns_parser/struct.Packet.html#method.parse) | 5,386,460 | `dns_parser::Packet::parse(&[u8])` | dns-parser |
| 6 | [dns-message-parser](https://docs.rs/dns-message-parser) | 120,778 | `dns_message_parser::Dns::decode(Bytes)` | dns-message-parser |
| 7 | [rustdns](https://docs.rs/rustdns) | 102,165 | `rustdns::Message::from_slice(&[u8])` | rustdns |
| 8 | [dns-protocol](https://docs.rs/dns-protocol) | 30,680 |  | dns-protocol |
| 9 | [dnsparse](https://docs.rs/dnsparse) | 5,876 |  | dnsparse |
| 10 | [packet-dissector-dns](https://docs.rs/packet-dissector-dns) | 3,416 |  |  |
| 11 | [dns_parse](https://docs.rs/dns_parse) | 2,774 |  |  |

## Excluded or recorded separately

- **mdns-sd** (excluded): mDNS service-discovery daemon; its message parser is not a documented public bytes API.
