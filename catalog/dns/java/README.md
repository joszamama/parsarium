# DNS / Java — pilot

**Status:** pilot_five_verified_search_bounded; incomplete. 5 verified third-party paths, 0 verified standard APIs, 5 verified Docker harnesses.

Pilot cell: five JVM paths verified, netty-codec-dns, dnsjava, pcap4j-core, minidns-core and the Scala library dns4s-core_2.13, ranked by deps.dev direct dependents summed over releases (a weak signal; Pcap4J's count covers its whole multi-protocol artifact). The cell stays below ten because no further qualifying path was found in the bounded search. Scala libraries count in this Java cell when they document a JVM API, as Scala and Kotlin libraries such as circe-yaml and ktoml do in other Java cells; dns4s is ranked by its Scala 2.13 coordinate only. Netty leaves A/AAAA as raw records (the harness formats the decoded bytes) and its DnsQuery has no AA/TC/RA/RCODE. Pcap4J's names come from DnsDomainName.decompress, whose leading '.' for pointer-only names the harness drops, and its coverage and AFL++ feedback are scoped to its DNS classes. MiniDNS decodes AD and CD but not the reserved Z bit; dns4s decodes none of Z, AD and CD. Round 2 added targeted deps.dev lookups for the plausible Maven search hits: the Netty backport and Netty 5 alpha are the selected Netty family, ph-dns and spotify dns wrap dnsjava, happy-dns keeps its parser package-private, and ninio-dns and the Direct Project DNS are network applications. Round 3 added Maven searches for dns packet, parser, protocol, decoder, mdns and jmdns: ApacheDS's DnsMessageDecoder was run and throws on the CNAME answer (no CNAME decoder), otavia's DNS codec 0.4.5 has only a query encoder, JmDNS keeps its message reader in its implementation package and skips MX, and Pekko's DNS codec is internal API. Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/java/dns/ranking.md) · [Standard API inventory](../../../data/java/dns/standard.json)

## Third-party parsers

- [netty-codec-dns](netty-codec-dns/README.md) — verified Docker harness
- [dnsjava](dnsjava/README.md) — verified Docker harness
- [pcap4j-core](pcap4j-core/README.md) — verified Docker harness
- [minidns-core](minidns-core/README.md) — verified Docker harness
- [dns4s-core_2.13](dns4s-core-2-13/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
