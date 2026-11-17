# DNS / C++ — pilot

**Status:** pilot_one_verified_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: one C++ path verified, libtins (Debian popcon 52, the only C++ DNS message library with a Debian source package). PcapPlusPlus has no Debian source, so it has no primary metric and stays an unranked lead. Poco, Qt QDnsLookup, Boost.Asio and the PowerDNS applications are excluded (resolvers or applications, no message-bytes API). Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use; the remaining leads are unverified, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/cpp/dns/ranking.md) · [Standard API inventory](../../../data/cpp/dns/standard.json)

## Third-party parsers

- [libtins](libtins/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
