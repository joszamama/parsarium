# Java × DNS: selected parsers (pilot)

One verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

deps.dev directDependentCount summed over all releases, from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [netty-codec-dns](https://netty.io/4.2/api/io/netty/handler/codec/dns/DatagramDnsResponseDecoder.html) | 4.2.21.Final | 1,038 | Netty DNS codec (DnsResponseDecoder, DnsMessageUtil, DefaultDnsRecordDecoder, DnsCodecUtil) |

**netty-codec-dns 4.2.21.Final** (Apache-2.0) parses local bytes with `new DatagramDnsResponseDecoder() / new DatagramDnsQueryDecoder() in an EmbeddedChannel, fed new DatagramPacket(ByteBuf, recipient, sender)`. Both controls match the oracle summary. The response control covers 414 library lines in 15 files. AFL++ feedback repeats 3 times per control; response and query give 414/277 parser features and 433/295 AFL++ tuples, differing by 251 features and 250 tuples ([receipt](netty-codec-dns-feedback-differential.json)). Own Java decoder; Vert.x's DNS client and Netty's DnsNameResolver use it. Netty leaves A/AAAA (and MX/CNAME after decompression) as raw records, so the harness formats addresses from the decoded bytes and reads names with the public DefaultDnsRecordDecoder.decodeName. DnsQuery carries no AA/TC/RA/RCODE; they are reported as 0 for the query control.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | dnsjava:dnsjava | 888 | `new org.xbill.DNS.Message(byte[])` | dnsjava |
| 2 | org.pcap4j:pcap4j-core | 210 | `DnsPacket.newPacket(byte[], int, int)` | Pcap4J DnsPacket |
| 3 | org.minidns:minidns-core | 32 | `new org.minidns.dnsmessage.DnsMessage(byte[])` | MiniDNS |

## Checked, excluded or recorded separately

- **de.measite.minidns:minidns-core** (excluded): Old Maven coordinate of MiniDNS; same family as org.minidns:minidns-core.
- **io.vertx:vertx-core** (excluded): The DNS client is a network API over Netty's codec; no documented message-bytes parser of its own. Its count is for all of vertx-core.
- **org.xbill:dnsjava** (excluded): Not on deps.dev (404); the published coordinate is dnsjava:dnsjava.
