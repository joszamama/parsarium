# Java × DNS: selected parsers (pilot)

Three verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

deps.dev directDependentCount summed over all releases, from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [netty-codec-dns](https://netty.io/4.2/api/io/netty/handler/codec/dns/DatagramDnsResponseDecoder.html) | 4.2.21.Final | 1,038 | Netty DNS codec (DnsResponseDecoder, DnsMessageUtil, DefaultDnsRecordDecoder, DnsCodecUtil) |
| 2 | [dnsjava](https://javadoc.io/doc/dnsjava/dnsjava/3.7.1/org/xbill/DNS/Message.html#%3Cinit%3E(byte%5B%5D)) | 3.7.1 | 888 | dnsjava (org.xbill.DNS Message, Header, DNSInput, Name and per-type rrFromWire) |
| 3 | [pcap4j-core](https://javadoc.io/doc/org.pcap4j/pcap4j-core/1.8.2/org/pcap4j/packet/DnsPacket.html) | 1.8.2 | 210 | Pcap4J DNS packet classes (DnsPacket, DnsDomainName, DnsResourceRecord, DnsRData*) |

**netty-codec-dns 4.2.21.Final** (Apache-2.0) parses local bytes with `new DatagramDnsResponseDecoder() / new DatagramDnsQueryDecoder() in an EmbeddedChannel, fed new DatagramPacket(ByteBuf, recipient, sender)`. Both controls match the oracle summary. The response control covers 414 library lines in 15 files. AFL++ feedback repeats 3 times per control; response and query give 414/277 parser features and 433/295 AFL++ tuples, differing by 251 features and 250 tuples ([receipt](netty-codec-dns-feedback-differential.json)). Own Java decoder; Vert.x's DNS client and Netty's DnsNameResolver use it. Netty leaves A/AAAA (and MX/CNAME after decompression) as raw records, so the harness formats addresses from the decoded bytes and reads names with the public DefaultDnsRecordDecoder.decodeName. DnsQuery carries no AA/TC/RA/RCODE; they are reported as 0 for the query control.

**dnsjava 3.7.1** (BSD-3-Clause) parses local bytes with `org.xbill.DNS.Message(byte[] b) throws IOException`. Both controls match the oracle summary. The response control covers 467 library lines in 21 files. AFL++ feedback repeats 3 times per control; response and query give 467/376 parser features and 487/396 AFL++ tuples, differing by 91 features and 91 tuples ([receipt](dnsjava-feedback-differential.json)). Own Java decoder; keeps the raw flags word, so Z, AD and CD are all reported. Presentation text is dnsjava's rdataToString except AAAA, which the harness formats from the decoded 16 bytes as RFC 5952 text.

**pcap4j-core 1.8.2** (MIT) parses local bytes with `org.pcap4j.packet.DnsPacket.newPacket(byte[] rawData, int offset, int length) throws IllegalRawDataException`. Both controls match the oracle summary. The response control covers 575 library lines in 14 files. AFL++ feedback repeats 3 times per control; response and query give 575/437 parser features and 595/457 AFL++ tuples, differing by 138 features and 138 tuples ([receipt](pcap4j-core-feedback-differential.json)). Own Java decoder inside the Pcap4J packet library (pinned to 1.8.2, the latest non-pre-release; 2.0.0-alpha.6 is the deps.dev default). The documented DnsPacket.newPacket(byte[], int, int) decodes a DNS message from caller-supplied bytes; no capture handle, interface or libpcap call is used (JNA is on the class path but never loads a native library). RDATA comes from the documented runtime module pcap4j-packetfactory-static 1.8.2. Pcap4J keeps the reserved Z bit, AD and CD. Names are decompressed with the documented DnsDomainName.decompress(message); for a name that is only a compression pointer Pcap4J returns a leading '.', which the harness drops. AAAA text is formatted by the harness from the decoded 16 bytes (RFC 5952). Its deps.dev count covers the whole multi-protocol pcap4j-core artifact. Coverage and AFL++ features are scoped to Pcap4J's DNS classes (org.pcap4j.packet.Dns*, namednumber.Dns*, StaticDnsRDataFactory and util.ByteArrays): building the first RDATA loads the static factory binder, which initialises every protocol's named-number tables (TcpPort, UdpPort, IpNumber and others) and would otherwise make up most of the response control's features.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | org.minidns:minidns-core | 32 | `new org.minidns.dnsmessage.DnsMessage(byte[])` | MiniDNS |

## Checked, excluded or recorded separately

- **de.measite.minidns:minidns-core** (excluded): Old Maven coordinate of MiniDNS; same family as org.minidns:minidns-core.
- **io.vertx:vertx-core** (excluded): The DNS client is a network API over Netty's codec; no documented message-bytes parser of its own. Its count is for all of vertx-core.
- **org.xbill:dnsjava** (excluded): Not on deps.dev (404); the published coordinate is dnsjava:dnsjava.
