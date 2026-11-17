# DNS / PHP — pilot

**Status:** pilot_five_verified_search_bounded; incomplete. 5 verified third-party paths, 0 verified standard APIs, 5 verified Docker harnesses.

Pilot cell: five PHP paths verified, react/dns, daverandom/libdns, pear/net_dns2, utopia-php/dns and jdwx/dns-query, ranked by Packagist total downloads. daverandom/libdns's php-fuzzer blocker (the interceptor rewrite breaks one class constant) is resolved by loading that single class file unmodified in the fuzz entry only; amphp/dns, spatie/dns and remotelyliving/php-dns are excluded as resolvers or wrappers. Round-2 checks: purplepixie/phpdns parses only inside its socket client; mikepultz/netdns2 is the same repository as pear/net_dns2 (identical v2.0.7 commit) and is not counted twice; the other new Packagist hits are resolvers, format adapters over LibDNS, Net_DNS2 1.x forks or unreleased packages. jdwx/dns-query is a Net_DNS2 1.x fork that shares 6.0% of its distinct source lines with pear/net_dns2 2.x; yswery/dns remains a lead. react/dns, daverandom/libdns and utopia-php/dns drop the Z, AD and CD bits (z reported as 0). Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use; the remaining leads are unverified, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/php/dns/ranking.md) · [Standard API inventory](../../../data/php/dns/standard.json)

## Third-party parsers

- [react/dns](react-dns/README.md) — verified Docker harness
- [daverandom/libdns](daverandom-libdns/README.md) — verified Docker harness
- [pear/net_dns2](pear-net-dns2/README.md) — verified Docker harness
- [utopia-php/dns](utopia-php-dns/README.md) — verified Docker harness
- [jdwx/dns-query](jdwx-dns-query/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
