# DNS / Python — pilot

**Status:** pilot_five_verified_search_bounded; incomplete. 5 verified third-party paths, 0 verified standard APIs, 5 verified Docker harnesses.

Pilot cell: five Python paths verified, dnspython, dpkt, dnslib, py3dns and dns-messages, ranked by PyPI Stats last-month downloads. py3dns has no API reference (README and bundled unpacker tests only) and its import reads /etc/resolv.conf as a local file. pycares is excluded (c-ares channel API, no bytes parser) and scapy is excluded under this pilot's no-socket rule (its import opens AF_NETLINK sockets). Round-2 checks: zeroconf, impacket and pypacker fail the response control (MX or AAAA/CNAME rdata not decoded by the library); pyshark wraps tshark; pydns is py3dns's predecessor; async-dns decodes both controls but documents no message-bytes API and stays a lead. dns-messages has very low adoption (46 downloads). Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. The PyPI name search is alphabetical and bounded to its first 100 hits, so further leads came from targeted lookups. Package-level adoption metrics include non-DNS use; the remaining leads are unverified, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/python/dns/ranking.md) · [Standard API inventory](../../../data/python/dns/standard.json)

## Third-party parsers

- [dnspython](dnspython/README.md) — verified Docker harness
- [dpkt](dpkt/README.md) — verified Docker harness
- [dnslib](dnslib/README.md) — verified Docker harness
- [py3dns](py3dns/README.md) — verified Docker harness
- [dns-messages](dns-messages/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
