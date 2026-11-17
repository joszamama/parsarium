# DNS / JavaScript — pilot

**Status:** pilot_ten_verified_search_bounded; incomplete. 10 verified third-party paths, 0 verified standard APIs, 10 verified Docker harnesses.

Pilot cell at the ten-path ceiling, ranked by npm 30-day downloads (round-1 window). Families: dns-packet with two forks (@dnsquery/dns-packet, kept as a rewrite at 4.3% shared distinct source lines, 29.8% normalised; @noelminamino/dns-packet, a fork of @dnsquery that shares 38.8% of its distinct lines with it, kept as a separate package API with the overlap recorded) and dns-message (a DataView rewrite derived from dns-packet, 0.6% shared); independent decoders dns2, native-dns-packet, hbo-dnsd (dnsd fork; the original dnsd is the excluded near-identical pair), dns-js, @gibme/dns and @portable/dns-packet. Z handling differs: hbo-dnsd and @portable/dns-packet report AD and CD only; several harnesses compress AAAA text per RFC 5952 from the library's decoded groups, and type/class names are mapped back with each package's own tables (dns-packet forks, hbo-dnsd, @gibme/dns, @portable/dns-packet via its unexported dist/codes.js). dns2's and @gibme/dns's line totals include module-load lines of their bundled client/server modules. Excluded: @leichtgewicht/dns-packet (99.6% of its lines are in @dnsquery/dns-packet, its successor), mdns-js-packet (earlier name of dns-js), dnsd, @serverless-dns/dns-parser and two native-dns-packet forks (near-identical), and the clients dns-query, native-dns, dohdec and multicast-dns. bns stays a lead without a documented message-bytes API; dnspacket-ts is below the ceiling. Each verified path parses the two valid controls (a query and a response with compressed CNAME/A/AAAA/MX answers) to the hand-written oracle summary, has library source coverage and stable AFL++ feedback that differs between the controls. Two valid controls do not establish EDNS0, DNSSEC, TXT, authority/additional or malformed-input behaviour. Package-level adoption metrics include non-DNS use, @portable/dns-packet was first released three weeks before the window ended, and the cell is not a definitive top ten.

[Ranking and search limits](../../../data/javascript/dns/ranking.md) · [Standard API inventory](../../../data/javascript/dns/standard.json)

## Third-party parsers

- [dns-packet](dns-packet/README.md) — verified Docker harness
- [@dnsquery/dns-packet](dnsquery-dns-packet/README.md) — verified Docker harness
- [dns2](dns2/README.md) — verified Docker harness
- [native-dns-packet](native-dns-packet/README.md) — verified Docker harness
- [hbo-dnsd](hbo-dnsd/README.md) — verified Docker harness
- [dns-js](dns-js/README.md) — verified Docker harness
- [@gibme/dns](gibme-dns/README.md) — verified Docker harness
- [@noelminamino/dns-packet](noelminamino-dns-packet/README.md) — verified Docker harness
- [@portable/dns-packet](portable-dns-packet/README.md) — verified Docker harness
- [dns-message](dns-message/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
