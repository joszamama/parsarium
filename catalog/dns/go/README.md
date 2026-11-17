# DNS / Go — pilot

**Status:** pilot_eight_verified_search_bounded; incomplete. 8 verified third-party paths, 0 verified standard APIs, 8 verified Docker harnesses.

Pilot cell: eight Go paths verified (github.com/miekg/dns, github.com/google/gopacket/layers, golang.org/x/net/dns/dnsmessage, codeberg.org/miekg/dns, github.com/benburkert/dns, github.com/phuslu/fastdns, github.com/cznic/dns/msg, tangled.sh/seiso.moe/magna), ranked by pkg.go.dev Imported by package count. Remaining leads: www.bamsoftware.com/git/dnstt.git/dns (unresolved_control_failure), github.com/cybergarage/go-mdns/mdns/dns (unresolved_control_failure). Excluded after checking: github.com/coredns/coredns/plugin/pkg/dnsutil, github.com/gopacket/gopacket/layers, github.com/zmap/dns, github.com/mr-torgue/dns, github.com/pion/mdns, github.com/ncruces/go-dns, github.com/eycorsican/go-tun2socks/common/dns, github.com/hashicorp/mdns, github.com/micro/mdns, github.com/whyrusleeping/mdns, github.com/pion/mdns/v2, github.com/cznic/dns/rr, github.com/asciimoth/gonnect/dns, github.com/bassosimone/dnscodec, github.com/bassosimone/minest, github.com/dmachard/go-netutils, github.com/xtls/xray-core/transport/internet/finalmask/xdns, github.com/Packet-Clearing-House/DNSAuth/libs/dnsdist, github.com/presotto/go-mdns-sd/go_dns (reasons in leads.json). Round 3 added pkg.go.dev searches with the same surface and metric (dns wire, dns codec, dns decode, dns unpack, dnsmessage, mdns, dns rr; first 100 each, under round3_search in the snapshot). The positive-count hits that were opened (the three most-imported mDNS libraries, pion/mdns/v2, codec, wire and tunnel helpers listed in leads.json) either wrap an already selected decoder (miekg/dns, x/net dnsmessage, gopacket, cznic/dns), copy the dnstt control failure, or are not wire parsers; the remaining round-3 hits are mostly go-micro/libp2p service-discovery registry plugins and forks, recognised by package path and not opened. The one new family found (a copy of Go's old net/dnsmsg.go inside go-mdns-sd) has no known importers. The cell therefore stays at eight: no further Go package with a positive pkg.go.dev importer count and its own documented message-bytes decoder was found within the bounded search. gopacket's count covers its whole multi-protocol layers package. The standard library exports no DNS message parser (its net resolver vendors x/net dnsmessage without exporting it). Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/go/dns/ranking.md) · [Standard API inventory](../../../data/go/dns/standard.json)

## Third-party parsers

- [github.com/miekg/dns](github-com-miekg-dns/README.md) — verified Docker harness
- [github.com/google/gopacket/layers](github-com-google-gopacket-layers/README.md) — verified Docker harness
- [golang.org/x/net/dns/dnsmessage](golang-org-x-net-dns-dnsmessage/README.md) — verified Docker harness
- [codeberg.org/miekg/dns](codeberg-org-miekg-dns/README.md) — verified Docker harness
- [github.com/benburkert/dns](github-com-benburkert-dns/README.md) — verified Docker harness
- [github.com/phuslu/fastdns](github-com-phuslu-fastdns/README.md) — verified Docker harness
- [github.com/cznic/dns/msg](github-com-cznic-dns-msg/README.md) — verified Docker harness
- [tangled.sh/seiso.moe/magna](tangled-sh-seiso-moe-magna/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
