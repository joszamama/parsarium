# DNS / C — pilot

**Status:** pilot_two_verified_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: two C paths verified, c-ares and ldns, ranked by Debian popcon sourcemax installations. bind9, unbound and libevent are excluded because they document no public parser for caller-supplied message bytes; knot, udns and getdns remain leads (getdns shares the ldns-derived gldns code). glibc and musl libresolv ns_initparse are recorded as standard/runtime leads and were not run. c-ares and ldns drop the reserved Z bit (z carries AD and CD). Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use; the remaining leads are unverified, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/c/dns/ranking.md) · [Standard API inventory](../../../data/c/dns/standard.json)

## Third-party parsers

- [c-ares](c-ares/README.md) — verified Docker harness
- [ldns](ldns/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
