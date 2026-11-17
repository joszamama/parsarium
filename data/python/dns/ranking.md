# Python × DNS: selected parsers (pilot)

Four verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

PyPI Stats last_month downloads excluding known mirrors, from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [dnspython](https://dnspython.readthedocs.io/en/v2.9.2/message-make.html#dns.message.from_wire) | 2.9.2 | 286,812,791 | dnspython wire reader (dns/message.py _WireReader, dns/wire.py Parser, dns/name.py) |
| 2 | [dpkt](https://kbandla.github.io/dpkt/api/api_auto.html#module-dpkt.dns) | 1.9.8 | 1,492,890 | dpkt DNS packet class (dpkt/dns.py) |
| 3 | [dnslib](https://github.com/paulc/dnslib/blob/0.9.26/README.md) | 0.9.26 | 1,231,762 | dnslib (dnslib/dns.py DNSRecord.parse over dnslib/buffer.py and dnslib/label.py) |
| 4 | [py3dns](https://launchpad.net/py3dns) | 4.0.2 | 129,993 | py3dns / PyDNS (DNS/Lib.py Munpacker classes and DnsResult) |

**dnspython 2.9.2** (ISC) parses local bytes with `dns.message.from_wire(wire: bytes) -> dns.message.Message`. Both controls match the oracle summary. The response control covers 665 library lines in 27 files. AFL++ feedback repeats 3 times per control; response and query give 665/216 parser features and 685/236 AFL++ tuples, differing by 449 features and 449 tuples ([receipt](dnspython-feedback-differential.json)). Own pure-Python decoder; no C extension and no other DNS library. RRsets group records by owner and type; the harness lists each rdata with its RRset's owner, type, class and TTL.

**dpkt 1.9.8** (BSD-3-Clause) parses local bytes with `dpkt.dns.DNS(buf: bytes)`. Both controls match the oracle summary. The response control covers 90 library lines in 3 files. AFL++ feedback repeats 3 times per control; response and query give 90/60 parser features and 110/80 AFL++ tuples, differing by 30 features and 30 tuples ([receipt](dpkt-feedback-differential.json)). Own pure-Python decoder in a packet-parsing library; no capture or socket is used. The MX preference is kept as a 1-tuple by dpkt 1.9.8 and the harness reads its value.

**dnslib 0.9.26** (BSD-2-Clause) parses local bytes with `dnslib.DNSRecord.parse(packet: bytes) -> dnslib.DNSRecord`. Both controls match the oracle summary. The response control covers 178 library lines in 6 files. AFL++ feedback repeats 3 times per control; response and query give 178/93 parser features and 198/113 AFL++ tuples, differing by 85 features and 85 tuples ([receipt](dnslib-feedback-differential.json)). Own pure-Python decoder; no other DNS library and no socket. dnslib keeps the reserved Z bit, AD and CD as separate header properties; the harness assembles z from them. RDATA text is dnslib's own toZone() presentation.

**py3dns 4.0.2** (CNRI-Python) parses local bytes with `DNS.Lib.DnsResult(u: DNS.Lib.MunpackerText(buf: bytes), args: dict)`. Both controls match the oracle summary. The response control covers 113 library lines in 5 files. AFL++ feedback repeats 3 times per control; response and query give 113/74 parser features and 133/94 AFL++ tuples, differing by 39 features and 39 tuples ([receipt](py3dns-feedback-differential.json)). Own pure-Python decoder: the Python 3 port of Guido van Rossum's PyDNS (the older pydns distribution is its predecessor). py3dns ships no API reference; the README points to the library code and the bundled DNS/tests/testPackers.py, which drive the same DNS.Lib unpackers on byte strings, and DnsRequest itself decodes replies with DnsResult(MunpackerText(reply)). Importing DNS reads /etc/resolv.conf as a local file; no socket is created. The harness joins the MX (preference, exchange) tuple and adds trailing dots.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | pypacker | 3,765 |  | pypacker |

## Checked, excluded or recorded separately

- **pycares** (excluded): pycares 5.2.1's public API is a c-ares Channel (query, search, getaddrinfo, gethostbyaddr) that sends queries; its parse_dnsrec(dnsrec) takes a c-ares record handed to a query callback, not caller-supplied bytes. No documented parser for local message bytes. Its parser family is c-ares, verified separately in the C cell.
- **aiodns** (excluded): asyncio resolver over pycares; network API only.
- **scapy** (excluded): Excluded under this pilot's no-socket rule: importing scapy.layers.dns in a --network none container (python:3.13-slim, socket.socket constructor instrumented) created 11 AF_NETLINK sockets while scapy.arch enumerated routes and interfaces, before any parse. The DNS parse itself opened none.
- **dnserver** (excluded): DNS server built on dnslib; no own parser.
- **dnslib-ng** (excluded): Not found on PyPI Stats (404).
