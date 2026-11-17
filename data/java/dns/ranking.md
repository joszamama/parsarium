# Java × DNS: leads (pilot)

No path is verified yet. Leads are ordered by one adoption metric to choose what to verify first; this is not a selection.

## Adoption metric

deps.dev directDependentCount summed over all releases, from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Compared only within this cell.

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | [io.netty:netty-codec-dns](https://netty.io/4.1/api/io/netty/handler/codec/dns/DatagramDnsResponseDecoder.html) | 1,038 | `DatagramDnsResponseDecoder / DatagramDnsQueryDecoder over a local DatagramPacket (EmbeddedChannel)` | Netty DNS codec (DnsRecordDecoder) |
| 2 | [dnsjava:dnsjava](https://javadoc.io/doc/dnsjava/dnsjava/latest/org/xbill/DNS/Message.html) | 888 | `new org.xbill.DNS.Message(byte[])` | dnsjava |
| 3 | [org.pcap4j:pcap4j-core](https://javadoc.io/doc/org.pcap4j/pcap4j-core/latest/org/pcap4j/packet/DnsPacket.html) | 210 | `DnsPacket.newPacket(byte[], int, int)` | Pcap4J DnsPacket |
| 4 | [org.minidns:minidns-core](https://javadoc.io/doc/org.minidns/minidns-core/latest/org/minidns/dnsmessage/DnsMessage.html) | 32 | `new org.minidns.dnsmessage.DnsMessage(byte[])` | MiniDNS |

## Excluded or recorded separately

- **de.measite.minidns:minidns-core** (excluded): Old Maven coordinate of MiniDNS; same family as org.minidns:minidns-core.
- **io.vertx:vertx-core** (excluded): The DNS client is a network API over Netty's codec; no documented message-bytes parser of its own. Its count is for all of vertx-core.
- **org.xbill:dnsjava** (excluded): Not on deps.dev (404); the published coordinate is dnsjava:dnsjava.
