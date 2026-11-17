# Python × DNS: leads (pilot)

No path is verified yet. Leads are ordered by one adoption metric to choose what to verify first; this is not a selection.

## Adoption metric

PyPI Stats last_month downloads excluding known mirrors, from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Compared only within this cell.

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | [dnspython](https://dnspython.readthedocs.io/en/stable/message-make.html#dns.message.from_wire) | 286,812,791 | `dns.message.from_wire(wire)` | dnspython |
| 2 | [pycares](https://pycares.readthedocs.io/) | 17,928,720 | `resolver API over c-ares` | c-ares |
| 3 | [scapy](https://scapy.readthedocs.io/en/latest/api/scapy.layers.dns.html) | 4,173,275 | `scapy.layers.dns.DNS(raw_bytes)` | Scapy DNS layer |
| 4 | [dpkt](https://kbandla.github.io/dpkt/api/api_auto.html#module-dpkt.dns) | 1,492,890 | `dpkt.dns.DNS(buf)` | dpkt DNS |
| 5 | [dnslib](https://github.com/paulc/dnslib#readme) | 1,231,762 | `dnslib.DNSRecord.parse(packet)` | dnslib |
| 6 | [py3dns](https://launchpad.net/py3dns) | 129,993 | `DNS.Lib.DnsResult / Munpacker` | py3dns |
| 7 | [pypacker](https://gitlab.com/mike01/pypacker) | 3,765 |  | pypacker |

## Excluded or recorded separately

- **aiodns** (excluded): asyncio resolver over pycares; network API only.
- **dnserver** (excluded): DNS server built on dnslib; no own parser.
- **dnslib-ng** (excluded): Not found on PyPI Stats (404).
