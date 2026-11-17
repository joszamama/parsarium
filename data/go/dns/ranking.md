# Go × DNS: leads (pilot)

No path is verified yet. Leads are ordered by one adoption metric to choose what to verify first; this is not a selection.

## Adoption metric

pkg.go.dev Imported by package count, from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Compared only within this cell.

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | [github.com/miekg/dns](https://pkg.go.dev/github.com/miekg/dns#Msg.Unpack) | 16,234 | `(*dns.Msg).Unpack([]byte)` | miekg/dns (v1) |
| 2 | [github.com/google/gopacket/layers](https://pkg.go.dev/github.com/google/gopacket/layers#DNS.DecodeFromBytes) | 5,428 | `(*layers.DNS).DecodeFromBytes(data, gopacket.NilDecodeFeedback)` | gopacket DNS layer |
| 3 | [golang.org/x/net/dns/dnsmessage](https://pkg.go.dev/golang.org/x/net/dns/dnsmessage#Message.Unpack) | 1,202 | `(*dnsmessage.Message).Unpack([]byte) / dnsmessage.Parser` | x/net dnsmessage |
| 4 | [github.com/gopacket/gopacket/layers](https://pkg.go.dev/github.com/gopacket/gopacket/layers#DNS.DecodeFromBytes) | 171 | `(*layers.DNS).DecodeFromBytes` | gopacket DNS layer (community fork) |
| 5 | [codeberg.org/miekg/dns](https://pkg.go.dev/codeberg.org/miekg/dns) | 39 | `dns.Msg Unpack (v2)` | miekg/dns v2 |
| 6 | [github.com/phuslu/fastdns](https://pkg.go.dev/github.com/phuslu/fastdns) | 9 | `fastdns.ParseMessage(dst, payload, copying)` | phuslu fastdns |

## Excluded or recorded separately

- **github.com/coredns/coredns/plugin/pkg/dnsutil** (excluded): Helper package over miekg/dns; no own message parser.
