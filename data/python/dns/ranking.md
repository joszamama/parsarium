# Python × DNS: selected parsers (pilot)

One verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

PyPI Stats last_month downloads excluding known mirrors, from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [dnspython](https://dnspython.readthedocs.io/en/v2.9.2/message-make.html#dns.message.from_wire) | 2.9.2 | 286,812,791 | dnspython wire reader (dns/message.py _WireReader, dns/wire.py Parser, dns/name.py) |

**dnspython 2.9.2** (ISC) parses local bytes with `dns.message.from_wire(wire: bytes) -> dns.message.Message`. Both controls match the oracle summary. The response control covers 665 library lines in 27 files. AFL++ feedback repeats 3 times per control; response and query give 665/216 parser features and 685/236 AFL++ tuples, differing by 449 features and 449 tuples ([receipt](dnspython-feedback-differential.json)). Own pure-Python decoder; no C extension and no other DNS library. RRsets group records by owner and type; the harness lists each rdata with its RRset's owner, type, class and TTL.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | pycares | 17,928,720 | `resolver API over c-ares` | c-ares |
| 2 | scapy | 4,173,275 | `scapy.layers.dns.DNS(raw_bytes)` | Scapy DNS layer |
| 3 | dpkt | 1,492,890 | `dpkt.dns.DNS(buf)` | dpkt DNS |
| 4 | dnslib | 1,231,762 | `dnslib.DNSRecord.parse(packet)` | dnslib |
| 5 | py3dns | 129,993 | `DNS.Lib.DnsResult / Munpacker` | py3dns |
| 6 | pypacker | 3,765 |  | pypacker |

## Checked, excluded or recorded separately

- **aiodns** (excluded): asyncio resolver over pycares; network API only.
- **dnserver** (excluded): DNS server built on dnslib; no own parser.
- **dnslib-ng** (excluded): Not found on PyPI Stats (404).
