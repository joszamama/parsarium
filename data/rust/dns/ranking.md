# Rust × DNS: selected parsers (pilot)

Seven verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

crates.io recent_downloads (90 days), from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17 (round-2 targeted lookups under `round2_targeted`, same source and day). Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [hickory-proto](https://docs.rs/hickory-proto/0.26.3/hickory_proto/op/struct.Message.html#method.from_vec) | 0.26.3 | 36,097,977 | Hickory DNS proto (formerly trust-dns-proto): BinDecoder and Message/Record decoders |
| 2 | [simple-dns](https://docs.rs/simple-dns/0.13.1/simple_dns/struct.Packet.html#method.parse) | 0.13.1 | 4,084,902 | simple-dns (src/dns/packet.rs, header.rs, name.rs, rdata/*) |
| 3 | [domain](https://docs.rs/domain/0.12.3/domain/base/message/struct.Message.html#method.from_slice) | 0.12.3 | 2,135,993 | NLnet Labs domain (base/message.rs, base/name/parsed.rs, base/record.rs, rdata) |
| 4 | [dns-parser](https://docs.rs/dns-parser/0.8.0/dns_parser/struct.Packet.html#method.parse) | 0.8.0 | 524,293 | dns-parser (src/parser.rs, header.rs, name.rs, rdata/*) |
| 5 | [dns-message-parser](https://docs.rs/dns-message-parser/0.9.0/dns_message_parser/struct.Dns.html#method.decode) | 0.9.0 | 7,679 | dns-message-parser (src/decode/*: decoder, dns, domain_name, rr) |
| 6 | [rustdns](https://docs.rs/rustdns/0.7.0/rustdns/struct.Message.html#method.from_slice) | 0.7.0 | 2,786 | rustdns (src/dns.rs MessageParser, types.rs, resource.rs) |
| 7 | [rsdns](https://docs.rs/rsdns/0.23.0/rsdns/message/reader/struct.MessageIterator.html#method.new) | 0.23.0 | 2,486 | rsdns message reader (src/message/reader/*, bytes/cursor, names, records/data) |

**hickory-proto 0.26.3** (MIT OR Apache-2.0) parses local bytes with `hickory_proto::op::Message::from_vec(buffer: &[u8]) -> Result<Message, DecodeError>`. Both controls match the oracle summary. The response control covers 479 library lines in 55 files. AFL++ feedback repeats 3 times per control; response and query give 703/446 parser features and 285/178 AFL++ tuples, differing by 259 features and 107 tuples ([receipt](hickory-proto-feedback-differential.json)). Own pure-Rust decoder (serialize/binary/decoder.rs, op/message.rs, rr/record.rs, rr/domain/name.rs). trust-dns-proto is the same project under its earlier crate name. The crate drops the reserved Z bit, so z reports AD and CD only.

**simple-dns 0.13.1** (MIT) parses local bytes with `simple_dns::Packet::parse(data: &[u8]) -> Result<Packet, SimpleDnsError>`. Both controls match the oracle summary. The response control covers 310 library lines in 46 files. AFL++ feedback repeats 3 times per control; response and query give 434/272 parser features and 182/120 AFL++ tuples, differing by 162 features and 62 tuples ([receipt](simple-dns-feedback-differential.json)). Own pure-Rust decoder, used by mdns-sd-style service discovery crates (simple-mdns, iroh); no code from hickory-proto. It exposes AD and CD as packet flags but not the reserved Z bit, so z reports AD and CD only. A and AAAA addresses are stored as u32/u128; the harness prints them with std::net.

**domain 0.12.3** (BSD-3-Clause) parses local bytes with `domain::base::Message::from_slice(slice: &[u8]) -> Result<&Message<[u8]>, ShortMessage>`. Both controls match the oracle summary. The response control covers 606 library lines in 65 files. AFL++ feedback repeats 3 times per control; response and query give 692/419 parser features and 32/28 AFL++ tuples, differing by 273 features and 4 tuples ([receipt](domain-feedback-differential.json)). Own pure-Rust decoder by NLnet Labs (the authors of ldns, Unbound and NSD), a separate Rust code base from the selected C ldns path. from_slice checks the header length; the question and record sections are parsed lazily when the harness iterates them (records read as AllRecordData with ParsedName). It keeps the Z, AD and CD bits. Built with default-features = false and std (only the rand default is dropped). Its parser is generic over octet types, so most of it is monomorphized into the (uninstrumented) harness crate: the scoped AFL++ map keeps only 32/28 tuples (4 differing) although LLVM source regions differ by 273.

**dns-parser 0.8.0** (MIT OR Apache-2.0) parses local bytes with `dns_parser::Packet::parse(data: &[u8]) -> Result<Packet, Error>`. Both controls match the oracle summary. The response control covers 250 library lines in 29 files. AFL++ feedback repeats 3 times per control; response and query give 351/181 parser features and 129/79 AFL++ tuples, differing by 170 features and 52 tuples ([receipt](dns-parser-feedback-differential.json)). Own pure-Rust decoder (tailhook), the parser behind older mDNS crates; no code from hickory-proto or simple-dns. The header keeps AD and CD but not the reserved Z bit, so z reports AD and CD only. ResourceRecord has no numeric type field: the harness maps the decoded RData variant (A, AAAA, CNAME, NS, PTR, MX) to its type number. Last release 2018 (edition 2015 crate).

**dns-message-parser 0.9.0** (BSD-3-Clause) parses local bytes with `dns_message_parser::Dns::decode(bytes: Bytes) -> DecodeResult<Dns>`. Both controls match the oracle summary. The response control covers 338 library lines in 86 files. AFL++ feedback repeats 3 times per control; response and query give 509/276 parser features and 252/140 AFL++ tuples, differing by 233 features and 114 tuples ([receipt](dns-message-parser-feedback-differential.json)). Own pure-Rust decoder (LinkTed); no code from hickory-proto, domain or simple-dns. Flags keep AD and CD but not the reserved Z bit, so z reports AD and CD only. Records decode into typed structs; A and AAAA structs carry no class because the decoder accepts those types only in class IN (any other class is a decode error), so the harness reports class 1 for them. The harness copies the local bytes into a bytes::Bytes buffer for the documented decode entry point.

**rustdns 0.7.0** (Apache-2.0) parses local bytes with `rustdns::Message::from_slice(buf: &[u8]) -> io::Result<Message>`. Both controls match the oracle summary. The response control covers 221 library lines in 9 files. AFL++ feedback repeats 3 times per control; response and query give 350/203 parser features and 218/150 AFL++ tuples, differing by 149 features and 68 tuples ([receipt](rustdns-feedback-differential.json)). Own pure-Rust decoder (bramp); no code from hickory-proto or the other selected crates. Built with default-features = false, so the DNS clients (UDP/TCP/DoH) and zone-file parser are not compiled; the message parser is part of the base crate. It keeps the Z, AD and CD bits. TTLs are Durations printed in whole seconds.

**rsdns 0.23.0** (MIT OR Apache-2.0) parses local bytes with `rsdns::message::reader::MessageIterator::new(buf: &[u8]) -> Result<MessageIterator>; header(), questions(), records()`. Both controls match the oracle summary. The response control covers 463 library lines in 33 files. AFL++ feedback repeats 3 times per control; response and query give 607/386 parser features and 259/108 AFL++ tuples, differing by 223 features and 151 tuples ([receipt](rsdns-feedback-differential.json)). Own pure-Rust decoder in a DNS client library; built without any net-* feature, so no client code is compiled. The records iterator tags every record with its section. rsdns exposes no Z, AD or CD flag (the Z getter is test-only), so z is reported as 0.

## Remaining leads

| Order | Lead | Metric | Status | Input API lead | Family |
| ---: | --- | ---: | --- | --- | --- |
| 1 | dns-protocol | 2,785 | unresolved |  | dns-protocol |
| 2 | packet-dissector-dns | 1,980 | unresolved |  |  |
| 3 | dns_parse | 1,056 | unresolved |  |  |
| 4 | dnsparse | 11 | unresolved |  | dnsparse |

## Checked, excluded or recorded separately

- **trust-dns-proto** (excluded): Predecessor of the already selected hickory-proto: trust-dns-proto 0.23.2 is the last release of the same project before the rename to hickory-proto (0.24). It passed both DNS controls and the full gate, but the decoder code is largely the same: 72% of trust-dns-proto's distinct non-test lines in serialize/binary (BinDecoder), 83% in rr/domain (name decoding) and 53% in op (Message/Header) are identical in hickory-proto 0.26.3 (44% over the whole crate, which also carries resolver/runtime code). Shared family with a stronger selected path; not counted. Evidence: data/rust/dns/trust-dns-proto-demoted.json.
- **mdns-sd** (excluded): mDNS service-discovery daemon; its message parser is not a documented public bytes API.
