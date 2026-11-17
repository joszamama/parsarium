# DNS / Rust — pilot

**Status:** pilot_one_verified_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: one Rust path verified, hickory-proto, ranked by crates.io 90-day downloads. trust-dns-proto 0.23.2 (the project's previous crate name) passed the full gate but is excluded as a predecessor sharing most of the decoder code (72-83% of distinct non-test lines in its binary decoder and name modules); its records are archived in trust-dns-proto-demoted.json. domain, simple-dns and dns-parser remain leads and would add independent families. hickory-proto drops the reserved Z bit (z carries AD and CD); its AFL++ overlay is scoped to the parser crate because the summary encoder's random hashing made whole-binary maps unstable. Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use; the remaining leads are unverified, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/rust/dns/ranking.md) · [Standard API inventory](../../../data/rust/dns/standard.json)

## Third-party parsers

- [hickory-proto](hickory-proto/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
