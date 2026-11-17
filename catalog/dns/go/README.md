# DNS / Go — pilot

**Status:** pilot_eight_verified_search_bounded; incomplete. 8 verified third-party paths, 0 verified standard APIs, 8 verified Docker harnesses.

Pilot cell: eight Go paths verified (github.com/miekg/dns, github.com/google/gopacket/layers, golang.org/x/net/dns/dnsmessage, codeberg.org/miekg/dns, github.com/benburkert/dns, github.com/phuslu/fastdns, github.com/cznic/dns/msg, tangled.sh/seiso.moe/magna), ranked by pkg.go.dev Imported by package count. Remaining leads: www.bamsoftware.com/git/dnstt.git/dns (unresolved_control_failure), github.com/cybergarage/go-mdns/mdns/dns (unresolved_control_failure). Excluded after checking: github.com/coredns/coredns/plugin/pkg/dnsutil, github.com/gopacket/gopacket/layers, github.com/zmap/dns, github.com/mr-torgue/dns, github.com/pion/mdns, github.com/ncruces/go-dns, github.com/eycorsican/go-tun2socks/common/dns (reasons in leads.json). gopacket's count covers its whole multi-protocol layers package. The standard library exports no DNS message parser (its net resolver vendors x/net dnsmessage without exporting it). Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use, and the cell is not a definitive top ten.

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
