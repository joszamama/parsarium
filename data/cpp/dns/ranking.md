# C++ × DNS: leads (pilot)

No path is verified yet. Leads are ordered by one adoption metric to choose what to verify first; this is not a selection.

## Adoption metric

Debian popcon sourcemax installations (max over binary packages built from the source package), from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Compared only within this cell.

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | [libtins](https://libtins.github.io/docs/latest/d0/dcd/classTins_1_1DNS.html) | 52 | `Tins::DNS(const uint8_t *buffer, uint32_t total_sz)` | libtins DNS PDU parser |

Unranked leads (no primary metric): pcapplusplus.

## Excluded or recorded separately

- **poco** (excluded): Resolver over getaddrinfo/gethostbyname; no DNS message bytes API.
- **qtbase-opensource-src** (excluded): QDnsLookup performs network lookups; it documents no parser for caller-supplied message bytes.
- **boost1.83** (excluded): getaddrinfo wrapper; no DNS message parser.
- **asio** (excluded): getaddrinfo wrapper; no DNS message parser.
- **pdns** (excluded): Authoritative server application; its MOADNSParser is internal, not an installed library.
- **dnsdist** (excluded): Load-balancer application, not a library.
- **pdns-recursor** (excluded): Resolver application, not a library.
