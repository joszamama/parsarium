# DNS / C — pilot

**Status:** pilot_five_verified_search_bounded; incomplete. 5 verified third-party paths, 1 verified standard APIs, 5 verified Docker harnesses.

Pilot cell: five C paths verified, c-ares, ldns, knot (libknot), udns and getdns, ranked by Debian popcon sourcemax installations from the pinned table; the cell stays below ten because no further Debian-packaged C library with a documented API for caller-supplied message bytes decodes the controls. getdns bundles gldns (Unbound's sldns, ldns lineage), but its own decoder files share 75 of 3,228 distinct normalized source lines (2.3%) with ldns 1.8.4, so it is kept as a distinct package API with the lineage stated. Round 2 added targeted lookups for further debian-source:dns and conan:dns hits (registry-snapshot.json round2_targeted): libmicrodns, libjdns and djbdns are excluded (no documented message-bytes API or no library), as are adns, unbound, bind9, libevent and libspf2 from round 1; dnsjit (popcon 4) stays unresolved because its parser is a Lua module inside the dnsjit engine with no linkable C library; Conan-only mdns and pro-mdnsd have no primary metric. Round 3 read all 128 debian-source:dns names (round 1 recorded the first 100) and looked up libraries and packet tools that might carry a decoder: mdnsd's libmdnsd message_parse is public but leaves MX RDATA raw (control failure); avahi and systemd keep their packet code internal; wireshark, libpcap, libnet, libtrace3 and ndpi are capture, construction or classification libraries without a documented message decoder; sofia-sip, lwip and ruli are resolvers; knot-resolver parses with the selected libknot; libowfat carries djbdns's primitives. glibc libresolv ns_initparse/ns_parserr is verified on both controls as a standard/runtime path (not instrumented, no AFL++ feedback, outside the ranking); musl was not run. c-ares, ldns and udns drop the reserved Z bit (z carries AD and CD); knot and getdns report all three bits. Harness-side RDATA formatting (lower-casing, joining the MX preference and exchange) is disclosed per path. Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Popcon counts are package-level, include non-DNS use and are small below c-ares; the cell is not a definitive top ten.

[Ranking and search limits](../../../data/c/dns/ranking.md) · [Standard API inventory](../../../data/c/dns/standard.json)

## Third-party parsers

- [c-ares](c-ares/README.md) — verified Docker harness
- [ldns](ldns/README.md) — verified Docker harness
- [knot](knot/README.md) — verified Docker harness
- [udns](udns/README.md) — verified Docker harness
- [getdns](getdns/README.md) — verified Docker harness

## Standard and runtime APIs

- [glibc libresolv ns_initparse/ns_parserr](standard/glibc-libresolv-ns-initparse-ns-parserr/README.md) — verified API path
