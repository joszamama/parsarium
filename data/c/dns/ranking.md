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

None recorded.

## Checked, excluded or recorded separately

- **adns** (excluded): Resolver library; its public API submits queries and returns parsed answers but documents no parser for caller-supplied message bytes.
- **unbound** (excluded): libunbound's public API is a resolver (ub_resolve) that returns the raw answer packet; the sldns wire parser is internal and not installed as a public API.
- **bind9** (excluded): BIND 9 libdns/libisc are internal to BIND since 9.18; no development headers or documented stable message-parse API are shipped.
- **libevent** (excluded): evdns exposes a resolver and server; message parsing is internal, with no documented API for caller-supplied message bytes.
- **libspf2** (excluded): SPF policy library; not a DNS message parser API.
- **glibc** (standard_runtime): C library resolver API; recorded under standard/runtime, outside third-party ranking.
- **musl** (standard_runtime): C library resolver API; recorded under standard/runtime, outside third-party ranking.
