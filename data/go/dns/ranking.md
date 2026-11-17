# Go × DNS: selected parsers (pilot)

One verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

pkg.go.dev Imported by package count, from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [github.com/miekg/dns](https://pkg.go.dev/github.com/miekg/dns@v1.1.73#Msg.Unpack) | v1.1.73 | 16,234 | miekg/dns v1 (msg.go, msg_helpers.go, zmsg.go generated rdata unpackers) |

**github.com/miekg/dns v1.1.73** (BSD-3-Clause) parses local bytes with `(*dns.Msg).Unpack(msg []byte) error`. Both controls match the oracle summary. The response control covers 207 library lines in 10 files. AFL++ feedback repeats 3 times per control; response and query give 131/73 parser features and 150/92 AFL++ tuples, differing by 60 features and 60 tuples ([receipt](github-com-miekg-dns-feedback-differential.json)). Own pure-Go decoder; CoreDNS and many Go DNS tools build on it. codeberg.org/miekg/dns is a later v2 rewrite by the same author.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | github.com/google/gopacket/layers | 5,428 | `(*layers.DNS).DecodeFromBytes(data, gopacket.NilDecodeFeedback)` | gopacket DNS layer |
| 2 | golang.org/x/net/dns/dnsmessage | 1,202 | `(*dnsmessage.Message).Unpack([]byte) / dnsmessage.Parser` | x/net dnsmessage |
| 3 | github.com/gopacket/gopacket/layers | 171 | `(*layers.DNS).DecodeFromBytes` | gopacket DNS layer (community fork) |
| 4 | codeberg.org/miekg/dns | 39 | `dns.Msg Unpack (v2)` | miekg/dns v2 |
| 5 | github.com/phuslu/fastdns | 9 | `fastdns.ParseMessage(dst, payload, copying)` | phuslu fastdns |

## Checked, excluded or recorded separately

- **github.com/coredns/coredns/plugin/pkg/dnsutil** (excluded): Helper package over miekg/dns; no own message parser.
