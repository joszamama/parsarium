# DNS cell protocol

This cell applies the [general protocol](../../PROTOCOL.md) to one DNS message in the wire format of RFC 1035 section 4: a 12-byte header, then the question, answer, authority and additional sections, with name compression (section 4.1.4). The input is local message bytes. EDNS0 (RFC 6891), DNSSEC record types, zone files, DNS over HTTPS/TLS framing and the two-byte TCP length prefix are out of scope. The controls contain no OPT record.

## Eligibility

A path qualifies only if a documented API takes caller-supplied message bytes (a byte array, buffer or stream) and decodes the header, questions and resource records itself or through a named parser. Resolvers that send queries and return answers, zone-file parsers, packet-capture readers that need a link-layer frame, and wrappers that run `dig` or another process are excluded or left as leads in `data/<ecosystem>/dns/leads.json`. A C library resolver API such as libresolv `ns_initparse` is a standard/runtime path and stays outside the third-party ranking.

No harness opens a socket, contacts a resolver or server, or sends a query. Each harness parses local bytes in process.

## Observed result

The harness reports, from the parsed message:

- header: `id`, `qr`, `opcode`, `aa`, `tc`, `rd`, `ra`, `z`, `rcode`, and the four section counts;
- every question as `{name, type, class}`;
- every record in `answers`, `authority` and `additional` as `{name, type, class, ttl, rdata}`.

Names are lower case and absolute, with a trailing dot. Types and classes are numbers. RDATA is presentation text: a dotted quad for A, RFC 5952 text for AAAA, a name for CNAME, NS and PTR, `<preference> <exchange>` for MX, and quoted strings joined by spaces for TXT. A harness may normalise the library's own presentation (adding the trailing dot, lower case, compressing an IPv6 address from its 16 decoded bytes), but every value must come from the library's parse. `z` holds the three bits after RA (the reserved Z bit, AD and CD). A library that drops the reserved Z bit on decode reports AD and CD only, and its record says so; both controls have all three bits clear.

## Controls

- `controls/dns/response.bin`: the primary control, 113 bytes. ID `0xabcd`, flags `QR RD RA`, NOERROR; question `www.example.test. A IN`; four answers: `www.example.test.` CNAME `example.test.` (TTL 3600), and for `example.test.` an A `192.0.2.10` (300), an AAAA `2001:db8::10` (600) and an MX `10 mail.example.test.` (7200). Every owner name and both name RDATA use compression pointers, to the question name (offset 12) and to its `example.test` suffix (offset 16).
- `controls/dns/query.bin`: the second control for AFL++ feedback, 30 bytes. ID `0x1234`, RD set, one question `example.test. A IN`, no records.

`controls/dns/make_controls.py` writes both files byte for byte without a DNS library. `controls/dns/check_controls.py` is the independent oracle: a small hand-written decoder (header unpacked with `struct`, labels read one at a time, pointers followed backwards only, every byte consumed). It rebuilds both summaries and compares them, with each file's size and SHA-256, to `controls/dns/expected.json`. No parser counted in a DNS cell is used as the oracle.

## Adoption

Paths are ranked within one ecosystem by that ecosystem's existing primary metric: npm 30-day downloads, PyPI Stats last-month downloads, crates.io 90-day recent downloads, Packagist total downloads, pkg.go.dev known importing packages, and deps.dev direct dependents summed over all Maven releases. C and C++ use Debian popcon sourcemax installations from the pinned table `data/curation/popcon-sourcemax-by_inst.gz`, as the C JSON cell does. The searches, their limits and hits, and every lead's metric are in `data/<ecosystem>/dns/registry-snapshot.json` (written by `scripts/snapshot_dns_registry.py`). Package-level metrics include non-DNS use; packet libraries such as gopacket, Scapy or Pcap4J count all their protocols.

## AFL++

The overlay must show parser-derived feedback on both controls: repeated runs of one control give identical maps, and the two controls differ. The receipt records edge counts, the difference between the controls, and the parser source lines covered. The overlay runs no campaign and tests no malformed input.

## Fandango

Fanbase has no DNS spec, and Fandango's own DNS example is a networked client/server spec. `fuzzing/fandango/specs/dns_message.fan` is a local single-message grammar with a documented compression limit; see [the decision](../../fuzzing/fandango/dns-decision.md).
