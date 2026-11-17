# DNS / JavaScript — pilot

**Status:** pilot_two_verified_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: two JavaScript paths verified, dns-packet and its fork @dnsquery/dns-packet (shared family, kept as a rewrite: 4.3% of its distinct non-test source lines are shared, 29.8% after normalisation), ranked by npm 30-day downloads. dns2, @leichtgewicht/dns-packet (another fork), native-dns-packet and dns-js remain leads; multicast-dns is excluded as an mDNS network API over dns-packet. Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use; the remaining leads are unverified, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/javascript/dns/ranking.md) · [Standard API inventory](../../../data/javascript/dns/standard.json)

## Third-party parsers

- [dns-packet](dns-packet/README.md) — verified Docker harness
- [@dnsquery/dns-packet](dnsquery-dns-packet/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
