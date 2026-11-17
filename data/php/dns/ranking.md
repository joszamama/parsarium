# PHP × DNS: selected parsers (pilot)

Three verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

Packagist total downloads, from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [react/dns](https://github.com/reactphp/dns/blob/v1.14.0/src/Protocol/Parser.php#L16-L35) | v1.14.0 | 179,404,103 | ReactPHP DNS protocol Parser (src/Protocol/Parser.php) |
| 2 | [daverandom/libdns](https://github.com/DaveRandom/LibDNS/blob/v2.1.0/examples/AQuery.php) | v2.1.0 | 66,619,313 | LibDNS (Decoder, DecodingContext, Packets\Packet and Records\Types decoders) |
| 3 | [pear/net_dns2](https://github.com/mikepultz/netdns2/blob/v2.0.7/src/NetDNS2/Packet/Response.php) | v2.0.7 | 3,392,919 | Net_DNS2 / NetDNS2 (Packet, Header, Question and per-type RR rrSet decoders) |

**react/dns v1.14.0** (MIT) parses local bytes with `React\Dns\Protocol\Parser::parseMessage(string $data): Message`. Both controls match the oracle summary. The response control covers 108 library lines in 4 files. AFL++ feedback repeats 3 times per control; response and query give 108/49 parser features and 128/69 AFL++ tuples, differing by 59 features and 59 tuples ([receipt](react-dns-feedback-differential.json)). Own pure-PHP decoder (unpack, readDomain with pointer following, inet_ntop for addresses). It drops the Z, AD and CD bits, so z is reported as 0.

**daverandom/libdns v2.1.0** (MIT) parses local bytes with `LibDNS\Decoder\Decoder::decode(string $data): LibDNS\Messages\Message (from (new DecoderFactory)->create(null, false))`. Both controls match the oracle summary. The response control covers 594 library lines in 40 files. AFL++ feedback repeats 3 times per control; response and query give 591/407 parser features and 611/427 AFL++ tuples, differing by 184 features and 184 tuples ([receipt](daverandom-libdns-feedback-differential.json)). Own pure-PHP decoder; amphp/dns and danog's DNS packages delegate message decoding to it. It drops the Z, AD and CD bits, so z is reported as 0. php-fuzzer's include-interceptor cannot rewrite Records/Types/DomainName.php (a PHP_INT_SIZE ternary class constant), so the php-fuzzer entry loads that one file through the native file:// wrapper and re-registers the interceptor; Xdebug coverage and the AFL++ bridge count it normally.

**pear/net_dns2 v2.0.7** (MIT) parses local bytes with `NetDNS2\Packet\Response::__construct(string $_data, int $_size)`. Both controls match the oracle summary. The response control covers 192 library lines in 19 files. AFL++ feedback repeats 3 times per control; response and query give 192/92 parser features and 212/112 AFL++ tuples, differing by 100 features and 100 tuples ([receipt](pear-net-dns2-feedback-differential.json)). Own pure-PHP decoder. pear/net_dns2 2.x is the namespaced NetDNS2 code from the mikepultz/netdns2 repository, so mikepultz/netdns2 on Packagist shares this family. Keeps Z, AD and CD.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | utopia-php/dns | 196,676 | `Utopia\DNS\Message::decode($packet)` | Utopia DNS |
| 2 | jdwx/dns-query | 6,451 | `new JDWX\DNSQuery\Packet\ResponsePacket($data, strlen($data))` | jdwx DNSQuery (Net_DNS2 1.x fork) |
| 3 | yswery/dns | 4,664 | `yswery\DNS\Decoder::decodeMessage($message)` | yswery DNS server decoder |

## Checked, excluded or recorded separately

- **amphp/dns** (excluded): Async resolver; message decoding is delegated to daverandom/libdns. No own documented message-bytes parser.
- **spatie/dns** (excluded): Runs the external dig command; excluded (external process, network).
- **purplepixie/phpdns** (excluded): Network client only: the README describes 'a socket-level direct network DNS client'; DNSQuery parses replies inside query() through private readResponse/readRecord over the socket buffer, and no public API accepts caller-supplied message bytes.
- **mikepultz/netdns2** (excluded): Same project as the selected pear/net_dns2: both Packagist names point to the mikepultz/netdns2 repository, Packagist marks pear/net_dns2 abandoned in favour of this name, and mikepultz/netdns2 v2.0.7 is the same commit (5353baa6...) as the pinned pear/net_dns2 v2.0.7. Its newest v2.0.8 keeps 3,157 of v2.0.7's 3,303 distinct normalized non-blank, non-comment src lines (95.6%). Not counted twice under the rename/predecessor rule; pear/net_dns2 keeps the slot as the higher-adoption name.
- **remotelyliving/php-dns** (excluded): Resolver wrapper; network API only.
- **badcow/dns** (excluded): Zone-file text library; not a wire-message parser.
- **appserver-io/dnsserver** (excluded): DNS server application on appserver.io's threaded server stack (appserver-io/server, appserver-io/concurrency, PHP >=5.4 era); it documents no parser API for caller-supplied message bytes.
- **bluelibraries/dns** (excluded): Resolver library: the README documents record retrieval through dns_get_record, dig and raw UDP/TCP queries; its Raw\RawDataResponse decoder is constructed from a RawDataRequest inside the socket handlers and is not documented for caller-supplied bytes.
- **danog/libdns-json** (excluded): Encoder/decoder for Google's JSON DNS format on top of daverandom/libdns; not a wire-format parser.
- **danog/dns-over-https** (excluded): DNS-over-HTTPS resolver (network API); message decoding is delegated to daverandom/libdns.
- **icicleio/dns** (excluded): Asynchronous resolver for the Icicle framework; message decoding is delegated to daverandom/libdns 1.x.
- **plesk/net_dns2** (excluded): Plesk's fork of the PEAR Net_DNS2 1.x code (psr-0 Net_DNS2, latest v1.5.4), i.e. the predecessor line of the selected pear/net_dns2 2.x; not counted under the predecessor rule.
- **metaregistrar/php-dns-client** (excluded): No tagged release on Packagist (dev-master only), so no pinned release can be verified; it is a network DNS client.
- **splitice/dns-query** (excluded): No tagged release on Packagist (dev-master only), so no pinned release can be verified.
- **nytris/dns** (excluded): Wrapper over react/dns and react/cache (its only dependencies); no own message parser.
- **php-standard-library/dns** (excluded): Async resolver; its wire decoder is Psl\DNS\Internal\Decoder in an internal namespace, not a documented public API.
- **hiblaphp/dns** (excluded): Async resolver for the HiblaPHP event loop (pre-release 1.0.0-beta.2); no documented message-bytes parser API.
- **clue/mdns-react** (excluded): Multicast DNS resolver over react/dns; no own parser.
- **danog/libdns-native** (excluded): Converts between PHP's dns_get_record raw format and daverandom/libdns messages; not a separate wire-format parser.
