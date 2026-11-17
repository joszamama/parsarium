# C++ × DNS: selected parsers (pilot)

One verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

Debian popcon sourcemax installations (max over binary packages built from the source package), from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [libtins](https://libtins.github.io/docs/latest/d0/dcd/classTins_1_1DNS.html) | 4.6 | 52 | libtins DNS PDU (src/dns.cpp with its Memory::InputMemoryStream reader) |

**libtins 4.6** (BSD-2-Clause) parses local bytes with `Tins::DNS::DNS(const uint8_t *buffer, uint32_t total_sz); queries(), answers(), authority(), additional() and header getters`. Both controls match the oracle summary. The response control covers 426 library lines in 20 files. AFL++ feedback repeats 3 times per control; response and query give 204/150 parser features and 459/264 AFL++ tuples, differing by 54 features and 209 tuples ([receipt](libtins-feedback-differential.json)). Own C++ decoder; built here without libpcap, so no capture or socket code is linked in. Keeps the Z, AD and CD bits.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | pcapplusplus | missing | `pcpp::DnsLayer(uint8_t *data, size_t dataLen, Layer *prevLayer, Packet *packet)` | PcapPlusPlus DnsLayer |

## Checked, excluded or recorded separately

- **poco** (excluded): Resolver over getaddrinfo/gethostbyname; no DNS message bytes API.
- **qtbase-opensource-src** (excluded): QDnsLookup performs network lookups; it documents no parser for caller-supplied message bytes.
- **boost1.83** (excluded): getaddrinfo wrapper; no DNS message parser.
- **asio** (excluded): getaddrinfo wrapper; no DNS message parser.
- **pdns** (excluded): Authoritative server application; its MOADNSParser is internal, not an installed library.
- **dnsdist** (excluded): Load-balancer application, not a library.
- **pdns-recursor** (excluded): Resolver application, not a library.
