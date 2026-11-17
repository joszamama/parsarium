# PHP × DNS: selected parsers (pilot)

One verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

Packagist total downloads, from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [react/dns](https://github.com/reactphp/dns/blob/v1.14.0/src/Protocol/Parser.php#L16-L35) | v1.14.0 | 179,404,103 | ReactPHP DNS protocol Parser (src/Protocol/Parser.php) |

**react/dns v1.14.0** (MIT) parses local bytes with `React\Dns\Protocol\Parser::parseMessage(string $data): Message`. Both controls match the oracle summary. The response control covers 108 library lines in 4 files. AFL++ feedback repeats 3 times per control; response and query give 108/49 parser features and 128/69 AFL++ tuples, differing by 59 features and 59 tuples ([receipt](react-dns-feedback-differential.json)). Own pure-PHP decoder (unpack, readDomain with pointer following, inet_ntop for addresses). It drops the Z, AD and CD bits, so z is reported as 0.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | daverandom/libdns | 66,619,313 | `(new LibDNS\Decoder\DecoderFactory)->create()->decode($data)` | LibDNS |
| 2 | pear/net_dns2 | 3,392,919 | `new Net_DNS2_Packet_Response($data, strlen($data))` | Net_DNS2 |
| 3 | purplepixie/phpdns | 1,540,214 |  | PHPDNS |
| 4 | mikepultz/netdns2 | 632,286 | `NetDNS2\Packet\Response` | Net_DNS2 |
| 5 | jdwx/dns-query | 6,451 |  |  |
| 6 | yswery/dns | 4,664 | `yswery\DNS\Decoder::decodeMessage($message)` | yswery DNS server decoder |
| 7 | appserver-io/dnsserver | 2,280 |  |  |

## Checked, excluded or recorded separately

- **amphp/dns** (excluded): Async resolver; message decoding is delegated to daverandom/libdns. No own documented message-bytes parser.
- **spatie/dns** (excluded): Runs the external dig command; excluded (external process, network).
- **remotelyliving/php-dns** (excluded): Resolver wrapper; network API only.
- **badcow/dns** (excluded): Zone-file text library; not a wire-message parser.
