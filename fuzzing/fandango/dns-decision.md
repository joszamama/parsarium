# DNS message spec

Fanbase has no DNS spec. Its `index.yml` (schema 2, fetched 2026-11-17 at
commit `d20f8d053b1cf7fd37c71e74c2d20f0ed91f4306`, SHA-256
`ec4311210b6dd74cf8ee21156ee20df09f8e95150c9a4492c1c9bdeac09e9bd6`) lists 33
formats and none of them is DNS.

The Fandango 1.3.1 repository does contain
[`evaluation/protocol_testing_eval/dns/dns.fan`](https://github.com/fandango-fuzzer/fandango/blob/v1.3.1/evaluation/protocol_testing_eval/dns/dns.fan)
(SHA-256 `8968e9b39708db6838c061a58ea627938a95a91ed623f5605d117992f693e328`).
It is not used here:

- It describes a client and server exchange over UDP sockets
  (`udp://127.0.0.1:25566`). This pilot parses local message bytes only and
  runs no network experiments.
- It imports the third-party `faker` package, which the pinned Fandango lock
  does not include.
- It writes uncompressed names and compresses them in the network send hook,
  so a file-mode run would not produce the compressed form.

[`specs/dns_message.fan`](specs/dns_message.fan) is a small local grammar
instead. It writes one message per file. The header counts are fixed by the
alternative chosen (a query, or a response with one to four answers), and each
variable `RDLENGTH` is a `where` constraint that Fandango repairs.

## Limits

- Name compression uses one pointer target, the question name at offset 12
  (`C0 0C`). A pointer to a suffix or to an earlier record would depend on the
  lengths before it, so none is generated. The DNS controls also use a pointer
  to the `example.test` suffix at offset 16; the grammar does not.
- Labels come from a fixed lower-case set (`example`, `test`, `www`, `mail`,
  `ns`, `parsarium`), with one to three labels per name.
- Only the question and answer sections are generated. There are no authority
  or additional records, no EDNS0 OPT record, and no opcode other than QUERY.
- RCODE is always 0.

## Check

```sh
PYTHONHASHSEED=0 .venv/fandango-1.3.1-locked/bin/fandango fuzz \
  -f fuzzing/fandango/specs/dns_message.fan -n 30 --random-seed 1 \
  --progress-bar off -d /tmp/fandango-dns -x .bin
```

On 2026-11-17 this produced 30 files: 13 queries and 17 responses with one to
four answers (17 CNAME, 8 MX, 6 TXT, 6 A, 3 AAAA), 13 of them with the
`C0 0C` pointer. Each file decoded with the hand-written oracle in
`controls/dns/check_controls.py` (`summarize`), which follows pointers and
requires every byte to be consumed, and `fandango parse --file-mode binary`
accepted all 30.
