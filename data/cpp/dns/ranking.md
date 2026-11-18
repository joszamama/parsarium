# C++ × DNS: selected parsers (pilot)

One verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

Debian popcon sourcemax installations (max over binary packages built from the source package), from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [libtins](https://libtins.github.io/docs/latest/d0/dcd/classTins_1_1DNS.html) | 4.6 | 52 | libtins DNS PDU (src/dns.cpp with its Memory::InputMemoryStream reader) |

**libtins 4.6** (BSD-2-Clause) parses local bytes with `Tins::DNS::DNS(const uint8_t *buffer, uint32_t total_sz); queries(), answers(), authority(), additional() and header getters`. Both controls match the oracle summary. The response control covers 426 library lines in 20 files. AFL++ feedback repeats 3 times per control; response and query give 204/150 parser features and 459/264 AFL++ tuples, differing by 54 features and 209 tuples ([receipt](libtins-feedback-differential.json)). Own C++ decoder; built here without libpcap, so no capture or socket code is linked in. Keeps the Z, AD and CD bits.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family | Status |
| ---: | --- | ---: | --- | --- | --- |
| 1 | isc-kea | 516 | `isc::dns::Message(Message::PARSE).fromWire(isc::util::InputBuffer&) (kea/dns/message.h)` | Kea libdns++ (BIND 10 lineage) | unresolved_control_failure |
| 2 | dnslib-cpp | missing | `` | mnezerka dnslib | unresolved_no_primary_metric |
| 3 | libdnspacket | missing | `` | libdnspacket (header-only C++17) | unresolved_no_primary_metric |

- **isc-kea**: Debian's kea-dev installs libkea-dns++ with kea/dns/message.h (Message::fromWire parses a wire message), but by source inspection of upstream 3.0.4 (kea-3.0.4.tar.xz, sha256 62d32494...) src/lib/dns/rrparamregistry.cc registers RDATA factories only for TSIG, A, NS, SOA, PTR, TXT, AAAA, OPT, RRSIG, DHCID and TKEY; CNAME and MX are type names only, so their RDATA stays generic (raw) and the names inside them are not decoded by the library.
- **dnslib-cpp**: Small C++ DNS encode/decode library (and a fork of it) on GitHub with no Debian source package, so no primary metric. Not attempted. Star fallback (2026-11-18): mnezerka/dnslib has 65 stars, below the 100-star threshold, and no tagged release.
- **libdnspacket**: Header-only C++17 DNS packet parser/builder on GitHub; neither it nor the other GitHub-only C++ parsers found by the GitHub repository searches (packetzero/dnsparser, ElNeMeR70/cpp-dns-encode) has a Debian source package, so none has a primary metric. Not attempted. Star fallback (2026-11-18): bughandler/libdnspacket has 31 stars and packetzero/dnsparser 35, both below the 100-star threshold.

## Checked, excluded or recorded separately

- **pcapplusplus** (excluded): No primary metric: PcapPlusPlus has no Debian source package (absent from the pinned popcon sourcemax table; sources.debian.org search for 'pcapplusplus' returned no exact or partial match on 2026-11-17), so the Debian dev-package fallback is also unavailable. Star fallback (2026-11-18): seladb/PcapPlusPlus has 3,174 stars and tagged releases, but it is a multi-protocol packet capture, parsing and crafting library (dozens of protocol layers, pcap/PF_RING/DPDK capture); its stars reflect those features, so it does not qualify under the format-specific repository rule (as for GLib GMarkup).
- **poco** (excluded): Resolver over getaddrinfo/gethostbyname; no DNS message bytes API.
- **qtbase-opensource-src** (excluded): QDnsLookup performs network lookups; it documents no parser for caller-supplied message bytes.
- **boost1.83** (excluded): getaddrinfo wrapper; no DNS message parser.
- **asio** (excluded): getaddrinfo wrapper; no DNS message parser.
- **pdns** (excluded): Authoritative server application; its MOADNSParser is internal, not an installed library.
- **dnsdist** (excluded): Load-balancer application, not a library.
- **pdns-recursor** (excluded): Resolver application, not a library.
- **libjdns** (excluded): The C++ binary package libqjdns-qt5 wraps the jdns resolver/mDNS sessions in QJDns; the packet decoder (jdns_packet.h) is private, so no documented API parses caller-supplied message bytes.
- **kf6-kdnssd** (excluded): Service-discovery (browse/publish) framework over Avahi or mDNSResponder; no DNS message parser API.
- **kdnssd-kf5** (excluded): KF5 version of the same service-discovery framework; no DNS message parser API.
- **seastar** (excluded): No Debian source package in the pinned table (no primary metric); its seastar::net::dns resolver delegates message decoding to c-ares and documents no parser for caller-supplied message bytes.
- **libcrafter** (excluded): C++ packet crafting and decoding library with a DNS layer, but no Debian source package (sources.debian.org 404), so no primary metric and no Debian dev-package fallback. Not attempted. Star fallback (2026-11-18): pellegre/libcrafter has 312 stars, but it is a multi-protocol packet crafting and decoding library, not a format-specific DNS library, so the star fallback does not apply.
- **hello-dns** (excluded): DNS teaching repository with the tdns example server/resolver and its DNSMessageReader; 654 stars, but the repository has no tagged release (GitHub tags API returned none on 2026-11-18), so no pinned tagged release qualifies for the star fallback.
- **adguard-dnslibs** (excluded): DNS proxy and filtering library used in AdGuard products (120 stars): DoH/DoT/DNSCrypt upstreams and a filtering engine. Its message handling uses ldns (conanfile.py at v2.10.2 requires ldns), already counted in the C cell, and its stars reflect the proxy/filtering features, so it does not qualify under the format-specific repository rule.
- **bundy** (excluded): Authoritative DNS server suite continuing BIND 10 (138 stars); its libdns++ is the BIND 10 lineage of Kea's libdns++ (response-control failure in this cell), the repository is a server rather than a parser library, and its tags are development-branch markers (trac*_base), not releases.
