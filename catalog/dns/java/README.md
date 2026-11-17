# DNS / Java — pilot

**Status:** pilot_four_verified_search_bounded; incomplete. 4 verified third-party paths, 0 verified standard APIs, 4 verified Docker harnesses.

Pilot cell: four Java paths verified, netty-codec-dns, dnsjava, pcap4j-core and minidns-core, ranked by deps.dev direct dependents summed over releases (a weak signal; Pcap4J's count covers its whole multi-protocol artifact). Netty leaves A/AAAA as raw records (the harness formats the decoded bytes) and its DnsQuery has no AA/TC/RA/RCODE. Pcap4J's names come from DnsDomainName.decompress, whose leading '.' for pointer-only names the harness drops, and its coverage and AFL++ feedback are scoped to its DNS classes. MiniDNS decodes AD and CD but not the reserved Z bit. Round 2 added targeted deps.dev lookups for the plausible Maven search hits: ApacheDS's DNS decoder fails the response control by source inspection (no CNAME decoder), the Netty backport and Netty 5 alpha are the selected Netty family, ph-dns and spotify dns wrap dnsjava, happy-dns keeps its parser package-private, ninio-dns and the Direct Project DNS are network applications, and the Scala codecs dns4s and otavia stay unresolved pending a decision on Scala artifacts in a Java cell. Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/java/dns/ranking.md) · [Standard API inventory](../../../data/java/dns/standard.json)

## Third-party parsers

- [netty-codec-dns](netty-codec-dns/README.md) — verified Docker harness
- [dnsjava](dnsjava/README.md) — verified Docker harness
- [pcap4j-core](pcap4j-core/README.md) — verified Docker harness
- [minidns-core](minidns-core/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
