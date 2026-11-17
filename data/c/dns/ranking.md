# C × DNS: selected parsers (pilot)

One verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

Debian popcon sourcemax installations (max over binary packages built from the source package), from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [c-ares](https://c-ares.org/docs/ares_dns_parse.html) | 1.34.9 | 43,027 | c-ares DNS record parser (src/lib/record/ares_dns_parse.c, ares_dns_name.c over ares_buf.c) |

**c-ares 1.34.9** (MIT) parses local bytes with `ares_dns_parse(const unsigned char *buf, size_t buf_len, unsigned int flags, ares_dns_record_t **dnsrec)`. Both controls match the oracle summary. The response control covers 1,037 library lines in 58 files. AFL++ feedback repeats 3 times per control; response and query give 837/555 parser features and 393/272 AFL++ tuples, differing by 282 features and 125 tuples ([receipt](c-ares-feedback-differential.json)). Own C decoder; it is also the parser behind Node.js dns, pycares and many resolvers. It keeps AD/CD but not the reserved Z bit.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | ldns | 1,240 | `ldns_wire2pkt(&pkt, data, len)` | NLnet Labs ldns wire2host |
| 2 | knot | 483 | `knot_pkt_new(wire, len, NULL) + knot_pkt_parse(pkt, 0) (libknot)` | Knot DNS libknot packet parser |
| 3 | udns | 463 | `dns_initparse / dns_nextrr (udns)` | udns own parser |
| 4 | getdns | 118 | `getdns_wire2msg_dict(wire, len, &dict)` | getdns over ldns-derived gldns wire code |

## Checked, excluded or recorded separately

- **adns** (excluded): Resolver library; its public API submits queries and returns parsed answers but documents no parser for caller-supplied message bytes.
- **unbound** (excluded): libunbound's public API is a resolver (ub_resolve) that returns the raw answer packet; the sldns wire parser is internal and not installed as a public API.
- **bind9** (excluded): BIND 9 libdns/libisc are internal to BIND since 9.18; no development headers or documented stable message-parse API are shipped.
- **libevent** (excluded): evdns exposes a resolver and server; message parsing is internal, with no documented API for caller-supplied message bytes.
- **libspf2** (excluded): SPF policy library; not a DNS message parser API.
- **glibc** (standard_runtime): C library resolver API; recorded under standard/runtime, outside third-party ranking.
- **musl** (standard_runtime): C library resolver API; recorded under standard/runtime, outside third-party ranking.
