# DNS / Python — pilot

**Status:** pilot_two_verified_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: two Python paths verified, dnspython and dpkt, ranked by PyPI Stats last-month downloads. pycares is excluded (c-ares channel API, no bytes parser) and scapy is excluded under this pilot's no-socket rule (its import opens AF_NETLINK sockets). dnslib, py3dns and pypacker remain leads. Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use; the remaining leads are unverified, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/python/dns/ranking.md) · [Standard API inventory](../../../data/python/dns/standard.json)

## Third-party parsers

- [dnspython](dnspython/README.md) — verified Docker harness
- [dpkt](dpkt/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
