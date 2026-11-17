# C × DNS: leads (pilot)

No path is verified yet. Leads are ordered by one adoption metric to choose what to verify first; this is not a selection.

## Adoption metric

Debian popcon sourcemax installations (max over binary packages built from the source package), from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Compared only within this cell.

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | [c-ares](https://c-ares.org/docs/ares_dns_parse.3.html) | 43,027 | `ares_dns_parse(buf, len, flags, &dnsrec) (c-ares >= 1.28)` | c-ares own DNS record parser (ares_dns_parse.c, ares_buf.c) |
| 2 | [ldns](https://nlnetlabs.nl/documentation/ldns/wire2host_8h.html) | 1,240 | `ldns_wire2pkt(&pkt, data, len)` | NLnet Labs ldns wire2host |
| 3 | [knot](https://www.knot-dns.cz/docs/latest/html/) | 483 | `knot_pkt_new(wire, len, NULL) + knot_pkt_parse(pkt, 0) (libknot)` | Knot DNS libknot packet parser |
| 4 | [udns](https://www.corpit.ru/mjt/udns/udns.3.html) | 463 | `dns_initparse / dns_nextrr (udns)` | udns own parser |
| 5 | [getdns](https://getdnsapi.net/documentation/spec/) | 118 | `getdns_wire2msg_dict(wire, len, &dict)` | getdns over ldns-derived gldns wire code |

## Excluded or recorded separately

- **adns** (excluded): Resolver library; its public API submits queries and returns parsed answers but documents no parser for caller-supplied message bytes.
- **unbound** (excluded): libunbound's public API is a resolver (ub_resolve) that returns the raw answer packet; the sldns wire parser is internal and not installed as a public API.
- **bind9** (excluded): BIND 9 libdns/libisc are internal to BIND since 9.18; no development headers or documented stable message-parse API are shipped.
- **libevent** (excluded): evdns exposes a resolver and server; message parsing is internal, with no documented API for caller-supplied message bytes.
- **libspf2** (excluded): SPF policy library; not a DNS message parser API.
- **glibc** (standard_runtime): C library resolver API; recorded under standard/runtime, outside third-party ranking.
- **musl** (standard_runtime): C library resolver API; recorded under standard/runtime, outside third-party ranking.
