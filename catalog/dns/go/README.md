# DNS / Go — pilot

**Status:** pilot_two_verified_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: two Go paths verified, miekg/dns and gopacket's layers.DNS, ranked by pkg.go.dev known importing packages. gopacket's count covers its whole multi-protocol layers package. golang.org/x/net/dns/dnsmessage, codeberg.org/miekg/dns, the gopacket community fork and phuslu/fastdns remain leads. The standard library exports no DNS message parser. Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use; the remaining leads are unverified, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/go/dns/ranking.md) · [Standard API inventory](../../../data/go/dns/standard.json)

## Third-party parsers

- [github.com/miekg/dns](github-com-miekg-dns/README.md) — verified Docker harness
- [github.com/google/gopacket/layers](github-com-google-gopacket-layers/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
