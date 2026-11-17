# DNS / PHP — pilot

**Status:** pilot_two_verified_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: two PHP paths verified, react/dns and pear/net_dns2, ranked by Packagist total downloads. daverandom/libdns parses both controls but fails the php-fuzzer gate (its rewrite breaks a constant expression), so its slot is left open; amphp/dns, spatie/dns and remotelyliving/php-dns are excluded as resolvers or wrappers. react/dns drops the Z, AD and CD bits (z reported as 0). Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use; the remaining leads are unverified, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/php/dns/ranking.md) · [Standard API inventory](../../../data/php/dns/standard.json)

## Third-party parsers

- [react/dns](react-dns/README.md) — verified Docker harness
- [pear/net_dns2](pear-net-dns2/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
