# DNS / C++ — pilot

**Status:** pilot_one_verified_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: one C++ path verified, libtins, ranked by Debian popcon sourcemax installations; the cell stays at one because no other C++ DNS message library with a documented bytes API, a Debian metric and a passing response control was found. PcapPlusPlus (pcpp::DnsLayer over a caller-supplied buffer) stays a lead without a primary metric: it has no Debian source package (absent from the pinned table; sources.debian.org search returned no match on 2026-11-17), so the Debian dev-package fallback is unavailable too, and GitHub stars are not allowed outside PLY cells. Round 2 checked the remaining C++ debian-source:dns hits and Seastar (registry-snapshot.json round2_targeted): libjdns/QJDns keeps its packet decoder private, kf6-kdnssd and kdnssd-kf5 are service-discovery frameworks, and Seastar's resolver delegates decoding to c-ares; POCO, Qt QDnsLookup, Boost/asio and the PowerDNS applications stay excluded from round 1. Round 3 read all 128 debian-source:dns names and checked ISC Kea: kea-dev installs libkea-dns++ (Message::fromWire), but Kea 3.0.4 registers no CNAME or MX RDATA decoder, so the response control fails. libtins parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Its popcon count (52) is weak and package-level; the cell is not a definitive top ten.

[Ranking and search limits](../../../data/cpp/dns/ranking.md) · [Standard API inventory](../../../data/cpp/dns/standard.json)

## Third-party parsers

- [libtins](libtins/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
