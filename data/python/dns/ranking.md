# Python × DNS: selected parsers (pilot)

Seven verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

PyPI Stats last_month downloads excluding known mirrors, from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [dnspython](https://dnspython.readthedocs.io/en/v2.9.2/message-make.html#dns.message.from_wire) | 2.9.2 | 286,812,791 | dnspython wire reader (dns/message.py _WireReader, dns/wire.py Parser, dns/name.py) |
| 2 | [twisted](https://docs.twisted.org/en/twisted-26.10.0/api/twisted.names.dns.Message.html#fromStr) | 26.10.0 | 15,068,322 | Twisted Names (twisted/names/dns.py Message.decode, Query, RRHeader, Name and per-type Record_* decoders) |
| 3 | [mitmproxy](https://docs.mitmproxy.org/stable/api/mitmproxy/dns.html#DNSMessage.unpack) | 12.3.1 | 4,113,220 | mitmproxy DNS (mitmproxy/dns.py DNSMessage.unpack_from over mitmproxy/net/dns/domain_names.py) |
| 4 | [dpkt](https://kbandla.github.io/dpkt/api/api_auto.html#module-dpkt.dns) | 1.9.8 | 1,492,890 | dpkt DNS packet class (dpkt/dns.py) |
| 5 | [dnslib](https://github.com/paulc/dnslib/blob/0.9.26/README.md) | 0.9.26 | 1,231,762 | dnslib (dnslib/dns.py DNSRecord.parse over dnslib/buffer.py and dnslib/label.py) |
| 6 | [py3dns](https://launchpad.net/py3dns) | 4.0.2 | 129,993 | py3dns / PyDNS (DNS/Lib.py Munpacker classes and DnsResult) |
| 7 | [dns-messages](https://github.com/wahlflo/dns-messages#parsing-dns-messages) | 1.0.1 | 46 | dns-messages (DnsMessageParser with per-type rr_data classes) |

**dnspython 2.9.2** (ISC) parses local bytes with `dns.message.from_wire(wire: bytes) -> dns.message.Message`. Both controls match the oracle summary. The response control covers 665 library lines in 27 files. AFL++ feedback repeats 3 times per control; response and query give 665/216 parser features and 685/236 AFL++ tuples, differing by 449 features and 449 tuples ([receipt](dnspython-feedback-differential.json)). Own pure-Python decoder; no C extension and no other DNS library. RRsets group records by owner and type; the harness lists each rdata with its RRset's owner, type, class and TTL.

**twisted 26.10.0** (MIT) parses local bytes with `twisted.names.dns.Message().fromStr(str: bytes) -> None (then the decoded Message fields)`. Both controls match the oracle summary. The response control covers 137 library lines in 1 file. AFL++ feedback repeats 3 times per control; response and query give 137/79 parser features and 157/99 AFL++ tuples, differing by 58 features and 58 tuples ([receipt](twisted-feedback-differential.json)). Own pure-Python decoder in Twisted's DNS package (twisted.names); it uses no other DNS library. Twisted decodes AD and CD but not the reserved Z bit, so z carries AD and CD only (both controls have all three bits clear). A text is Record_A.dottedQuad(); AAAA text is formatted by the harness from the 16 decoded address bytes (RFC 5952). Importing twisted.names.dns imports twisted.internet protocol classes but installs no reactor and opens no socket. Its PyPI count covers the whole Twisted networking framework, not only DNS use.

**mitmproxy 12.3.1** (MIT) parses local bytes with `mitmproxy.dns.DNSMessage.unpack(buffer: bytes, timestamp: float | None = None) -> DNSMessage`. Both controls match the oracle summary. The response control covers 160 library lines in 2 files. AFL++ feedback repeats 3 times per control; response and query give 160/69 parser features and 180/89 AFL++ tuples, differing by 91 features and 91 tuples ([receipt](mitmproxy-feedback-differential.json)). Own pure-Python decoder in mitmproxy's DNS flow model; it uses no other DNS library. It keeps the 3-bit field after RA as `reserved`. unpack decompresses names inside CNAME/MX RDATA; the harness reads A/AAAA through the record's ipv4_address/ipv6_address properties, CNAME through domain_name, and the MX preference and exchange from the decompressed RDATA with the library's domain_names.unpack_from. Importing mitmproxy.dns pulls in mitmproxy's flow and connection model (the full runtime requirement set is installed from pinned wheels), but no proxy, server or event loop is started and no socket is opened. Its PyPI count covers the whole interception proxy, not only DNS use.

**dpkt 1.9.8** (BSD-3-Clause) parses local bytes with `dpkt.dns.DNS(buf: bytes)`. Both controls match the oracle summary. The response control covers 90 library lines in 3 files. AFL++ feedback repeats 3 times per control; response and query give 90/60 parser features and 110/80 AFL++ tuples, differing by 30 features and 30 tuples ([receipt](dpkt-feedback-differential.json)). Own pure-Python decoder in a packet-parsing library; no capture or socket is used. The MX preference is kept as a 1-tuple by dpkt 1.9.8 and the harness reads its value.

**dnslib 0.9.26** (BSD-2-Clause) parses local bytes with `dnslib.DNSRecord.parse(packet: bytes) -> dnslib.DNSRecord`. Both controls match the oracle summary. The response control covers 178 library lines in 6 files. AFL++ feedback repeats 3 times per control; response and query give 178/93 parser features and 198/113 AFL++ tuples, differing by 85 features and 85 tuples ([receipt](dnslib-feedback-differential.json)). Own pure-Python decoder; no other DNS library and no socket. dnslib keeps the reserved Z bit, AD and CD as separate header properties; the harness assembles z from them. RDATA text is dnslib's own toZone() presentation.

**py3dns 4.0.2** (CNRI-Python) parses local bytes with `DNS.Lib.DnsResult(u: DNS.Lib.MunpackerText(buf: bytes), args: dict)`. Both controls match the oracle summary. The response control covers 113 library lines in 5 files. AFL++ feedback repeats 3 times per control; response and query give 113/74 parser features and 133/94 AFL++ tuples, differing by 39 features and 39 tuples ([receipt](py3dns-feedback-differential.json)). Own pure-Python decoder: the Python 3 port of Guido van Rossum's PyDNS (the older pydns distribution is its predecessor). py3dns ships no API reference; the README points to the library code and the bundled DNS/tests/testPackers.py, which drive the same DNS.Lib unpackers on byte strings, and DnsRequest itself decodes replies with DnsResult(MunpackerText(reply)). Importing DNS reads /etc/resolv.conf as a local file; no socket is created. The harness joins the MX (preference, exchange) tuple and adds trailing dots.

**dns-messages 1.0.1** (MIT) parses local bytes with `dns_messages.DnsMessage.from_bytes(raw_bytes: bytes) -> DnsMessage`. Both controls match the oracle summary. The response control covers 208 library lines in 14 files. AFL++ feedback repeats 3 times per control; response and query give 208/160 parser features and 228/180 AFL++ tuples, differing by 48 features and 48 tuples ([receipt](dns-messages-feedback-differential.json)). Own pure-Python decoder (bit-list header unpacking, its own name decompression); no other DNS library. It keeps the 3-bit z field. The bundled DnsServer class is imported with the package but never started, so no socket is created. Its adoption is very low (46 downloads in the window).

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | async-dns | 6,920 | `async_dns.core.DNSMessage.parse(data)` | async_dns (async_dns/core/record.py DNSMessage/Record) |
| 2 | dns-client | 1,213 | `dns_client.Packet.read_from(fp)` | dns_client (protocol.py Packet/Record) |

- **async-dns** (unresolved): No documented message-bytes API: the README documents only the resolver, the server and parse_hosts_file. DNSMessage.parse is exported through async_dns.core but undocumented, so it stays a lead rather than a selected path.
- **dns-client** (unresolved): Exports Packet, Header, Question and Record with a read_from(fp) classmethod, but the README documents only the network DNSClient (query over UDP/TLS). Packet.parse also decodes only the answer section (a TODO notes that authority and additional are not read). Kept as a lead, like async-dns, rather than selected.

## Checked, excluded or recorded separately

- **pycares** (excluded): pycares 5.2.1's public API is a c-ares Channel (query, search, getaddrinfo, gethostbyaddr) that sends queries; its parse_dnsrec(dnsrec) takes a c-ares record handed to a query callback, not caller-supplied bytes. No documented parser for local message bytes. Its parser family is c-ares, verified separately in the C cell.
- **aiodns** (excluded): asyncio resolver over pycares; network API only.
- **scapy** (excluded): Excluded under this pilot's no-socket rule: importing scapy.layers.dns in a --network none container (python:3.13-slim, socket.socket constructor instrumented) created 11 AF_NETLINK sockets while scapy.arch enumerated routes and interfaces, before any parse. The DNS parse itself opened none.
- **pypacker** (excluded): Fails the response control: CNAME and MX rdata are not decoded by the library, so the oracle summary cannot be produced from its parse.
- **dnserver** (excluded): DNS server built on dnslib; no own parser.
- **dnslib-ng** (excluded): Not found on PyPI Stats (404).
- **zeroconf** (excluded): Fails the response control: the MX answer is not decoded and is dropped from the answer list, so the four-record answer section cannot be reproduced from the library's parse. It is an mDNS service-discovery stack; the parser is the multicast DNS subset.
- **pyshark** (excluded): Wraps the external tshark process (a capture-file dissector); no in-process parser for caller-supplied DNS message bytes. Excluded as an external-process wrapper.
- **impacket** (excluded): Fails the response control: AAAA rdata is not decoded and the MX exchange is wrong (offset bug), so the oracle summary cannot be produced from the library's parse.
- **dns-lexicon** (excluded): Manipulates records through DNS hosting providers' HTTP APIs; no DNS wire-message parser.
- **pydns** (excluded): Python 2 PyDNS distribution, the predecessor of the selected py3dns (py3dns is its Python 3 port with the same DNS.Lib unpackers); not counted under the predecessor rule.
- **PythonDNS** (excluded): DNS interception proxy (0.1): PythonDNS/InterceptResolver.py imports dnslib's DNSRecord, RR and DNSServer; no own message parser.
- **dnspython3** (excluded): Separate 2016 distribution of dnspython 1.15.0 for Python 3 (same project, home page dnspython.org); an older release line of the selected dnspython, not counted under the predecessor rule.
- **microdns** (excluded): Test DNS server for the autest suite; its 1.0.3 wheel requires dnslib and trlib and has no own message parser.
- **dnsq** (excluded): Mailgun query tool (dnsq.py 1.1.6) built on dnspython's resolver (import dns.resolver); network API, no own parser.
- **aiodnsresolver** (excluded): asyncio resolver; its README calls the module's pack and parse functions 'otherwise private' (used by the tests' built-in nameserver), so there is no documented message-bytes API.
- **dnsmock** (excluded): Described on PyPI as a custom resolver (21.2b2); no documented API for caller-supplied message bytes.
- **asyncdns2** (excluded): Pure-Python asynchronous resolver: the documentation covers Query, Resolver and Reply objects returned by lookups; replies are decoded inside the resolver's DNSProtocol, with no documented API for caller-supplied message bytes.
- **dnspythonchia** (excluded): Chia's fork of dnspython 2.2.0 (same DNS toolkit and extras); same family as the selected dnspython.
- **dnslib3** (excluded): Fork of the selected dnslib: the 0.10.0 wheel installs the same top-level package name dnslib, and 2,100 of the 3,187 distinct non-blank, non-comment source lines of dnslib 0.9.26 (65.9%) also occur in it. Metric 20.
