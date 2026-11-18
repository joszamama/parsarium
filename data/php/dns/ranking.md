# PHP × DNS: selected parsers (pilot)

Five verified third-party path(s), ranked by one metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

Packagist total downloads, from [registry-snapshot.json](registry-snapshot.json) captured 2026-11-17. Package-level counts include non-DNS use and are compared only within this cell.

| Rank | Package | Release | Packagist downloads (all time) | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [react/dns](https://github.com/reactphp/dns/blob/v1.14.0/src/Protocol/Parser.php#L16-L35) | v1.14.0 | 179,404,103 | ReactPHP DNS protocol Parser (src/Protocol/Parser.php) |
| 2 | [daverandom/libdns](https://github.com/DaveRandom/LibDNS/blob/v2.1.0/examples/AQuery.php) | v2.1.0 | 66,619,313 | LibDNS (Decoder, DecodingContext, Packets\Packet and Records\Types decoders) |
| 3 | [pear/net_dns2](https://github.com/mikepultz/netdns2/blob/v2.0.7/src/NetDNS2/Packet/Response.php) | v2.0.7 | 3,392,919 | Net_DNS2 / NetDNS2 (Packet, Header, Question and per-type RR rrSet decoders) |
| 4 | [utopia-php/dns](https://github.com/utopia-php/dns/blob/3.1.0/README.md) | 3.1.0 | 196,676 | Utopia DNS (Message, Message/Header, Question, Record and Domain decoders) |
| 5 | [jdwx/dns-query](https://github.com/jdwx/dns-query/blob/v2.0.11/src/Packet/ResponsePacket.php) | v2.0.11 | 6,451 | jdwx DNSQuery (Net_DNS2 1.x fork: Packet, Header, Question and per-type RR rrSet decoders) |

**react/dns v1.14.0** (MIT) parses local bytes with `React\Dns\Protocol\Parser::parseMessage(string $data): Message`. Both controls match the oracle summary. The response control covers 108 library lines in 4 files. AFL++ feedback repeats 3 times per control; response and query give 108/49 parser features and 128/69 AFL++ tuples, differing by 59 features and 59 tuples ([receipt](react-dns-feedback-differential.json)). Own pure-PHP decoder (unpack, readDomain with pointer following, inet_ntop for addresses). It drops the Z, AD and CD bits, so z is reported as 0.

**daverandom/libdns v2.1.0** (MIT) parses local bytes with `LibDNS\Decoder\Decoder::decode(string $data): LibDNS\Messages\Message (from (new DecoderFactory)->create(null, false))`. Both controls match the oracle summary. The response control covers 594 library lines in 40 files. AFL++ feedback repeats 3 times per control; response and query give 591/407 parser features and 611/427 AFL++ tuples, differing by 184 features and 184 tuples ([receipt](daverandom-libdns-feedback-differential.json)). Own pure-PHP decoder; amphp/dns and danog's DNS packages delegate message decoding to it. It drops the Z, AD and CD bits, so z is reported as 0. php-fuzzer's include-interceptor cannot rewrite Records/Types/DomainName.php (a PHP_INT_SIZE ternary class constant), so the php-fuzzer entry loads that one file through the native file:// wrapper and re-registers the interceptor; Xdebug coverage and the AFL++ bridge count it normally.

**pear/net_dns2 v2.0.7** (MIT) parses local bytes with `NetDNS2\Packet\Response::__construct(string $_data, int $_size)`. Both controls match the oracle summary. The response control covers 192 library lines in 19 files. AFL++ feedback repeats 3 times per control; response and query give 192/92 parser features and 212/112 AFL++ tuples, differing by 100 features and 100 tuples ([receipt](pear-net-dns2-feedback-differential.json)). Own pure-PHP decoder. pear/net_dns2 2.x is the namespaced NetDNS2 code from the mikepultz/netdns2 repository, so mikepultz/netdns2 on Packagist shares this family. Keeps Z, AD and CD.

**utopia-php/dns 3.1.0** (MIT) parses local bytes with `Utopia\DNS\Message::decode(string $packet): Message`. Both controls match the oracle summary. The response control covers 181 library lines in 5 files. AFL++ feedback repeats 3 times per control; response and query give 181/113 parser features and 201/133 AFL++ tuples, differing by 68 features and 68 tuples ([receipt](utopia-php-dns-feedback-differential.json)). Own pure-PHP decoder (unpack, Domain::decode with backward-only pointer following, inet_ntop for addresses) in Appwrite's DNS server toolkit. It ignores the Z, AD and CD bits, so z is reported as 0. The package pulls in its telemetry and validator dependencies; only Message::decode runs.

**jdwx/dns-query v2.0.11** (BSD-2-Clause) parses local bytes with `JDWX\DNSQuery\Packet\ResponsePacket::__construct(string $i_data, int $i_size)`. Both controls match the oracle summary. The response control covers 156 library lines in 10 files. AFL++ feedback repeats 3 times per control; response and query give 156/87 parser features and 176/107 AFL++ tuples, differing by 69 features and 69 tuples ([receipt](jdwx-dns-query-feedback-differential.json)). Forked from Net_DNS2 1.x and rewritten for PHP 8.1 (README credits Mike Pultz). It shares the Net_DNS2 family with the selected pear/net_dns2 2.x path but is a separate rewrite: 196 of its 3,279 distinct normalized non-blank, non-comment source lines (6.0%) also occur in pear/net_dns2 v2.0.7's src. Keeps Z, AD and CD. Types and classes are mnemonics mapped back through the library's Lookups tables; AAAA text is compressed from the library's uncompressed hex groups.

## Remaining leads

| Order | Lead | Metric | Input API lead | Family |
| ---: | --- | ---: | --- | --- |
| 1 | cboxdk/dns | 6,740 | `Cbox\Dns\Protocol\Decoder::decode(string $message, RecordType $expected, string $host, ...)` |  |
| 2 | yswery/dns | 4,664 | `yswery\DNS\Decoder::decodeMessage($message)` | yswery DNS server decoder |

- **cboxdk/dns** (unresolved_control_failure): Raw-socket resolver toolkit. Its Protocol\Decoder::decode (not covered by the documentation, which describes typed lookups) requires the expected type and host and returns a DnsResponse with records and rcode: by source inspection of v1.1.0 it discards the header ID, QR, opcode, TC, RD, RA and the question entries and does not keep record classes, so the oracle summary cannot be produced from its parse.
- **yswery/dns** (unresolved): Lead only: the package is a DNS server; yswery\DNS\Decoder::decodeMessage(string) is public but neither the README nor its docblock (@param/@return only) documents decoding caller-supplied message bytes. Not built.

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
- **dapphp/torutils** (excluded): Tor control-protocol and DNSEL utilities; v2.0.0beta1's TorDNSEL class builds and reads its own DNS query packets inside the network lookup (no public API for caller-supplied message bytes), and its count covers the whole Tor toolkit.
- **danog/php-rtc-mdns** (excluded): Amp multicast DNS resolver for WebRTC; 1.1.12 requires daverandom/libdns (selected) for message decoding. No own parser.
- **ljpc/pure-php-doh-client** (excluded): DNS-over-HTTPS client: 1.3.0 decodes responses inside the static DNS::query() call (private processHeader/getHeader and per-type decode() helpers fed from the HTTPS response), with no public API for caller-supplied message bytes.
- **chieftools/dns-resolver** (excluded): Recursive resolver with DNSSEC validation; v1.5.0 requires mikepultz/netdns2 (the selected Net_DNS2 family) and uses it as its transport and packet layer.
- **mezon/dns-client** (excluded): Service-name registry (getServices, resolveHost, setService); 1.0.1 has no DNS wire-format code.
- **zanphp/dns-client** (excluded): No tagged release (dev-master only); the client calls swoole_async_dns_lookup, with no message parser.
- **domraider/libdns** (excluded): Fork of daverandom/libdns (same 'DNS protocol implementation written in pure PHP' code base) with no tagged release (1.0.x-dev only).
- **quasarstream/mdns** (excluded): mDNS resolver; v1.0.0 requires react/dns (selected) for message handling. No own parser.
- **sharkydog/mdns** (excluded): mDNS resolver and responder; v1.8 requires react/dns (selected). No own parser.
- **hoa/dns** (excluded): Hoa\Dns is a DNS server event loop: its Resolver parses incoming queries inside the socket server and documents no message-bytes parser.
- **noglitchyo/dealdoh** (excluded): DNS-over-HTTPS proxy (pre-release 0.4.0-beta) that requires react/dns for message handling.
- **rafalmasiarek/dns-resolver** (excluded): From-scratch resolver client; its DnsMessageDecoder::decode(data, expectedId, type) is not documented in the README (which documents the resolver contract) and returns only answers of the queried type.
- **arrayaccess/dns-client** (excluded): Resolver client: the README documents only lookup(); packet classes are used internally by the resolver.
- **thruster/dns** (excluded): Port of an early ReactPHP DNS component to the Thruster event loop (its Parser::parseChunk mirrors react/dns's old chunked parser); resolver API only, 38 downloads.
- **ipokbr/dns** (excluded): Parses dig text output lines (Aux_Func::fill_dns_array splits host/ttl/class/type/data), not DNS wire messages.
- **kakserpom/phpdaemon** (excluded): Asynchronous application framework (pre-release v1.0-beta2); its DNS client parses replies in Clients\DNS\Connection::onUdpPacket, a connection callback that resolves the pending request's callback, with no documented API for caller-supplied message bytes. The download count covers the whole framework.
- **sirmonti/doh** (excluded): DNS-over-HTTPS resolver for Google and Cloudflare: the README documents only static dns($name, $type) lookups over HTTPS returning answer arrays; no wire-format message parser for caller-supplied bytes.
- **yocto/yoclib-dns** (excluded): RDATA codec only: the README documents deserialising one record's RDATA from wire or presentation format by class and type; there is no message, header, question or name-compression decoder.
- **horde/dns** (excluded): Zone and record management backends (Bind9, Rdo database, Mock); no tagged release on Packagist and no wire-format parser.
- **yggverse/net** (excluded): Network helpers whose Dig::records runs the external dig command (+short); no message parser.
- **chielteuben/php-dns-extended** (excluded): Maintained fork of the excluded remotelyliving/php-dns resolver wrapper; network API only.
- **php-standard-library/dnssec** (excluded): DNSSEC validator built on the excluded php-standard-library/dns resolver, whose wire decoder is internal API; no own documented message parser.
- **anquanssl/dns** (excluded): GitHub fork of the excluded bluelibraries/dns resolver library; same code base, resolver API only.
- **bluelibraries/php5-dns** (excluded): PHP 5 edition of the excluded bluelibraries/dns resolver library; resolver API only.
