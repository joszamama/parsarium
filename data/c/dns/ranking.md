# C × DNS: selected parsers (pilot)

Five verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

Debian popcon sourcemax installations (max over binary packages built from the source package), from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [c-ares](https://c-ares.org/docs/ares_dns_parse.html) | 1.34.9 | 43,027 | c-ares DNS record parser (src/lib/record/ares_dns_parse.c, ares_dns_name.c over ares_buf.c) |
| 2 | [ldns](https://nlnetlabs.nl/documentation/ldns/wire2host_8h.html) | 1.8.4 | 1,240 | NLnet Labs ldns (wire2host.c, rr.c, packet.c, str2host/host2str for presentation) |
| 3 | [knot](https://gitlab.nic.cz/knot/knot-dns/-/blob/v3.6.2/src/libknot/packet/pkt.h) | 3.6.2 | 483 | Knot DNS libknot (packet/pkt.c, packet/rrset-wire.c, dname.c; rrset-dump.c for presentation) |
| 4 | [udns](https://www.corpit.ru/mjt/udns/udns.3.html) | 0.7 | 463 | udns (Michael Tokarev) raw-packet routines (udns_parse.c, udns_dn.c, udns_XtoX.c) |
| 5 | [getdns](https://getdnsapi.net/doxygen/group__UDNSDataConversionFunctions.html) | 1.7.3 | 118 | getdns message-dict decoder (src/rr-iter.c, src/rr-dict.c, src/util-internal.c over the bundled gldns read helpers) |

**c-ares 1.34.9** (MIT) parses local bytes with `ares_dns_parse(const unsigned char *buf, size_t buf_len, unsigned int flags, ares_dns_record_t **dnsrec)`. Both controls match the oracle summary. The response control covers 1,037 library lines in 58 files. AFL++ feedback repeats 3 times per control; response and query give 837/555 parser features and 393/272 AFL++ tuples, differing by 282 features and 125 tuples ([receipt](c-ares-feedback-differential.json)). Own C decoder; it is also the parser behind Node.js dns, pycares and many resolvers. It keeps AD/CD but not the reserved Z bit.

**ldns 1.8.4** (BSD-3-Clause) parses local bytes with `ldns_status ldns_wire2pkt(ldns_pkt **packet, const uint8_t *data, size_t len)`. Both controls match the oracle summary. The response control covers 785 library lines in 42 files. AFL++ feedback repeats 3 times per control; response and query give 529/412 parser features and 406/329 AFL++ tuples, differing by 117 features and 83 tuples ([receipt](ldns-feedback-differential.json)). Own C decoder; getdns bundles gldns derived from ldns, and Unbound's internal sldns shares the lineage. Built without OpenSSL; presentation text comes from ldns_rdf2str. It has no Z getter, so z carries AD and CD only.

**knot 3.6.2** (GPL-2.0-or-later) parses local bytes with `knot_pkt_t *knot_pkt_new(void *wire, uint16_t len, knot_mm_t *mm) + int knot_pkt_parse(knot_pkt_t *pkt, unsigned flags)`. Both controls match the oracle summary. The response control covers 957 library lines in 57 files. AFL++ feedback repeats 3 times per control; response and query give 875/266 parser features and 250/80 AFL++ tuples, differing by 609 features and 170 tuples ([receipt](knot-feedback-differential.json)). Own C decoder of the Knot DNS authoritative server, shipped as the libknot library (Debian source knot, binary libknot-dev). Only libknot is built (no daemon, utilities or modules); presentation text comes from knot_rrset_txt_dump_data, lower-cased by the harness. libknot exposes the reserved Z bit, AD and CD separately, so z carries all three.

**udns 0.7** (LGPL-2.1-or-later) parses local bytes with `dns_getdn(pkt, &cur, end, dn, dnsiz) for question names, then void dns_initparse(struct dns_parse *p, dnscc_t *qdn, dnscc_t *pkt, dnscc_t *cur, dnscc_t *end) + int dns_nextrr(struct dns_parse *p, struct dns_rr *rr), with the dns_qid/dns_qr/.../dns_numar header accessors`. Both controls match the oracle summary. The response control covers 110 library lines in 4 files. AFL++ feedback repeats 3 times per control; response and query give 100/72 parser features and 110/86 AFL++ tuples, differing by 28 features and 24 tuples ([receipt](udns-feedback-differential.json)). Own C decoder of an asynchronous stub-resolver library; only its documented low-level parsing routines are called and no resolver context is created. The routines return each RR's owner, type, class, TTL and RDATA span; the harness renders RDATA with udns calls (dns_ntop for A/AAAA, dns_getdn + dns_dntop for names, dns_get16 for the MX preference) and reads authority/additional by resetting dnsp_rrl to the section count. udns has accessors for AD and CD but none for the reserved Z bit, so z carries AD and CD only.

**getdns 1.7.3** (BSD-3-Clause) parses local bytes with `getdns_return_t getdns_wire2msg_dict(const uint8_t *wire, size_t wire_sz, getdns_dict **msg_dict)`. Both controls match the oracle summary. The response control covers 881 library lines in 58 files. AFL++ feedback repeats 3 times per control; response and query give 860/629 parser features and 701/533 AFL++ tuples, differing by 231 features and 168 tuples ([receipt](getdns-feedback-differential.json)). getdns walks the message with its own rr-iter.c/rr-dict.c iterators and builds the message dict in util-internal.c; it bundles gldns, an import of Unbound's sldns (ldns lineage). Distinct normalized non-blank source lines (comments removed, gldns_ mapped to ldns_): getdns's own decoder files rr-iter.c, rr-dict.c, util-internal.c, convert.c, dict.c and list.c share 75 of 3,228 lines (2.3%) with ldns 1.8.4's *.c; the bundled gldns *.c share 1,128 of 3,610 (31.2%). Kept as a distinct package API with the shared lineage stated. Built stub-only without libunbound; no context is created. Names come from getdns_convert_dns_name_to_fqdn and addresses from getdns_display_ip_address; the harness lower-cases names and joins the MX preference and exchange. getdns reports the reserved Z bit, AD and CD separately, so z carries all three.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family | Status |
| ---: | --- | ---: | --- | --- | --- |
| 1 | gnunet | 58 | `struct GNUNET_DNSPARSER_Packet *GNUNET_DNSPARSER_parse(const char *udp_payload, size_t udp_payload_length) (gnunet_dnsparser_lib.h, libgnunetutil)` | GNUnet DNSPARSER (src/util/dnsparser.c) | unresolved |
| 2 | mdnsd | 28 | `int message_parse(struct message *m, unsigned char *packet) (libmdnsd/1035.h)` | mdnsd (Jeremie Miller's 1035.c, troglobit fork) | unresolved_control_failure |
| 3 | dnsjit | 4 | `Lua core.object.dns (parse) inside the dnsjit engine` | DNS-OARC dnsjit core.object.dns | unresolved |
| 4 | yadifa | 1 | `dns_packet_reader_init(reader, buffer, size) then dns_packet_reader_read_record (dnscore/dns_packet_reader.h)` | YADIFA dnscore | unresolved |
| 5 | mdns | missing | `` | mjansson/mdns (header-only mDNS) | unresolved_no_primary_metric |
| 6 | pro-mdnsd | missing | `` | mdnsd (Jeremie Miller) fork | unresolved_no_primary_metric |
| 7 | firedns | missing | `` | firedns | unresolved_no_primary_metric |
| 8 | s6-dns | missing | `s6dns_message_parse_init / s6dns_message_parse_next and per-type s6dns_message_get_* (libs6dns)` | skarnet s6-dns | unresolved_no_primary_metric |
| 9 | wdns | missing | `wdns_parse_message(wdns_message_t *m, const uint8_t *pkt, size_t len)` | Farsight wdns | unresolved_no_primary_metric |
| 10 | dnsparse | missing | `` | dnsparse (Robert Graham) | unresolved_no_primary_metric |

- **gnunet**: Documented own decoder (header comment: 'Parse a UDP payload of a DNS packet in to a nice struct'): it decodes the header flags (Z, AD and CD included), questions, and names inside CNAME/NS/PTR/MX RDATA with compression. Not verified because it does not keep the TTL: GNUNET_DNSPARSER_parse_record stores expiration_time = now + TTL from the wall clock, and the library's own serializer recovers a TTL by truncating the remaining time, which yields TTL-1 once any time has passed. Reporting the controls' TTLs would need harness arithmetic on the clock, so it stays a lead. A/AAAA RDATA would also stay raw bytes.
- **mdnsd**: Debian builds libmdnsd-dev with libmdnsd/1035.h, whose message_parse decodes the header, questions and records of caller-supplied bytes, but by source inspection of v1.2 (libmdnsd/1035.c) the record parser decodes only A, AAAA, NS, CNAME, PTR, SRV and TXT RDATA; the MX answer of controls/dns/response.bin keeps raw RDATA, so its exchange name is not decoded by the library.
- **dnsjit**: Not attempted this round. dnsjit is a LuaJIT engine program: Debian builds dnsjit and an Architecture: all dnsjit-dev that installs only usr/include and man3 pages, so there is no linkable C library; the documented parser is the Lua core.object.dns module, which a harness would have to drive through the dnsjit executable and a Lua script.
- **yadifa**: Debian's libyadifa-dev is Architecture: all and installs only usr/include (no shared or static library); the YADIFA name server links its dnscore statically. The packet reader has terse header comments but no API reference, so there is no documented library API for caller-supplied messages. Not attempted; popcon 1.
- **mdns**: Conan recipe only; no Debian source package in the pinned popcon table, so no primary metric and no Debian dev-package fallback. GitHub stars are not allowed outside PLY cells.
- **pro-mdnsd**: Conan recipe only; no Debian source package in the pinned popcon table, so no primary metric and no Debian dev-package fallback. GitHub stars are not allowed outside PLY cells.
- **firedns**: Asynchronous resolver library last packaged in Debian jessie (0.9.12); absent from the pinned popcon table, so no primary metric and no Debian dev-package fallback. Not attempted.
- **s6-dns**: skarnet's libs6dns documents message-parsing functions and is packaged in Alpine, but Debian has no s6-dns source package (sources.debian.org 404; only skalibs), so there is no primary metric and no Debian dev-package fallback. Not attempted.
- **wdns**: Farsight Security's low-level DNS wire library, distributed through Farsight's own package repository; no Debian source package, so no primary metric. Not attempted.
- **dnsparse**: Stand-alone DNS response parser on GitHub with no Debian source package; no primary metric. Not attempted.

## Checked, excluded or recorded separately

- **adns** (excluded): Resolver library; its public API submits queries and returns parsed answers but documents no parser for caller-supplied message bytes.
- **unbound** (excluded): libunbound's public API is a resolver (ub_resolve) that returns the raw answer packet; the sldns wire parser is internal and not installed as a public API.
- **bind9** (excluded): BIND 9 libdns/libisc are internal to BIND since 9.18; no development headers or documented stable message-parse API are shipped.
- **libevent** (excluded): evdns exposes a resolver and server; message parsing is internal, with no documented API for caller-supplied message bytes.
- **libspf2** (excluded): SPF policy library; not a DNS message parser API.
- **glibc** (standard_runtime): C library resolver API, recorded under standard/runtime outside the third-party ranking. glibc 2.43 libresolv ns_initparse/ns_parserr (Ubuntu 2.43-2ubuntu2.7 in the pinned image) passes both controls; see standard.json.
- **musl** (standard_runtime): C library resolver API; recorded under standard/runtime, outside third-party ranking.
- **libmicrodns** (excluded): mDNS client/announcer library. Its installed header microdns.h exports only mdns_init, mdns_destroy, mdns_entries_send, mdns_entries_print, mdns_strerror, mdns_listen, mdns_announce, mdns_serve and mdns_request_initial_announce; message parsing is internal to the socket loop, with no documented API for caller-supplied message bytes.
- **libjdns** (excluded): Resolver/mDNS session library. src/jdns/CMakeLists.txt installs only jdns.h and jdns_export.h as public headers; the packet decoder (jdns_packet.h) is private, so no documented API parses caller-supplied message bytes.
- **djbdns** (excluded): Server and client programs; Debian builds no library or development package, and the dns_packet_* routines are internal to the programs.
- **mdnsresponder** (excluded): No Debian source package (no primary metric); its public dns_sd.h API registers, browses and resolves services over the daemon and documents no parser for caller-supplied message bytes.
- **avahi** (excluded): mDNS/DNS-SD daemon and libraries; libavahi-core-dev installs core, lookup, publish, rr and log headers but not the packet decoder (avahi-core/dns.h is internal), so there is no documented API for caller-supplied message bytes.
- **systemd** (excluded): systemd-resolved's DNS packet code is internal to the daemon; libsystemd-dev installs no DNS message parser API.
- **nss-mdns** (excluded): NSS module that resolves .local names through the Avahi daemon; no DNS message parser API.
- **dnsmasq** (excluded): DNS forwarder and DHCP server program; Debian builds no library or development package.
- **libpcap** (excluded): Packet-capture library; it reads frames and does not decode DNS messages.
- **libnet** (excluded): Packet construction library (libnet_build_dnsv4 builds headers); it does not parse DNS messages.
- **wireshark** (excluded): libwireshark (libwireshark-dev) dissects captured frames through its epan dissector framework; the DNS dissector is a registered dissector (packet-dns.c), not a documented library API for caller-supplied DNS message bytes.
- **sofia-sip** (excluded): SIP stack; its sresolv/sres resolver sends queries and returns record structures (sres_record.h), decoding replies inside the resolver; no API for caller-supplied message bytes.
- **ndpi** (excluded): Deep-packet-inspection flow classifier over IP packets; it extracts DNS metadata (query name, response addresses) for classification and exposes no message decoder.
- **knot-resolver** (excluded): Resolver daemon and libkres; DNS messages are parsed with libknot, whose packet parser is already selected as the knot path.
- **lwip** (excluded): Embedded TCP/IP stack; lwip/dns.h is a resolver (dns_gethostbyname) and lwip/apps/mdns.h a responder, both parsing replies internally; no API for caller-supplied message bytes.
- **libowfat** (excluded): Its dns.h carries djbdns's routines (excluded djbdns family): dns_packet_copy/getname/skipname primitives and per-type answer extractors such as dns_ip4_packet and dns_mx_packet; no decoder of the header, questions and record sections.
- **libtrace3** (excluded): Trace-processing library; libpacketdump's protocol decoders print packets read from capture traces and need link-layer frames, with no documented API that returns a decoded DNS message.
- **ruli** (excluded): SRV resolver library (asynchronous queries); no API for caller-supplied message bytes.
- **mongoose** (excluded): Fails the response control by source inspection of mongoose.h 7.23: struct mg_dns_message keeps one name and one resolved address, and struct mg_dns_rr has only name length, type, class and RDATA length (no TTL); CNAME and MX RDATA are not decoded.
- **belle-sip** (excluded): SIP stack that bundles William Ahern's dns.c under src/dns; its installed headers (include/belle-sip/) expose only the SIP resolver (resolver.h), not the dns_p_* packet API. No documented message-bytes API.
- **lua-cqueues** (excluded): Lua module: dns.c's packet parser is exposed only as the Lua cqueues.dns.packet object, not as a C library API; outside the C cell like dnsjit's Lua parser.
- **rspamd** (excluded): Spam-filter daemon whose bundled librdns resolver is private to rspamd (Debian builds no rspamd development package); no documented message-bytes API.
- **opensmtpd** (excluded): Mail server that bundles OpenBSD's asynchronous resolver (asr); its _asr_unpack_* message routines are internal and no library or header is installed. No documented message-bytes API.
- **pjproject** (excluded): No primary metric (absent from the pinned popcon table; Debian ships pjproject 2.17 only in experimental), and by source inspection of pjlib-util/src/pjlib-util/dns.c 2.17 parse_rr decodes RDATA only for A, AAAA, CNAME, NS, PTR and SRV, leaving the MX answer as raw data (response-control failure).
