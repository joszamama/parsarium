# DNS / Rust — pilot

**Status:** pilot_ten_verified_search_bounded; incomplete. 10 verified third-party paths, 0 verified standard APIs, 10 verified Docker harnesses.

Pilot cell: ten Rust paths verified (hickory-proto, simple-dns, domain, dns-parser, dns-message-parser, rustdns, rsdns, packet-dissector-dns, hns-dns-wire, oxidns-proto), ranked by crates.io recent_downloads (90 days). Remaining leads: smoltcp (unresolved_control_failure), webrtc-mdns (unresolved), dnssector (unresolved_control_failure), microdns (unresolved_control_failure), proxima-protocols (unresolved_control_failure), geiserx_ts_dns_wire (unresolved_control_failure), dns-protocol (unresolved_control_failure), mdns-proto (unresolved_control_failure), dns_parse (unresolved_control_failure), flex-dns (unresolved), dnsparse (unresolved_control_failure). Excluded after checking: trust-dns-proto, mdns-sd, rama-dns, hickory-net, rtc-mdns, tendns, packet-dissector-mdns, idns, dyns, dope-dns, dns-parser-revived, dns-parser-joe, dnsclient, pktkit (reasons in leads.json). crates.io searches sorted by recent downloads (dns, dns parser, dns packet, dns message, dns wire; first 100 each, under round3_search in the snapshot) found hns-dns-wire and confirmed packet-dissector-dns and oxidns-proto as the next verifiable crates by metric, while higher-download hits were resolvers, framework crates, an undocumented port (webrtc-mdns) or crates whose RDATA decoding misses MX/CNAME (smoltcp, proxima-protocols, mdns-proto). flex-dns (300) ranks above oxidns-proto (181) but needs a nightly-only compiler feature, so the tenth slot went to the next verifiable crate. Metric values are crates.io recent_downloads (90 days) from the snapshot; an earlier capture had recorded all-time downloads under that label and was corrected. trust-dns-proto 0.23.2 (hickory-proto's previous crate name) passed the full gate but is excluded as a predecessor sharing most of the decoder code; its records are archived in trust-dns-proto-demoted.json. Rust AFL++ overlays are scoped to the parser crates (afl_instrumented_crates) because the summary encoder's random hashing made whole-binary maps unstable. Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/rust/dns/ranking.md) · [Standard API inventory](../../../data/rust/dns/standard.json)

## Third-party parsers

- [hickory-proto](hickory-proto/README.md) — verified Docker harness · [source repository](<https://github.com/hickory-dns/hickory-dns>) · [crates.io](<https://crates.io/crates/hickory-proto>)
- [simple-dns](simple-dns/README.md) — verified Docker harness · [source repository](<https://github.com/balliegojr/simple-dns>) · [crates.io](<https://crates.io/crates/simple-dns>)
- [domain](domain/README.md) — verified Docker harness · [source repository](<https://github.com/NLnetLabs/domain>) · [crates.io](<https://crates.io/crates/domain>)
- [dns-parser](dns-parser/README.md) — verified Docker harness · [source repository](<https://github.com/tailhook/dns-parser>) · [crates.io](<https://crates.io/crates/dns-parser>)
- [dns-message-parser](dns-message-parser/README.md) — verified Docker harness · [source repository](<https://github.com/LinkTed/dns-message-parser>) · [crates.io](<https://crates.io/crates/dns-message-parser>)
- [rustdns](rustdns/README.md) — verified Docker harness · [source repository](<https://github.com/bramp/rustdns>) · [crates.io](<https://crates.io/crates/rustdns>)
- [rsdns](rsdns/README.md) — verified Docker harness · [source repository](<https://github.com/r-bk/rsdns>) · [crates.io](<https://crates.io/crates/rsdns>)
- [packet-dissector-dns](packet-dissector-dns/README.md) — verified Docker harness · [source repository](<https://github.com/higebu/packet-dissector>) · [crates.io](<https://crates.io/crates/packet-dissector-dns>)
- [hns-dns-wire](hns-dns-wire/README.md) — verified Docker harness · [source repository](<https://github.com/handshake-rs/hns-dane-engine>) · [crates.io](<https://crates.io/crates/hns-dns-wire>)
- [oxidns-proto](oxidns-proto/README.md) — verified Docker harness · [source repository](<https://github.com/svenshi/oxidns>) · [crates.io](<https://crates.io/crates/oxidns-proto>)

## Standard and runtime APIs

None verified in this pilot cell yet.
