# DNS / Java — pilot

**Status:** pilot_two_verified_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: two Java paths verified, netty-codec-dns and dnsjava, ranked by deps.dev direct dependents summed over releases (a weak signal). Netty leaves A/AAAA as raw records (the harness formats the decoded bytes) and its DnsQuery has no AA/TC/RA/RCODE. pcap4j and MiniDNS remain leads; vert.x is excluded as a network client over Netty's codec. Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use; the remaining leads are unverified, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/java/dns/ranking.md) · [Standard API inventory](../../../data/java/dns/standard.json)

## Third-party parsers

- [netty-codec-dns](netty-codec-dns/README.md) — verified Docker harness
- [dnsjava](dnsjava/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
