# DNS / Python — pilot

**Status:** pilot_eight_verified_search_bounded; incomplete. 8 verified third-party paths, 0 verified standard APIs, 8 verified Docker harnesses.

Pilot cell: eight Python paths verified, dnspython, Twisted (twisted.names.dns), mitmproxy (mitmproxy.dns), dpkt, dnslib, py3dns, namespy and dns-messages, ranked by PyPI Stats last-month downloads; the cell stays below ten because no further qualifying path was found. Twisted's and mitmproxy's counts cover the whole networking framework and interception proxy, not only their DNS packages; importing mitmproxy.dns pulls in mitmproxy's flow model and its full dependency set, but an instrumented run of both controls created no socket in either image. py3dns has no API reference (README and bundled unpacker tests only) and its import reads /etc/resolv.conf as a local file. pycares is excluded (c-ares channel API, no bytes parser) and scapy is excluded under this pilot's no-socket rule (its import opens AF_NETLINK sockets). Round-2 checks: zeroconf, impacket and pypacker fail the response control (MX or AAAA/CNAME rdata not decoded by the library); pyshark wraps tshark; pydns is py3dns's predecessor. Round 3 read all 1,074 PyPI names containing 'dns' (round 1 inspected the first 100 alphabetically) and looked up the plausible ones: PythonDNS and microdns wrap dnslib, dnsq wraps dnspython, dnspython3 and dnspythonchia are dnspython's older line and fork, dnslib3 is a dnslib fork (65.9% shared lines, same import name), aiodnsresolver keeps its parser private, asyncdns2 and dnsmock are resolvers. async-dns and dns-client decode messages through exported but undocumented classes and stay leads. Round 4 searched beyond the registry windows (registry-snapshot.json round4_discovery): GitHub repository searches (dns parser, dns packet, dns message, topic:dns, rfc1035, dns codec, dns decoder, dns wire format; first 100 each, mapped to PyPI names), awesome lists, packet and binary-format libraries and mDNS libraries, ranked only by the same PyPI Stats source (round4_targeted). It found namespy (selected; its name lacks 'dns'). netius stays a lead (decoder inside its DNS client module, header flags kept as raw octets); pyatv, kamene, aiozeroconf and kydns fail the response control by source inspection (MX, and for some CNAME/AAAA, not decoded); construct's 2.5 gallery struct follows no compression pointers; strangle wraps the obsolete BIND 8 libbind; scapy-python3 is a placeholder; PyPCAPKit, pycrate and hachoir have no DNS parser. Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use; the remaining leads are unverified, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/python/dns/ranking.md) · [Standard API inventory](../../../data/python/dns/standard.json)

## Third-party parsers

- [dnspython](dnspython/README.md) — verified Docker harness
- [twisted](twisted/README.md) — verified Docker harness
- [mitmproxy](mitmproxy/README.md) — verified Docker harness
- [dpkt](dpkt/README.md) — verified Docker harness
- [dnslib](dnslib/README.md) — verified Docker harness
- [py3dns](py3dns/README.md) — verified Docker harness
- [namespy](namespy/README.md) — verified Docker harness
- [dns-messages](dns-messages/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
