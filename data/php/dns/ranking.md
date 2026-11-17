# PHP × DNS: leads (pilot)

No path is verified yet. Leads are ordered by one adoption metric to choose what to verify first; this is not a selection.

## Adoption metric

Packagist total downloads, from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Compared only within this cell.

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | [react/dns](https://github.com/reactphp/dns#readme) | 179,404,103 | `(new React\Dns\Protocol\Parser())->parseMessage($data)` | ReactPHP DNS protocol parser |
| 2 | [daverandom/libdns](https://github.com/DaveRandom/LibDNS#readme) | 66,619,313 | `(new LibDNS\Decoder\DecoderFactory)->create()->decode($data)` | LibDNS |
| 3 | [pear/net_dns2](https://netdns2.com/documentation/) | 3,392,919 | `new Net_DNS2_Packet_Response($data, strlen($data))` | Net_DNS2 |
| 4 | [purplepixie/phpdns](https://www.purplepixie.org/phpdns/) | 1,540,214 |  | PHPDNS |
| 5 | [mikepultz/netdns2](https://netdns2.com/documentation/) | 632,286 | `NetDNS2\Packet\Response` | Net_DNS2 |
| 6 | [jdwx/dns-query](https://packagist.org/packages/jdwx/dns-query) | 6,451 |  |  |
| 7 | [yswery/dns](https://github.com/yswery/PHP-DNS-SERVER) | 4,664 | `yswery\DNS\Decoder::decodeMessage($message)` | yswery DNS server decoder |
| 8 | [appserver-io/dnsserver](https://packagist.org/packages/appserver-io/dnsserver) | 2,280 |  |  |

## Excluded or recorded separately

- **amphp/dns** (excluded): Async resolver; message decoding is delegated to daverandom/libdns. No own documented message-bytes parser.
- **spatie/dns** (excluded): Runs the external dig command; excluded (external process, network).
- **remotelyliving/php-dns** (excluded): Resolver wrapper; network API only.
- **badcow/dns** (excluded): Zone-file text library; not a wire-message parser.
