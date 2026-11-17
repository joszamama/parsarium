# DNS / Rust — pilot

**Status:** pilot_seven_verified_search_bounded; incomplete. 7 verified third-party paths, 0 verified standard APIs, 7 verified Docker harnesses.

Pilot cell: seven Rust paths verified (hickory-proto, simple-dns, domain, dns-parser, dns-message-parser, rustdns, rsdns), ranked by crates.io recent_downloads (90 days). Remaining leads: dnssector (unresolved_control_failure), microdns (unresolved_control_failure), dns-protocol (unresolved_control_failure), packet-dissector-dns (unresolved), dns_parse (unresolved_control_failure), dnsparse (unresolved_control_failure). Excluded after checking: trust-dns-proto, mdns-sd, rama-dns (reasons in leads.json). Metric values are crates.io recent_downloads (90 days) from the snapshot; round 1 had recorded all-time downloads under that label, corrected in round 2. trust-dns-proto 0.23.2 (hickory-proto's previous crate name) passed the full gate but is excluded as a predecessor sharing most of the decoder code; its records are archived in trust-dns-proto-demoted.json. Rust AFL++ overlays are scoped to the parser crates (afl_instrumented_crates) because the summary encoder's random hashing made whole-binary maps unstable. Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/rust/dns/ranking.md) · [Standard API inventory](../../../data/rust/dns/standard.json)

## Third-party parsers

- [hickory-proto](hickory-proto/README.md) — verified Docker harness
- [simple-dns](simple-dns/README.md) — verified Docker harness
- [domain](domain/README.md) — verified Docker harness
- [dns-parser](dns-parser/README.md) — verified Docker harness
- [dns-message-parser](dns-message-parser/README.md) — verified Docker harness
- [rustdns](rustdns/README.md) — verified Docker harness
- [rsdns](rsdns/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
