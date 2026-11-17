# Go × DNS: selected parsers (pilot)

Four verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

pkg.go.dev Imported by package count, from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17 (round-2 targeted lookups under `round2_targeted`, same source and day). Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [github.com/miekg/dns](https://pkg.go.dev/github.com/miekg/dns@v1.1.73#Msg.Unpack) | v1.1.73 | 16,234 | miekg/dns v1 (msg.go, msg_helpers.go, zmsg.go generated rdata unpackers) |
| 2 | [github.com/google/gopacket/layers](https://pkg.go.dev/github.com/google/gopacket@v1.1.19/layers#DNS.DecodeFromBytes) | v1.1.19 | 5,428 | gopacket DNS layer (layers/dns.go) |
| 3 | [golang.org/x/net/dns/dnsmessage](https://pkg.go.dev/golang.org/x/net@v0.63.0/dns/dnsmessage#Message.Unpack) | v0.63.0 | 1,202 | Go x/net dnsmessage (dns/dnsmessage/message.go) |
| 4 | [codeberg.org/miekg/dns](https://pkg.go.dev/codeberg.org/miekg/dns@v0.6.133#Msg.Unpack) | v0.6.133 | 39 | miekg/dns v2 rewrite (msg.go, zmsg.go, internal/unpack, pkg/dnsnet, rdata) |

**github.com/miekg/dns v1.1.73** (BSD-3-Clause) parses local bytes with `(*dns.Msg).Unpack(msg []byte) error`. Both controls match the oracle summary. The response control covers 207 library lines in 10 files. AFL++ feedback repeats 3 times per control; response and query give 131/73 parser features and 150/92 AFL++ tuples, differing by 60 features and 60 tuples ([receipt](github-com-miekg-dns-feedback-differential.json)). Own pure-Go decoder; CoreDNS and many Go DNS tools build on it. codeberg.org/miekg/dns is a later v2 rewrite by the same author.

**github.com/google/gopacket/layers v1.1.19** (BSD-3-Clause) parses local bytes with `(*layers.DNS).DecodeFromBytes(data []byte, df gopacket.DecodeFeedback) error`. Both controls match the oracle summary. The response control covers 282 library lines in 3 files. AFL++ feedback repeats 3 times per control; response and query give 86/67 parser features and 105/87 AFL++ tuples, differing by 19 features and 18 tuples ([receipt](github-com-google-gopacket-layers-feedback-differential.json)). Own pure-Go decoder inside Google's packet-decoding library; no libpcap is used (the pcap subpackage is not imported). It keeps the 3-bit Z field. Its importer count covers the whole multi-protocol layers package. github.com/gopacket/gopacket is a community fork of the same code.

**golang.org/x/net/dns/dnsmessage v0.63.0** (BSD-3-Clause) parses local bytes with `(*dnsmessage.Message).Unpack(msg []byte) error`. Both controls match the oracle summary. The response control covers 203 library lines in 1 file. AFL++ feedback repeats 3 times per control; response and query give 115/78 parser features and 135/98 AFL++ tuples, differing by 37 features and 37 tuples ([receipt](golang-org-x-net-dns-dnsmessage-feedback-differential.json)). Own pure-Go decoder maintained by the Go team; the standard library's net resolver vendors a copy of the same package internally (vendor/golang.org/x/net/dns/dnsmessage), which exports no API, so the cell has no standard path. dnsmessage keeps AD and CD but not the reserved Z bit, so z reports AD and CD only. A and AAAA bodies are fixed byte arrays; the harness prints them with net/netip. Its importer count is for this package only.

**codeberg.org/miekg/dns v0.6.133** (BSD-3-Clause) parses local bytes with `(*dns.Msg).Unpack() error`. Both controls match the oracle summary. The response control covers 154 library lines in 9 files. AFL++ feedback repeats 3 times per control; response and query give 104/47 parser features and 123/67 AFL++ tuples, differing by 57 features and 56 tuples ([receipt](codeberg-org-miekg-dns-feedback-differential.json)). Same author as the selected github.com/miekg/dns v1 but a separate module and a rewrite, not a rename: only 1,699 of the 7,165 distinct non-test source lines of its root package (23.7%) also occur in v1.1.73's root package, and the decoder moved to internal/unpack and pkg/dnsnet with rdata in its own package. Shared family with miekg/dns v1 is stated; the API differs (the caller puts the bytes in Msg.Data before Unpack, questions are RRs). It keeps the Z, AD and CD bits. Its importer count is low because it is pre-1.0 (v0.6.x).

## Remaining leads

| Order | Lead | Metric | Status | Input API lead | Family |
| ---: | --- | ---: | --- | --- | --- |
| 1 | github.com/gopacket/gopacket/layers | 171 | unresolved | `(*layers.DNS).DecodeFromBytes` | gopacket DNS layer (community fork) |
| 2 | github.com/phuslu/fastdns | 9 | unresolved | `fastdns.ParseMessage(dst, payload, copying)` | phuslu fastdns |

## Checked, excluded or recorded separately

- **github.com/coredns/coredns/plugin/pkg/dnsutil** (excluded): Helper package over miekg/dns; no own message parser.
